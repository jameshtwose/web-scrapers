from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy import create_engine

_ = load_dotenv(find_dotenv())

engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False, slow_mo=1000)
    browser = p.chromium.launch(headless=True, slow_mo=1000)
    page = browser.new_page()
    initial_url = "https://mijn.freelance.nl/"
    page.goto(initial_url)
    page.fill(
        "#login > div > div > div.content > div > form > ul > li.email.required > div > div > input[type=email]",
        os.getenv("FREELANCE_NL_USERNAME"),
    )
    page.fill(
        "#login > div > div > div.content > div > form > ul > li.password.required > div > div > input[type=password]",
        os.getenv("FREELANCE_NL_PASSWORD"),
    )
    page.click("#login > div > div > div.content > div > form > button")
    page.fill(
        "#filterform > div > div.matchfilter > div.matchfilter__query-fields.fields > div.matchfilter__query-items.items > div > div > div > div > div > div > input",
        "python",
    )
    page.keyboard.press("Enter")
    page.wait_for_timeout(5000)
    html = page.inner_html("#projects")
    soup = BeautifulSoup(html, "html.parser")

    all_df = pd.DataFrame()
    for url_end in [x.find("a")["href"] for x in soup.find_all(class_="open")][0:20]:
        page.goto(f"https://mijn.freelance.nl{url_end}")
        new_page_html = page.inner_html("#content")
        new_page_soup = BeautifulSoup(new_page_html, "html.parser")
        value_list = [x.text for x in new_page_soup.find_all("span", class_="value")]
        name_list = [
            x.text.replace("\n", "-").replace("  ", "")
            for x in new_page_soup.find_all("span", class_="name")
        ][0 : len(value_list)]
        df = pd.DataFrame(
            [new_page_soup.find("h1").text] + value_list,
            index=["job_title"] + name_list,
            columns=[0],
        ).T.assign(
            **{
                "description": new_page_soup.find("div", class_="htmldescription")
                .text.replace("\n", " ")
                .replace("  ", ""),
                "url": f"https://mijn.freelance.nl{url_end}",
            }
        )
        all_df = pd.concat([all_df, df])

    print(all_df.head())
    print(all_df.shape)
    print(all_df["job_title"].value_counts())
    print(all_df["Geplaatst door"].value_counts())
    
    # all_df.to_csv(
    #     f"~/Coding/web-scrapers/job_scrape/freelance_nl_data/freelance_nl_{datetime.today().strftime('%Y-%m-%d')}.csv", index=False
    # )
    with engine.connect() as connection:
        all_df.to_sql("freelance_nl_data", con=connection, if_exists="append", index=False)
