from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy import create_engine
import re

_ = load_dotenv(find_dotenv())

# engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))
engine = create_engine("sqlite:///hipsy.db")

with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False, slow_mo=1000)
    browser = p.chromium.launch(headless=True, slow_mo=1000)
    
    page = browser.new_page()
    initial_url = "https://hipsy.nl/events"
    page.goto(initial_url)
    html = page.inner_html("body")
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find_all("div")
    event_id_list = [
        div.attrs["wire:key"]
        for div in body
        if "wire:key" in div.attrs.keys() and "event" in div.attrs["wire:key"]
    ]
    for event_id in event_id_list:
        event = soup.find_all("div", {"wire:key": event_id})
        print(event_id)
        try:
            event_url = event[0].find("a").attrs["href"]
            page.goto(event_url)
            print(event_url)
            html = page.inner_html("*")
            soup = BeautifulSoup(html, "html.parser")
            page_title = soup.find("title").getText()
            print(page_title)
            body = soup.find("body")
            page_event_date = body.find("p", {"class": "text-green"}).getText()
            page_event_location = body.find("p", {"class": "text-base md:text-lg lg:text-xl"}).getText()
            page_event_description = body.find("div", {"class": "description-content"}).getText()
            print(page_event_date)
            print(page_event_location)
            page.goto(initial_url)
        except Exception as e:
            print(e)
            continue