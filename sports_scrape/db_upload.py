# %%
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# %%
engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

# %%
df = (pd.read_csv("data/opta_power_rankings.csv", index_col=0)
      .assign(**{"date_scraped": pd.to_datetime("today").strftime("%Y-%m-%d %H:%M:%S")}))

df.head()
# %%
# df.to_sql("opta_power_data", engine, if_exists="append", index=False)
# %%
