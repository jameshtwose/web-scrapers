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

_ = load_dotenv(find_dotenv())

engine = create_engine(os.getenv("SPORTS_SCRAPER_POSTGRES_URL"))

# configure the page
st.set_page_config(
    page_title="Freelance Jobs Dashboard", page_icon=":sparkles:", layout="wide"
)

single_color_palette = ["#8f0fd4"]


@st.cache_data(ttl=3600)
def load_data():
    column_list = [
        "job_title",
        "Geplaatst door",
        "Publicatiedatum",
        "Startdatum",
        "Op locatie",
        "Looptijd",
        "Aantal uur",
        "Tarief",
        "Contract",
        "Reacties",
        "description",
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
                "Reacties": lambda x: x["Reacties"]
                .str.split(" ", expand=True)[0]
                .astype(int),
                "Geplaatst door": lambda x: x["Geplaatst door"].fillna("Onbekend"),
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
chosen_jobs = st.sidebar.multiselect(
    "Select a job title",
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
st.header("All Scraped Data")
st.write(df)

# plot the amount of jobs per Date
st.header("Amount of Jobs per Date")
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
selected_df = df.loc[lambda x: x["job_title"].isin(chosen_jobs), :]
st.header("Selected Job Title(s)")
st.write(selected_df)

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
        selected_df["Looptijd"].value_counts().reset_index(),
        x="count",
        y="Looptijd",
        title="Looptijd Value Counts for the Selected Job Titles",
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
        selected_df["Aantal uur"].value_counts().reset_index(),
        x="count",
        y="Aantal uur",
        title="Aantal uur Value Counts for the Selected Job Titles",
        color_discrete_sequence=single_color_palette,
    )
)

# plot the Tarief value counts for the selected job titles
st.write(
    px.bar(
        selected_df["Tarief"].value_counts().reset_index(),
        x="count",
        y="Tarief",
        title="Tarief Value Counts for the Selected Job Titles",
        color_discrete_sequence=single_color_palette,
    )
)

# plot the Contract value counts for the selected job titles
st.write(
    px.bar(
        selected_df["Contract"].value_counts().reset_index(),
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
