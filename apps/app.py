import datetime

import databutton as db
import pandas as pd
import plotly.express as px
import streamlit as st
from lib.config import DATA_KEY


@db.streamlit("/heatmap", name="Heatmap")
def countries():
    st.set_page_config(
        page_title="Heatmap - News of the world",
        page_icon="🌍",
        layout="wide",
    )

    st.header("Heatmap showing countries mentioned in posts on /r/worldnews")

    st.markdown(
        """
        This project include a job which every 30 seconds gathers new posts from /r/worldnews which are sorted by new.
        The posts are then run through a model which outputs which countries are mentioned in the post.
        The result is a projection of the world where countries mentioned more frequently in reddit posts are 'hotter' and will stand out on the map.

        **Note:** As news from the US usually are posted in /r/news the US might be underrepresented here.
        """
    )

    df = db.dataframes.get(DATA_KEY)

    # Fetch posts scraped from reddit within the previous 24 hours
    df = df[df.scraped_at > datetime.datetime.now() - pd.to_timedelta("24hour")]

    grouped_posts_by_country_df = (
        df.groupby(["country_name", "country_code", "country_flag"], as_index=False)
        .size()
        .sort_values(by="size", ascending=False)
    )

    # Created heatmap of posts per country previous 24 hours
    # https://plotly.github.io/plotly.py-docs/generated/plotly.express.choropleth.html
    fig = px.choropleth(
        data_frame=grouped_posts_by_country_df,
        locations="country_name",
        color="size",
        scope="world",
        locationmode="country names",
        hover_name="country_name",
        hover_data={"country_name": True, "country_code": False, "size": True, "country_flag": True},
        color_continuous_scale=["#fff", "#2B0085"],
        projection="orthographic",
        height=800,
    )

    fig.update_geos(showcountries=True)

    # Plot heatmap in the streamlit app
    st.plotly_chart(fig, use_container_width=True)

    most_frequent_countries = grouped_posts_by_country_df["country_code"][:3]

    posts_from_most_frequent_countries = df[df["country_code"].isin(most_frequent_countries)].sort_values(
        by="scraped_at", ascending=False
    )[:10]

    rows = []
    for _, row in posts_from_most_frequent_countries.iterrows():
        rows.append(
            f"""
                {"{:.2%}".format(row.score)} {row.country_flag} <= [{row.title}]({row.url})
            """
        )

    st.header("Ten latest posts from the countries mentioned most frequently")

    st.markdown(
        """
        The list shows the post gathered from reddit and corresponding model outcome, here represented by a percentage and a flag.
        """
    )
    st.markdown("\n".join(rows))
