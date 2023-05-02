# %%
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# %%
engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

# %%
df = pd.read_sql("opta_power_data", engine)

# %%
print("\nData Frame Head:")
print("================")
print(df.head(3))
# %%
print("\nData Frame Descriptives:")
print("========================")
df.info()
print(df.describe())
# %%
