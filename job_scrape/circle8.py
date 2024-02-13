from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy import create_engine
import numpy as np

_ = load_dotenv(find_dotenv())

# engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False, slow_mo=5000)
    browser = p.chromium.launch(headless=True, slow_mo=4000)
    page = browser.new_page()
    initial_url = "https://www.circle8.nl/opdrachten"
    page.goto(initial_url)
    page.click("#sbs_plp_container-BLOCK_3567 > div > div.ccm-block-page-list-header.row > button")
    page.fill("#sbs_plp_searchBox_BLOCK_3567 > input", "python")
    page.keyboard.press("Enter")
    
    html = page.inner_html("#sbs_plp_container-BLOCK_3567 > div > div.ccm-block-page-list-pages")
    soup = BeautifulSoup(html, "html.parser")
    
    card_list = soup.find_all("div", {"class": "col-md-6 col-xl-3 mt-60"})
    
    body_content = "\n".join([str(x) for x in card_list])

    body_soup = BeautifulSoup(body_content, "html.parser")
    df = (
        pd.DataFrame(
            [x.text.split("\n") for x in body_soup.find_all("ul") if x.text.split("\n") != ""]
        )
        .replace("", np.nan)
        .dropna(axis=1)
        .rename(
            columns={
                3: "Op locatie",
                7: "Looptijd",
                11: "Aantal uur",
                15: "Startdatum",
                19: "Sluitingsdatum",
            }
        )
        .assign(
            **{
                "job_title": [x.text for x in soup.find_all("h5") if x.text != ""],
                "Publicatiedatum": datetime.today().strftime("%Y-%m-%d"),
                "Startdatum": lambda d: pd.to_datetime(d["Startdatum"], format="mixed"),
                "Sluitingsdatum": lambda d: pd.to_datetime(
                    d["Sluitingsdatum"], format="mixed"
                ),
                "url": [x["href"] for x in body_soup.find_all("a")]
            }
        )
        .loc[:, ["job_title", "url", "Startdatum", "Sluitingsdatum", "Op locatie", "Looptijd", "Aantal uur"]]
    )
    df.to_csv(f"data/circle8_{datetime.today().strftime('%Y-%m-%d')}.csv")