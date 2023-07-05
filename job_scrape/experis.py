import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime


url = "https://www.experis.nl/api/services/Jobs/searchjobs"
payload = {
    "sf": "sortOrder",
    "filter": {
        "page": "1",
        "searchKeyword": "python",
        "sortOrder": [{"value": "Datum", "key": "d407fd7533324acba682d0595ab7533e"}],
        "employmentType": [
            {"value": "Tijdelijk", "key": "ec5c97c476d94617b072dbbd4a95d5c7"}
        ],
        "offset": 0,
        "totalCount": 0,
        "limit": 10,
        "searchkeyword": "python",
        "haslocation": False,
        "language": "nl",
    },
    "referrer": "https://www.experis.nl/nl/zoek-vacatures?page=1&searchKeyword=python&sortOrder=Datum&employmentType=Tijdelijk&sf=employmentType&ids={sortOrder:[d407fd7533324acba682d0595ab7533e],employmentType:[ec5c97c476d94617b072dbbd4a95d5c7]}",
    "referrerPolicy": "strict-origin-when-cross-origin",
}
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-GB,en;q=0.9",
    "Content-Type": "application/json;charset=utf-8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5.1 Safari/605.1.15",
}

response = requests.post(url, json=payload, headers=headers)

# Access the response data
data = response.json()


def get_description(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    description = soup.find("div", {"class": "details-rich-text"}).text
    return description


df = (
    pd.DataFrame(data["jobsItems"])
    .assign(
        **{
            "url": lambda d: "https://www.experis.nl" + d["jobURL"],
            "description": lambda d: d["url"].apply(get_description),
            "Tarief": lambda d: d["salaryRate"].apply(
                lambda x: int(re.findall(r"\b\d+\b", x)[0]) / 40 / 5
            ),
        }
    )
    .rename(
        columns={
            "jobTitle": "job_title",
            "publishfromDate": "Publicatiedatum",
        }
    )
    .loc[:, ["job_title", "Publicatiedatum", "description", "url", "Tarief"]]
)

df.to_csv(f"data/experis_{datetime.today().strftime('%Y-%m-%d')}.csv")
