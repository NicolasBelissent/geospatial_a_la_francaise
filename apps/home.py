import streamlit as st
import leafmap.foliumap as leafmap
import folium


def app():
    st.title("Home")

    st.markdown(
        """
    Welcome to my Streamlit app! I built this app to gain a deeper understanding of Streamlit and geospatial data science.

    As a data scientist, I'm always looking for ways to improve my skills and learn new tools. Streamlit has quickly become a popular framework for building data-driven web applications, and I was excited to dive in and explore its capabilities.

    In this app, I've incorporated geospatial data to showcase how Streamlit can be used to create interactive maps that display information in a meaningful way. By experimenting with different visualizations and features, I hope to gain a better understanding of how to leverage Streamlit for geospatial data science projects. 
    """
    )
