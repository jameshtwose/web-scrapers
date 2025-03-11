from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy import create_engine

_ = load_dotenv(find_dotenv())

engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

def convert_str_to_dt(s):
    month_map = {
        "jan": "Jan",
        "feb": "Feb",
        "mrt": "Mar",
        "apr": "Apr",
        "mei": "May",
        "jun": "Jun",
        "jul": "Jul",
        "aug": "Aug",
        "sep": "Sep",
        "okt": "Oct",
        "nov": "Nov",
        "dec": "Dec"
    }
    
    for dutch, english in month_map.items():
        s = s.lower().replace(dutch, english)
    
    try:
        # 24 feb 2025 15:32
        if ":" in s:
            return datetime.strptime(s, "%d %b %Y %H:%M").strftime("%Y-%m-%d %H:%M")
        else:
            # 10 mrt 2025
            return datetime.strptime(s, "%d %b %Y").strftime("%Y-%m-%d")
    except Exception as e:
        print(f"Error converting {s}: {e}")
        return s

with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False, slow_mo=1000)
    browser = p.chromium.launch(headless=True, slow_mo=1000)
    page = browser.new_page()
    initial_url = "https://mijn.freelance.nl/"
    page.goto(initial_url)
    try:
        page.click("body > dialog > div.cf1e63.cf0e2J.cfM1eQ > div > div.cfAdwL.cf7ddU > div.cf2L3T.cffR0U > div.cf3Tgk.cf2pAE.cfAdwL.cf1IKf > div:nth-child(2) > button")
    except:
        pass
    page.fill(
        "#E-mailadres",
        os.getenv("FREELANCE_NL_USERNAME"),
    )
    page.fill(
        "#Wachtwoord",
        os.getenv("FREELANCE_NL_PASSWORD"),
    )
    page.click("body > main > div > div.w-full.lg\:rounded-2xl.lg\:bg-white.lg\:p-10.lg\:shadow-sm > div > form > div:nth-child(5) > button")
    page.goto("https://mijn.freelance.nl/opdracht-vinden/zoeken")
    page.fill(
        "body > div.flex.pt-14.lg\:h-full.lg\:pb-0.pb-14 > div > main > header > div.grid.gap-4 > div.grid.gap-2 > div > ul > li > input",
        "python",
    )
    page.keyboard.press("Enter")
    page.wait_for_timeout(5000)
    html = page.inner_html("body > div.flex.pt-14.lg\:h-full.lg\:pb-0.pb-14 > div > main > section.lg\:px-10.lg\:pt-6 > div.grid.min-h-96.content-start")
    soup = BeautifulSoup(html, "html.parser")
    # with open("freelance_nl.html", "w") as file:
    #     file.write(soup.prettify())

    all_df = pd.DataFrame()
    for url_end in soup.select('a'):
        print(url_end['href'])
        page.goto(f"https://mijn.freelance.nl{url_end['href']}")
        new_page_html = page.inner_html("body > div.flex.pt-14.lg\:h-full.lg\:pb-0.pb-14 > div > main > div > div > div")
        new_page_soup = BeautifulSoup(new_page_html, "html.parser")
        
        # with open("freelance_nl.html", "w") as file:
        #     file.write(new_page_soup.prettify())

        
        df = pd.DataFrame(
            {
                "job_title": new_page_soup.find('h2').text.strip(),
                "Publicatiedatum": convert_str_to_dt(new_page_soup.find('p').text.split('op')[-1].strip()),
                "Weergaven": new_page_soup.find('span').text.strip(),
                "Reacties": new_page_soup.find_all('span')[1].text.strip(),
                "Startdatum": convert_str_to_dt(new_page_soup.find_all('dd')[3].text.strip()),
                "Looptijd": new_page_soup.find_all('dd')[4].text.strip(),
                "Aantal uur": new_page_soup.find_all('dd')[5].text.strip(),
                "Tarief": new_page_soup.find_all('dd')[6].text.strip(),
                "Contract": new_page_soup.find_all('dd')[7].text.strip(),
                "Eindklant": new_page_soup.find_all('dd')[8].text.strip() if len(new_page_soup.find_all('dd')) > 8 else None,
                "description": new_page_soup.find(class_='prose').text.strip(),
                "Geplaatst door": new_page_soup.find('strong').text.strip(),
                "url": f"https://mijn.freelance.nl{url_end['href']}",
            },
            index=[0]
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
