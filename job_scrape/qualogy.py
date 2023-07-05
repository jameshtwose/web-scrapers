import asyncio
from pyppeteer import launch
import pandas as pd
from datetime import datetime


async def scrape():
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://www.werkenbijqualogy.com/vacatures/search/python/soort-dienstverband/interim")

    page_select = await page.querySelector("#vacancy-list")
    page_content = await page_select.getProperty("innerHTML")
    page_content_value = await page_content.jsonValue()
    # print(page_content_value)

    # vacancy-results > div:nth-child(1) > div
    list_content = await page_select.querySelectorAll(".card")

    # print(list_content)
    df = pd.DataFrame()
    for block in list_content:
        response_query = await block.getProperty("innerText")
        response = await response_query.jsonValue()
        url_query = await block.querySelector("a")
        url_get = await url_query.getProperty("href")
        url = await url_get.jsonValue()

        df = pd.concat([df, pd.DataFrame([x for x in response.split("\n") if x != "" and x != "Nieuw"] + [url]).T])
    (
        df
        .rename(columns={0: "job_title", 2: "description", 5: "url"})
        .assign(**{"Publicatiedatum": datetime.today().strftime('%Y-%m-%d')})
        .reset_index(drop=True)
        .loc[:, ["job_title", "Publicatiedatum", "description", "url"]]
        .to_csv(f"data/qualogy_{datetime.today().strftime('%Y-%m-%d')}.csv")
    )

    await browser.close()


asyncio.get_event_loop().run_until_complete(scrape())
