import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd




def app():

    st.title("Wines of Europe")

    st.markdown(
        """
        It wouldn't be a frenchman's approach to geospatial data science without working with wine data. This page allows you to explore two european wine datasets, overlayed on the same map.

        1. The first layer is a choropleth labelled 'Wine varieties'. It uses data provided by the [geospatial inventory of regulatory information for wine Protected Designations of Origin in Europe](https://springernature.figshare.com/collections/A_geospatial_inventory_of_regulatory_information_for_wine_Protected_Designations_of_Origin_in_Europe/5877659/1). This data provides a geopackage file in which is stored different european wine regions along with the names of the wine that these regions produce.
        2. The second layer is a bubble map labelled 'Country-level statistics'. It uses a combination of [OIV](https://www.oiv.int/what-we-do/data-discovery-report?oiv) data, [WHO wine consumption data](https://www.who.int/data/gho/data/indicators/indicator-details/GHO/alcohol-recorded-per-capita-(15-)-consumption-(in-litres-of-pure-alcohol)) and general european countruy level [geolocation data](https://www.kaggle.com/datasets/paultimothymooney/latitude-and-longitude-for-every-country-and-state?resource=download). The layer consists of country level bubbles, scaled by wine consumption. When clicked these bubbles give more country specific information on Import/Export, Production and Vineyard Surce Area. 
        
        The map is built using a mixture of pandas, geopandas and folium. Data processing was done prior to uploading to the Streamlit cloud. Code will be available on [Github](https://github.com/NicolasBelissent/geospatial_a_la_francaise).

        **Disclaimer:** The visualisation make take some time to render; more than the first map. Enough time to crack a bottle and serve yourself a glass (or 2).
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
    for _, row in markers_df.iterrows():
        # Create a CircleMarker and add it to the FeatureGroup
        marker = folium.CircleMarker(location=[row.geometry.y, row.geometry.x], 
                                    radius=row['FactValueNumeric']*10, 
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

    folium_static(m, width=1000, height=500)  # show the map
