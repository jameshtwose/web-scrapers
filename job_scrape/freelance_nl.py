import asyncio
from pyppeteer import launch
import pandas as pd

async def scrape():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://mijn.freelance.nl/acquisitie/mijn-matches?s706310')
    
    #projects > div > div.projectlist
    # list_content = page.querySelector("div.projectlist")
    # print(list_content)
    
    print(page.content())
    
    await browser.close()
    
asyncio.get_event_loop().run_until_complete(scrape())
    