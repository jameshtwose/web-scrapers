# sports-scraping
Scraping various websites for information on difference sports (scores, betting odds, etc.)

### Installation
1. Clone the repository - `git clone git@github.com:jameshtwose/sports-scraping.git`
2. Install the requirements - `pip install -r requirements.txt`

### Setup
- create the scrapy framework - `scrapy startproject sports_scraper`

### Usage
- cd into the project directory - `cd sports_scraper`
- start the scrapy shell - `scrapy shell`
- fetch the page - `fetch('https://www.theanalyst.com/eu/2023/04/who-are-the-best-football-team-in-the-world-opta-power-rankings/')`
- fetch the page - `fetch('http://0.0.0.0:8050/render.html?url=https://www.theanalyst.com/eu/2023/04/who-are-the-best-football-team-in-the-world-opta-power-rankings/')`
- fetch the page - `fetch('https://dataviz.theanalyst.com/opta-power-rankings/')`
- fetch the page - `fetch('http://0.0.0.0:8050/render.html?url=https://dataviz.theanalyst.com/opta-power-rankings/')`
- run the spider - `scrapy crawl opta_power_spider`