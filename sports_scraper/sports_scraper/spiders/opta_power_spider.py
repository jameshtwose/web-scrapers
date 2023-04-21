import scrapy
from scrapy_playwright.page import PageMethod
import logging


class OptaPowerSpiderSpider(scrapy.Spider):
    name = "opta_power_spider"
    start_urls = ["https://dataviz.theanalyst.com/opta-power-rankings/"]

    def start_requests(self):
        yield scrapy.Request("https://dataviz.theanalyst.com/opta-power-rankings/",
                             meta={
                                 "playwright": True,
                                 "playwright_include_page": True,
                                #  "playwright_page_methods": {"click": PageMethod("click", "button:has-text('>')", timeout=10000), }
                             },
                              callback=self.parse
                             )

    async def parse(self, response):
        
        def click_page(response):
            page=response.meta["playwright_page"]
            page.click("button:has-text('>')")
            self.logger.info("Clicked on the next page button")
        
        # page = response.meta["playwright_page"]
        # page.click("button:has-text('>')")
        
        page_selector_div = response.css("div.CoypyxzZG6qYm9LcBWtI")
        page_count_span = str(page_selector_div.xpath(".//span/text()").get())
        # page_on = int(page_count_span.split(" ")[0])
        page_last = int(page_count_span.split(" ")[-1])
        
        for page_on in range(1, 3):
            page_selector_div = response.css("div.CoypyxzZG6qYm9LcBWtI")
            page_count_span = str(page_selector_div.xpath(".//span/text()").get())
            print(page_count_span)
            for item in response.xpath("//table//tr"):
                yield {
                    "team": item.xpath(".//td[2]/div/div/div/text()").get(),
                    "rating": item.xpath(".//td[3]/text()").get(),
                    "ranking_change_7_days": item.xpath(".//td[4]/text()").get()
                }
                
            if page_on != page_last:                
                click_page(response)
        # next_page = response.xpath("//a[@class='next page-numbers']/@href").get()
        # next_page = response.xpath('button:text(">")').get()
        
        # if page_on != page_last:
        #     print(page_count_span)
        #     # page = response.meta["playwright_page"]
        #     # page.click("button:has-text('>')")
        #     # self.logger.info("Clicked on the next page button")
        #     yield scrapy.Request(
        #         "https://dataviz.theanalyst.com/opta-power-rankings/",
        #         callback=self.click_page
        #         )
                
        # yield {
        #     "next_page": response.xpath('//button[2]/text()').get(),
        #     "next_page_v2": response.css("div.CoypyxzZG6qYm9LcBWtI").get(),
        #     "next_page_v3": page_selector_div.xpath(".//button[2]/text()").get(),
        #     "next_page_v4": page_selector_div.xpath(".//button[1]/text()").get(),
        #     "next_page_v5": page_selector_div.xpath(".//span/text()").get(),
        # }



# //*[@id="root"]/div/div/div[2]/div[8]/div[1]/table/tbody/tr[1]/td[4]
# //*[@id="root"]/div/div/div[2]/div[8]/div[2]/button[2]
# #root > div > div > div.hXafwz_cbVF7HDOcyAH_ > div:nth-child(8) > div.CoypyxzZG6qYm9LcBWtI > span
# //*[@id="root"]/div/div/div[2]/div[8]/div[2]/span
