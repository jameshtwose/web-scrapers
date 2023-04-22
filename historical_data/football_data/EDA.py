# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())


# %%
def convert_numeric(col):
    try:
        return col.astype(float)
    except (TypeError, ValueError):
        return col


# %%
engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))
# %%
df = pd.read_sql("football_data", engine).apply(
    convert_numeric).dropna(axis=0, subset=["Date"])
# %%
df.info(max_cols=240)
# %%
_ = plt.figure(figsize=(20, 10))
_ = sns.heatmap(df.set_index("Date").isna().T, cbar=False)
_ = plt.title("Missing Values by Date")
# %%
# columns_of_interest = df.columns.tolist()[0:11]
columns_of_interest = ["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR"]
columns_of_interest
# %%
_ = plt.figure(figsize=(7, 5))
_ = sns.heatmap(df[columns_of_interest].set_index("Date").isna().T, cbar=False)
_ = plt.title("Missing Values by Date")
# %%
df[columns_of_interest].info()
# %%
df[columns_of_interest].head()
# %%
# TODO: this is currently not correct
# Need to make a win/loss/draw column that is based on a set of
# if/else statements
team_of_interest = "Portsmouth"
plot_df = (
    df[columns_of_interest]
    .assign(**{
        # "week": lambda x: x["Date"].dt.isocalendar().week,
               "month": lambda x: x["Date"].dt.month,
               "year": lambda x: x["Date"].dt.year,
               "year-month": lambda x: x["year"].astype(str) + "-" + x["month"].astype(str),
            #    "year-week": lambda x: x["year"].astype(str) + "-" + x["week"].astype(str)
               })
    .drop(["month", "Date", "FTAG", "FTHG"], axis=1)
    .loc[lambda x: (x["HomeTeam"] == team_of_interest) | (x["AwayTeam"] == team_of_interest), :]
    .melt(id_vars=["year", "FTR"])
    .loc[lambda x: x["value"] == team_of_interest, :]
    .groupby(["year", "FTR"])
    .count()
    .rename(columns={"value": "win_loss_draw"})
    .drop("variable", axis=1)
    .reset_index()
)
plot_df.shape
# %%
_ = sns.lineplot(data=plot_df, x="year", y="win_loss_draw", hue="FTR")
_ = plt.title(f"Win/Loss/Draw for {team_of_interest}")
# %%
plot_df
# %%
