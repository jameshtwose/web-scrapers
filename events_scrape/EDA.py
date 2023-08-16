# %%
from bs4 import BeautifulSoup

# %%
with open("hipsy.html", "r") as f:
    html = f.read()
# %%
soup = BeautifulSoup(html, "html.parser")
# %%
body = soup.find_all("div")
# %%
event_id_list = [
    div.attrs["wire:key"]
    for div in body
    if "wire:key" in div.attrs.keys() and "event" in div.attrs["wire:key"]
]
# %%
event_id_list
# %%
for event_id in event_id_list:
    event = soup.find_all("div", {"wire:key": event_id})
    print(event)
# %%
print(event[0].getText())
# %%
with open("hipsy_specific_page.html", "r") as f:
    html = f.read()
# %%
soup = BeautifulSoup(html, "html.parser")
# %%
page_title = soup.find("title").getText()
# %%
body = soup.find("body")
# %%
page_event_date = body.find("p", {"class": "text-green"}).getText()
# %%
page_event_location = body.find("p", {"class": "text-base md:text-lg lg:text-xl"}).getText()
# %%
page_event_description = body.find("div", {"class": "description-content"}).getText()
# %%
