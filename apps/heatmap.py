import streamlit as st
import leafmap.foliumap as leafmap
import folium
import geopandas as gpd
import numpy as np
import pandas as pd


def app():

    st.title("Visualiser")

    st.markdown(
        """
    This page can be used to visualise different geospatial indicators.

    """
    )

    raw = pd.read_json('cheese_data.json')['attributes']
    desc = pd.json_normalize(raw)

    m = folium.Map(location=(30, 10), zoom_start=3)

    for i,row in desc.iterrows():
        #Setup the content of the popup
        #iframe = folium.IFrame('Cheese:' + str(row["Cheese"])+'\n'+'Region:' + str(row["Region"])+'\n'+'Type:' + str(row["Type"])+'\n')
        html = ''' <h1 style="font-family: Verdana"> {0}</h1><br>
        <p style="font-family: Verdana"> Type: {1} </p>
        <p style="font-family: Verdana"> Region: {2} </p>
        <p style="font-family: Verdana"> Description: {3} </p>
        <br>
        <img src = {4}> '''.format(row['Cheese'], row['Type'], row['Region'], row['Text'],row['Photo_URL'])
        iframe = folium.IFrame(html=html, width=500, height=500)

        #Initialise the popup using the iframe
        popup = folium.Popup(iframe, min_width=500, max_width=500)
        
        #Add each row to the map
        folium.Marker(location=[row['lat'],row['long']],
                    popup = popup, c=row['Text']).add_to(map)
        
    m.to_streamlit(height=700)
