import streamlit as st
import leafmap.foliumap as leafmap
import folium


def app():
    st.title("Home")

    st.markdown(
        """
    A [streamlit](https://streamlit.io) app template for geospatial applications based on [streamlit-option-menu](https://github.com/victoryhb/streamlit-option-menu). 
    To create a direct link to a pre-selected menu, add `?page=<app name>` to the URL, e.g., `?page=upload`.
    https://share.streamlit.io/giswqs/streamlit-template?page=upload

    """
    )

    # import folium

    # political_countries_url = (
    #     "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    # )

    # m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    # folium.GeoJson(political_countries_url).add_to(m)

    # m.save("footprint.html")

    # # m = leafmap.Map(locate_control=True)
    # # m.add_basemap("ROADMAP")
    # m.to_streamlit(height=700)
