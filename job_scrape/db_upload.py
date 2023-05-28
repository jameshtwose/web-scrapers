# %%
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
from glob import glob

_ = load_dotenv(find_dotenv())

# %%
engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

# %%
df = pd.concat([pd.read_csv(x) for x in glob("./freelance_nl_data/*")])

df.head()
# %%
# df.to_sql("freelance_nl_data", engine, if_exists="append", index=False)
# %%
pd.read_sql("SELECT * FROM freelance_nl_data", engine)
# %%
