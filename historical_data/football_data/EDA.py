# %%
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
from dotenv import load_dotenv, find_dotenv
from utils import convert_numeric, label_wins_losses_draws

_ = load_dotenv(find_dotenv())

# set the style of the plots
if "jms_style_sheet" in plt.style.available:
    plt.style.use("jms_style_sheet")

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
# make a win/loss/draw column that is based on a set of
# if/else statements
team_of_interest = "Portsmouth"
time_interval = "year"
plot_df = (
    df[columns_of_interest]
    .loc[lambda x: (x["HomeTeam"] == team_of_interest) | (x["AwayTeam"] == team_of_interest), :]
    .assign(**{
        # "week": lambda x: x["Date"].dt.isocalendar().week,
        "month": lambda x: x["Date"].dt.month,
        "year": lambda x: x["Date"].dt.year,
        "year-month": lambda x: x["year"].astype(str) + "-" + x["month"].astype(str),
        "win_loss_draw": lambda x: x.apply(lambda y: label_wins_losses_draws(y, team_of_interest), axis=1),
            #    "year-week": lambda x: x["year"].astype(str) + "-" + x["week"].astype(str)
            })
    .drop(["month", "Date", "FTAG", "FTHG", "FTR"], axis=1)
    .melt(id_vars=[time_interval, "win_loss_draw"])
    .loc[lambda x: x["value"] == team_of_interest, :]
    .groupby([time_interval, "win_loss_draw"])
    .count()
    .rename(columns={"value": "amount"})
    .drop("variable", axis=1)
    .reset_index()
)
plot_df.shape
# %%
_ = sns.lineplot(data=plot_df, x=time_interval,
                 y="amount", hue="win_loss_draw")
_ = plt.title(f"Win/Loss/Draw for {team_of_interest}")
# %%
diff_df = plot_df.groupby(time_interval).apply(
    lambda x: x[x["win_loss_draw"] == "win"]["amount"].iloc[0] - x[x["win_loss_draw"] == "loss"]["amount"].iloc[0]).reset_index().rename(columns={0: "diff"})
# %%
_ = sns.lineplot(data=diff_df, x=time_interval,
                 y="diff")
_ = plt.title(f"Win/Loss difference for {team_of_interest}")

# %%
