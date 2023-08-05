# a streamlit dashboard to display the results of the job scrape
# to run the dashboard locally, run the following command from the root directory:
# streamlit run ./job_scrape/dashboard.py

import streamlit as st
import pandas as pd
from glob import glob
import plotly.express as px
from dotenv import load_dotenv, find_dotenv
import os
from sqlalchemy import create_engine
from datetime import datetime
import numpy as np

_ = load_dotenv(find_dotenv())

engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

# configure the page
st.set_page_config(
    page_title="Freelance Jobs Dashboard", page_icon=":sparkles:", layout="wide"
)

single_color_palette = ["#8f0fd4"]
double_color_palette = ["#8f0fd4", "#E8C003"]


def convert_looptijd_to_number(x):
    """Convert looptijd to number expressed in month units.

    Args:
        x (str): looptijd string

    Returns:
        float: looptijd expressed in months

    """
    if "maanden" in x:
        return int(x.split(" ")[0])
    elif "weken" in x:
        return int(x.split(" ")[0]) / 4
    elif "dagen" in x:
        return int(x.split(" ")[0]) / 30
    elif "jaar" in x:
        return int(x.split(" ")[0]) * 12


# @st.cache_data()
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


@st.cache_data(ttl=60)
def load_data():
    column_list = [
        "job_title",
        "Publicatiedatum",
        "description",
        "url",
        "Geplaatst door",
        "Startdatum",
        "Op locatie",
        "Looptijd",
        "Aantal uur",
        "Tarief",
        "Contract",
        "Reacties",
    ]
    return (
        # pd.concat([pd.read_csv(x) for x in glob("./job_scrape/freelance_nl_data/*")])
        pd.read_sql("SELECT * FROM freelance_nl_data", engine)
        .loc[:, column_list]
        .drop_duplicates(
            subset=[
                "job_title",
                "Publicatiedatum",
                "Startdatum",
                "Op locatie",
                "Looptijd",
                "Aantal uur",
                "Tarief",
            ],
            keep="last",
        )
        .assign(
            **{
                "Publicatiedatum": lambda x: pd.to_datetime(
                    x["Publicatiedatum"], format="%d-%m-%Y %H:%M"
                ),
                "Reacties": lambda x: x["Reacties"].str.split(" ", expand=True)[0]
                # .fillna(0)
                .astype(int),
                "Geplaatst door": lambda x: x["Geplaatst door"].fillna("Onbekend"),
                "minimum_aantal_uur": lambda x: x["Aantal uur"].str.split(
                    "-", expand=True
                )[0]
                # .fillna(40)
                .astype(int),
                "looptijd_in_months": lambda x: x["Looptijd"]
                # .fillna("12 maanden")
                .apply(convert_looptijd_to_number),
            }
        )
        .sort_values("Publicatiedatum", ascending=False)
        .reset_index(drop=True)
    )


# load the data
df = load_data()

# implement a sidebar
st.sidebar.title("Job Scrape Dashboard")
st.sidebar.markdown(
    """
    This dashboard displays the results of the job scrape.
    """
)
keyword_in_description = st.sidebar.text_input(
    "Enter a keyword to search for in the description (supports regex e.g. python|aws)",
    value="python",
    key="keyword_in_description",
    help="Enter a keyword to search for in the description.",
)
date_range = st.sidebar.date_input(
    "Select a date range",
    value=[df["Publicatiedatum"].dt.date.min(), df["Publicatiedatum"].dt.date.max()],
    min_value=df["Publicatiedatum"].dt.date.min(),
    max_value=df["Publicatiedatum"].dt.date.max(),
    key="date",
    help="Select a date range to display the jobs posted between those dates.",
)
minimum_aantal_uur = st.sidebar.slider(
    "Select the minimum amount of hours",
    value=36,
    min_value=16,
    max_value=40,
    step=1,
    key="minimum_aantal_uur",
    help="Select the minimum amount of hours to display the jobs above a certain hour amount.",
)
looptijd_in_months = st.sidebar.slider(
    "Select the minimum duration in months of the job",
    value=3,
    min_value=0,
    max_value=40,
    step=1,
    key="looptijd_in_months",
    help="Select the minimum duration in months to display the jobs above a certain duration.",
)
location_list = st.sidebar.multiselect(
    "Select a/ some location(s)",
    df["Op locatie"].unique(),
    key="location",
    help="Select a location to display the jobs in that location.",
)
if len(location_list) == 0:
    location_list = df["Op locatie"].unique()
