# %%
import os
import requests
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# %%
engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

# %%
dfs_list = []
for year in range(1993, 2023):
    r = requests.get(f"https://football-data.co.uk/mmz4281/{str(year)[2:]}{str(year+1)[2:]}/all-euro-data-{year}-{year+1}.xlsx").content
    dfs_dict = pd.read_excel(r, sheet_name=None)
    df = pd.concat([dfs_dict[key] for key in dfs_dict.keys()])
    dfs_list.append(df
                    .assign(**{"year_range": f"{year} - {year+1}"})
                    .dropna(thresh=1, axis=0)
                    )
# %%
all_df = pd.concat(dfs_list)
# %%
remove_cols_list = all_df.filter(regex="Unnamed").columns.tolist()
_ = all_df.drop(columns=remove_cols_list, inplace=True)
# %%
all_df.info(max_cols=240)
# %%
# all_df.to_sql("football_data", engine, if_exists="replace", index=False)
# %%
