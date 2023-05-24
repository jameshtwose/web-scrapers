# %%
import pandas as pd
from glob import glob
from datetime import datetime, timedelta
import textwrap
import matplotlib.pyplot as plt
import seaborn as sns

if "jms_style_sheet" in plt.style.available:
    plt.style.use("jms_style_sheet")

# %%
column_list = [
    "job_title",
    "Geplaatst door",
    "Publicatiedatum",
    "Startdatum",
    "Op locatie",
    "Looptijd",
    "Aantal uur",
    "Reacties",
    "description",
]
df = (
    pd.concat([pd.read_csv(x) for x in glob("freelance_nl_data/*")])
    .loc[:, column_list]
    .assign(
        **{
            "Publicatiedatum": lambda x: pd.to_datetime(
                x["Publicatiedatum"], format="%d-%m-%Y %H:%M"
            ),
            "Reacties": lambda x: x["Reacties"].str.split(" ", expand=True)[0].astype(int),
        }
    )
    .sort_values("Publicatiedatum", ascending=False)
    .reset_index(drop=True)
)
# %%
df.head()
# %%
_ = sns.countplot(y="Aantal uur", data=df)
# %%
_ = sns.countplot(y="Op locatie", data=df)
# %%
_ = sns.countplot(y="Looptijd", data=df)
# %%
_ = sns.countplot(y="Geplaatst door", data=df)
# %%
plot_df = df.loc[lambda x: x["job_title"].str.contains("Data|data|Python|BI"), :]
_ = sns.countplot(y="job_title", data=plot_df)
# %%
select_df = df.loc[
    lambda x: x["Publicatiedatum"] >= datetime.now() - timedelta(days=1)
].loc[lambda x: x["job_title"].str.contains("Data|data|Python|BI"), :]
for i, x in enumerate(select_df["job_title"].unique()):
    print("\n", i, x)
    print("\n".join(textwrap.wrap(plot_df.iloc[i, :]["description"], width=50)))
# %%
select_df
# %%
select_df["Aantal uur"].value_counts()
# %%
