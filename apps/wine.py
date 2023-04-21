import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd




def app():

    st.title("Wine Worldwide")

    st.markdown(
        """
    """
    )

    # load preprocessed data
    choropleth_df = gpd.read_file("data/wine_choropleth_smaller.gpkg")
    markers_df = gpd.read_file("data/wine_markers.gpkg")
    
    # Create a choropleth map with Wine name column, popups and legend turned off, and name set to 'Wine Varieties'
    m = choropleth_df.explore(column='Wine name', popup=True, legend=False, name='Wine Varieties')

    # Create a FeatureGroup for the markers
    fg = folium.FeatureGroup(name='Country-level statistics')

    # Add markers to FeatureGroup
    for index, row in markers_df.iterrows():
        # Create a CircleMarker and add it to the FeatureGroup
        marker = folium.CircleMarker(location=[row.geometry.y, row.geometry.x], 
                                    radius=row['FactValueNumeric']*8, 
                                    fill=True,
                                    fill_color='red',
                                    fill_opacity=0.4,
                                    color=None)
        
        # Create HTML for popup
        html = ''' <h1 style="font-family: Verdana"> {0}</h1><br>
        <p style="font-family: Verdana"> Total consumption (l of pure alcohol): {1} </p>
        <p style="font-family: Verdana"> Vineyard Surface Area (hectares): {2} </p>
        <p style="font-family: Verdana"> Total imported (1000 hl): {3} </p>
        <p style="font-family: Verdana"> Total exported (1000 hl): {4} </p>
        <p style="font-family: Verdana"> Total production (1000 hl): {5} </p>'''.format(row['country'], row['FactValueNumeric'], row['Surface Area'], row['Imports'],row['Exports'],row['Production'])
        
        # Create an iframe for the popup
        iframe = folium.IFrame(html=html, width=400, height=300)
        
        # Add the popup to the marker
        popup = folium.Popup(iframe, max_width=400)
        marker.add_child(popup)
        
        # Add the marker to the FeatureGroup
        fg.add_child(marker)

    # Add the FeatureGroup to the map
    m.add_child(fg)

    # Add a layer control to the map
    folium.LayerControl().add_to(m)

    folium_static(m)  # show the map
