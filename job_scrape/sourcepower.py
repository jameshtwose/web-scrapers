import asyncio
from pyppeteer import launch
import pandas as pd
from datetime import datetime


async def scrape():
    browser = await launch()
    page = await browser.newPage()
    await page.goto("https://www.sourcepower.nl/opdrachten/?_sf_s=python")

    selector = "body > div.elementor.elementor-644.elementor-location-archive > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-402d15d.elementor-section-boxed.elementor-section-height-default > div > div > div > div.elementor-element.elementor-element-bd0ab9a.elementor-grid-1.elementor-posts--thumbnail-top.elementor-grid-tablet-2.elementor-grid-mobile-1.elementor-widget.elementor-widget-archive-posts > div > div"
    # page_select = await page.querySelector("#ecs-posts")
    page_select = await page.querySelector(selector)
    # page_content = await page_select.getProperty("innerHTML")
    # page_content_value = await page_content.jsonValue()

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
        df
        .rename(columns={1: "Publicatiedatum", 3: "eindklant", 5: "Aantal uur", 6: "job_title", 8: "description", 10: "url"})
        .reset_index(drop=True)
        .loc[:, ["job_title", "Publicatiedatum", "description", "url", "eindklant", "Aantal uur"]]
        .to_csv(f"data/sourcepower_{datetime.today().strftime('%Y-%m-%d')}.csv")
    )

    await browser.close()


asyncio.get_event_loop().run_until_complete(scrape())
