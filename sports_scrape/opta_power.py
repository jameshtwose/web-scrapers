import asyncio
from pyppeteer import launch
import pandas as pd

async def scrape():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://dataviz.theanalyst.com/opta-power-rankings/')
    
    page_amount = await page.querySelector("div.CoypyxzZG6qYm9LcBWtI > span")
    page_amount_text = await page_amount.getProperty("textContent")
    page_amount_value = await page_amount_text.jsonValue()
    page_total = int(page_amount_value.split(" ")[-1])
    
    df_list = []
    for page_number in range(1, page_total+1):
        print(f"page {page_number} of {page_total}")
        table_content = await page.querySelector("div._YwuNK63XIsAkFnoxRRM")
        for table_row in await table_content.querySelectorAll("tr"):
            text_row = await table_row.getProperty("innerText")
            row = await text_row.jsonValue()
            if [x.replace("\n", "") for x in row.split("\t")][-1] != "RANKING CHANGE 7 DAYS":
                df_list.append([x.replace("\n", "") for x in row.split("\t")])
        await page.click("button:nth-child(3)")

    df = pd.DataFrame(df_list).rename(columns={0: "rank", 1: "team", 2: "rating", 3: "ranking_change_7_days"})
    df.to_csv("data/opta_power_rankings.csv")

    await browser.close()

asyncio.get_event_loop().run_until_complete(scrape())
