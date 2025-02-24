# %%
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv, find_dotenv
from glob import glob

_ = load_dotenv(find_dotenv(usecwd=True), override=True)

print(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

# %%
engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

# %%
# df = pd.concat([pd.read_csv(x) for x in glob("./freelance_nl_data/*")])
df = pd.read_csv(
    "./freelance_nl_data/freelance_nl_all_fixed.csv"
)

df.head()
# df.shape
# %%
# drop the table
# with engine.begin() as conn:
#     conn.execute(text("DROP TABLE IF EXISTS freelance_nl_data"))

# %%
df.to_sql("freelance_nl_data", engine, if_exists="append", index=False)
# %%
all_df = pd.read_sql("SELECT * FROM freelance_nl_data", engine)


# %%
all_df.shape

# %%
# all_df.reset_index().rename(columns={"index": "id"}).to_csv(
#     "./freelance_nl_data/freelance_nl_all.csv",
#     index=False,
# )