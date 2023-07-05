import os
import asyncio
from pyppeteer import launch
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine

_ = load_dotenv(find_dotenv())

engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

async def scrape():
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://www.quades.com/nl/vacatures/?_sf_s=python")

    page_select = await page.querySelector("#posts-container")
    page_content = await page_select.getProperty("innerHTML")
    page_content_value = await page_content.jsonValue()

    list_content = await page_select.querySelectorAll("article")

    df = pd.DataFrame()
    for block in list_content:
        response_query = await block.getProperty("innerText")
        response = await response_query.jsonValue()
        url_query = await block.querySelector("a")
        url_get = await url_query.getProperty("href")
        url = await url_get.jsonValue()

        df = pd.concat([df, pd.DataFrame([x for x in response.split("\n") if x != ""] + [url]).T])

    all_df = (
        df.rename(columns={0: "job_title", 1: "Publicatiedatum", 2: "meta_tags", 3: "description", 4: "url"})
        .reset_index(drop=True)
        .assign(**{"Publicatiedatum": lambda x: pd.to_datetime(x["Publicatiedatum"], format="%d-%m-%Y").dt.strftime("%d-%m-%Y %H:%M")})
        # .loc[:, ["job_title", "Publicatiedatum", "description", "url"]]
        .to_csv(f"data/quades_{datetime.today().strftime('%Y-%m-%d')}.csv")
    )
    
    # with engine.connect() as connection:
    #     all_df.to_sql("freelance_nl_data", con=connection, if_exists="append", index=False)

    await browser.close()


asyncio.get_event_loop().run_until_complete(scrape())
