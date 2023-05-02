# %%
import requests
import pandas as pd

# %%
url = "https://www.football-data.co.uk/mmz4281/2223/E0.csv"
# %%
response = requests.get(url)
# %%
pd.DataFrame(response.text).head()
# %%
pd.DataFrame(response.content).head()
# %%
response.content[0]
# %%
