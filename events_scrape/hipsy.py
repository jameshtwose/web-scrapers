from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy import create_engine
import re
import time

_ = load_dotenv(find_dotenv())

# engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))
engine = create_engine("sqlite:///hipsy.sqlite")

with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False, slow_mo=1000)
    browser = p.chromium.launch(headless=True, slow_mo=1000)

    page = browser.new_page()
    initial_url = "https://hipsy.nl/events"
    page.goto(initial_url)
    page.mouse.wheel(delta_x=0, delta_y=30000)
    time.sleep(10)
    html = page.inner_html("body")
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find_all("div")
    event_id_list = [
        div.attrs["wire:key"]
        for div in body
        if "wire:key" in div.attrs.keys() and "event" in div.attrs["wire:key"]
    ]
    print(f"Found {len(event_id_list)} events")
    df = pd.DataFrame()
    for event_id in event_id_list:
        event = soup.find_all("div", {"wire:key": event_id})
        try:
            event_url = event[0].find("a").attrs["href"]
            page.goto(event_url)
            print(event_url)
            inner_html = page.inner_html("*")
            inner_soup = BeautifulSoup(inner_html, "html.parser")
            page_title = inner_soup.find("title").getText()
            inner_body = inner_soup.find("body")
            page_event_date = inner_body.find("p", {"class": "text-green"}).getText()
            page_event_location = inner_body.find(
                "p", {"class": "text-base md:text-lg lg:text-xl"}
            ).getText()
            page_event_description = inner_body.find(
                "div", {"class": "description-content"}
            ).getText()
            df = pd.concat(
                [
                    df,
                    pd.DataFrame(
                        {
                            "event_id": [event_id],
                            "page_title": [page_title],
                            "page_event_date": [page_event_date],
                            "page_event_location": [page_event_location],
                            "page_event_description": [page_event_description],
                            "event_url": [event_url],
                            "scrape_datetime": [datetime.now()],
                        }
                    , index=[0]),
                ]
            )
            page.goto(initial_url)
            page.mouse.wheel(delta_x=0, delta_y=20000)
        except Exception as e:
            print(e)
            continue
        
    with engine.connect() as conn:
        df.to_sql("hipsy", conn, if_exists="append", index=False)