chosen_jobs = st.sidebar.multiselect(
    "Select a/ some job title(s)",
    df["job_title"].unique(),
    key="job_title",
    default=df.loc[
        lambda x: x["job_title"].str.contains("Data|data"), "job_title"
    ].unique(),
    help="Select a job title to display the description.",
)
st.sidebar.markdown(
    """
    <div style="text-align: center; padding-right: 10px; padding-top: 20px;">
        <img alt="logo" src="https://services.jms.rocks/img/logo.png" width="100">
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    """
    <div style="text-align: center; color: #E8C003; margin-top: 40px; margin-bottom: 40px;">
        <a href="https://services.jms.rocks" style="color: #E8C003;">Created by James Twose</a>
    </div>
    """,
    unsafe_allow_html=True,
)


if chosen_jobs == []:
    chosen_jobs = df["job_title"].unique()

# main page
st.title("Freelance Job Scrape Dashboard")

# amount of jobs scraped
st.markdown(
    f"""
    <h2 style="color: rgb(232, 192, 3); font-size: 20px;">
        Amount of Jobs Scraped = {df.shape[0]}
    </h2>
    """,
    unsafe_allow_html=True,
)

# display all the data
# st.header("All Scraped Data")
# st.write(df.to_html(render_links=True, escape=False, index=False), unsafe_allow_html=True)
# st.dataframe(df)

# plot the amount of jobs per Date
# st.header("Amount of Jobs per Date")
st.write(
    px.line(
        df.assign(**{"date": lambda x: x["Publicatiedatum"].dt.date})
        .groupby("date")
        .agg({"job_title": "count"})
        .sort_values("date", ascending=False)
        .reset_index(),
        x="date",
        y="job_title",
        title="Amount of Jobs per date",
        color_discrete_sequence=single_color_palette,
    )
)

# display the data for the selected job titles
if len(date_range) == 2:
    selected_df = (
        df.loc[lambda x: x["job_title"].isin(chosen_jobs), :]
        .loc[
            lambda x: x["Publicatiedatum"].dt.date.between(
                date_range[0], date_range[1]
            ),
            :,
        ]
        .loc[lambda x: x["minimum_aantal_uur"] >= minimum_aantal_uur, :]
        .loc[lambda x: x["looptijd_in_months"] >= looptijd_in_months, :]
        .loc[lambda x: x["Op locatie"].isin(location_list), :]
        .loc[
            lambda x: x["description"].str.contains(keyword_in_description, case=False),
            :,
        ]
    )
else:
    selected_df = df.loc[lambda x: x["job_title"].isin(chosen_jobs), :]

st.header("Selected Job Title(s)")
# amount of selected jobs
st.markdown(
    f"""
    <h2 style="color: rgb(232, 192, 3); font-size: 20px;">
        Amount of Selected Jobs = {selected_df.shape[0]}
    </h2>
    """,
    unsafe_allow_html=True,
)
st.write(selected_df)

# download the selected data
csv = convert_df(selected_df)
st.download_button(
    label="Download selected data as CSV",
    data=csv,
    file_name=f"freelance_jobs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv",
    mime="text/csv",
)

# plot the geplaats door value counts for the selected job titles
# st.write(
#     px.bar(
#         selected_df["Geplaatst door"].value_counts().reset_index(),
#         x="count",
#         y="Geplaatst door",
#         title="Geplaatst door Value Counts for the Selected Job Titles",
#     )
# )
st.markdown("#### People/ companies who posted the selected job titles:")
st.markdown(
    f"""<p style="color: {single_color_palette[0]}">{", "
    .join(selected_df["Geplaatst door"].dropna().unique().tolist())}</p>""",
    unsafe_allow_html=True,
)

# plot the looptijd value counts for the selected job titles
st.write(
    px.bar(
        selected_df["Looptijd"]
        .value_counts()
        .reset_index()
        .sort_values(by="count", ascending=True),
        x="count",
        y="Looptijd",
        title="Looptijd Value Counts for the Selected Job Titles",
        color_discrete_sequence=single_color_palette,
    )
)

# plot the amount of jobs per job title
st.write(
    px.bar(
        selected_df["job_title"]
        .value_counts()
        .reset_index()
        .sort_values(by="count", ascending=True),
        x="count",
        y="job_title",
        title="Amount of Jobs per Job Title of Selected Job Titles",
        color_discrete_sequence=single_color_palette,
    )
)

# plot the amount of jobs posted per person
st.write(
    px.bar(
        selected_df["Geplaatst door"]
        .value_counts()
        .reset_index()
        .sort_values(by="count", ascending=True),
        x="count",
        y="Geplaatst door",
        title="Amount of Jobs Posted per Person of Selected Job Titles",
        color_discrete_sequence=single_color_palette,
    )
)

# plot the number of responses per job title
st.write(
    px.bar(
        selected_df.sort_values("Reacties", ascending=False).reset_index(),
        x="job_title",
        y="Reacties",
        color="Geplaatst door",
        title="Number of Responses per Job Title of Selected Job Titles",
    )
)

# plot the Aantal uur value counts for the selected job titles
st.write(
    px.bar(
        selected_df["Aantal uur"]
        .value_counts()
        .reset_index()
        .sort_values(by="count", ascending=True),
        x="count",
        y="Aantal uur",
        title="Aantal uur Value Counts for the Selected Job Titles",
        color_discrete_sequence=single_color_palette,
    )
)

# plot the Tarief value counts for the selected job titles
st.write(
    px.bar(
        selected_df["Tarief"]
        .value_counts()
        .reset_index()
        .sort_values(by="count", ascending=True),
        x="count",
        y="Tarief",
        title="Tarief Value Counts for the Selected Job Titles",
        color_discrete_sequence=single_color_palette,
    )
)

def convert_to_float_if_possible(x):
    try:
        return float(x)
    except:
        return np.nan

plot_df = (
    selected_df
    .loc[:, ["Tarief"]]
    .assign(
        **{
            "Lower Tarief": lambda x: x["Tarief"].str.extract("(\d+)", expand=True)[0].astype(float),
        }
    )
    .dropna()
    .assign(
        **{
            "Upper Tarief": lambda x: x["Tarief"].str.split(" ", expand=True)[2].apply(convert_to_float_if_possible),
        }
    )
    .loc[:, ["Lower Tarief", "Upper Tarief"]]
    .melt()
)

# plot the density plot of the upper and lower tarief
st.write(
    px.histogram(
        plot_df,
        x="value",
        color="variable",
        marginal="box",
        title="Density Plot of the Upper and Lower Tarief of the Selected Job Titles",
        color_discrete_sequence=double_color_palette,
        nbins=20,
    )
)

# plot the Contract value counts for the selected job titles
st.write(
    px.bar(
        selected_df["Contract"]
        .value_counts()
        .reset_index()
        .sort_values(by="count", ascending=True),
        x="count",
        y="Contract",
        title="Contract Value Counts for the Selected Job Titles",
        color_discrete_sequence=single_color_palette,
    )
)

# hide the streamlit style
hide_streamlit_style = """
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>
                        """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
