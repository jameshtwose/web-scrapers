# %%
import pandas as pd
from glob import glob
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
    "description",
]
df = pd.concat([pd.read_csv(x) for x in glob("freelance_nl_data/*")]).loc[:, column_list]
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
plot_df = df.loc[lambda x: x["job_title"].str.contains("Data|data|Python"), :]
_ = sns.countplot(y="job_title", data=plot_df)
# %%
for i, x in enumerate(plot_df["job_title"].unique()):
    print("\n", i, x)
    print("\n".join(textwrap.wrap(plot_df.iloc[i, :]["description"], width=50)))
# %%
