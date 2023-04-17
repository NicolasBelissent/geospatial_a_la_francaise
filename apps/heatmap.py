import streamlit as st
import leafmap.foliumap as leafmap
import folium
import geopandas as gpd
import numpy as np


def app():

    st.title("Visualiser")

    st.markdown(
        """
    This page can be used to visualise different geospatial indicators.

    """
    )

    # filepath = "https://raw.githubusercontent.com/giswqs/leafmap/master/examples/data/us_cities.csv"
    # m = leafmap.Map(tiles="stamentoner")
    # m.add_heatmap(
    #     filepath,
    #     latitude="latitude",
    #     longitude="longitude",
    #     value="pop_max",
    #     name="Heat map",
    #     radius=20,
    # )

    
    # m.to_streamlit(height=700)


        
    # # Load shapefile using geopandas
    # gdf = gpd.read_file("cheese.shp")

    # # Create a random value for each country
    # values = np.random.rand(len(gdf))

    political_countries_url = (
        "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
    )

    m = folium.Map(location=(30, 10), zoom_start=3, tiles="cartodb positron")
    folium.GeoJson(political_countries_url).add_to(m)

    m.save("footprint.html")

    # # Add a choropleth layer to the map
    # folium.Choropleth(
    #     geo_data=gdf,
    #     data=gdf,
    #     columns=["iso_a3", values],
    #     key_on="feature.properties.iso_a3",
    #     fill_color="YlOrRd",
    #     fill_opacity=0.7,
    #     line_opacity=0.2,
    #     legend_name="Random Values"
    # ).add_to(m)

    # Display the map in Streamlit using the folium_static method
    m.to_streamlit(height=700)
