import asyncio
from pyppeteer import launch
import pandas as pd
from datetime import datetime


async def scrape():
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://www.quades.com/nl/vacatures/")

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

    (
        df.rename(columns={0: "title", 1: "date", 2: "meta_tags", 3: "description", 4: "url"})
        .reset_index(drop=True)
        .to_csv(f"data/quades_{datetime.today().strftime('%Y-%m-%d')}.csv")
    )

    await browser.close()


asyncio.get_event_loop().run_until_complete(scrape())
