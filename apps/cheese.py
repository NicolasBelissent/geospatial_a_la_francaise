# Import pandas and folium libraries
import streamlit as st
from streamlit_folium import folium_static
import folium
import pandas as pd


def app():

    st.title("Cheese Explorer")

    st.markdown(
        """
    The first part of this app/tool is a cheese visualisation tool. Like any good frenchman, I am passionate aboute about cheese - smelly, soft or textured. 
    
    This visualisation allows you to explore a selection of cheese varieties from across the globe. For every cheese, I've provided a information on the origin of the cheese, milk type, flavour and in some cases, a picture.
    
    The app uses the [Cheeses of the World](https://www.arcgis.com/home/item.html?id=52636e04c969420fb4f68cf74caa7281) dataset provided by ArcGIS. The map is built uses the **folium** python package. Code will be available on [Github](https://github.com/NicolasBelissent/geospatial_a_la_francaise). 

    **Disclaimer:** The visualisation make take some time to render. Enough time to grab a slice of cheese and some bread.
    """
    )



    # Read in data from a JSON file and select the 'attributes' column
    raw = pd.read_json('data/cheese_data.json')['attributes']

    # Normalize the JSON data into a flat table format
    cheese_df = pd.json_normalize(raw)

    
    # Define function to create the map
    def get_map(data, start_loc, zoom_start=3):
        
        # Create a new map object with starting location and zoom level
        map = folium.Map(start_loc=start_loc, zoom_start=zoom_start, width='100%')
    
        # Adding a custom icon for the marker
        icon_url = 'data/cheese_marker.png'

        # Iterate over each row of data
        for _, row in data.iterrows():
            
            # Define HTML content for popup
            html = ''' <h1 style="font-family: Verdana"> {0}</h1><br>
            <p style="font-family: Verdana";font-size: 12px> Type: {1} </p>
            <p style="font-family: Verdana";font-size: 12px> Region: {2} </p>
            <p style="font-family: Verdana";font-size: 12px> Description: {3} </p>
            <br>
            <img src = {4}> '''.format(row['Cheese'], row['Type'], row['Region'], row['Text'],row['Photo_URL'])
            
            # Create an iframe with the HTML content
            iframe = folium.IFrame(html=html, width=500, height=500)

            # Initialize the popup using the iframe
            popup = folium.Popup(iframe, min_width=500, max_width=500)
            
            # Load the custom icon
            icon = folium.features.CustomIcon(icon_url, icon_size=(25, 25))

            #Add each row to the map
            folium.Marker(location=[row['lat'],row['long']], icon=icon, popup = popup, c=row['Text']).add_to(map)
        
        # Return the completed map object
        return map

    # Define the starting location and zoom level, and render the map
    m = get_map(cheese_df, start_loc=[0, 0], zoom_start=1)
    
    folium_static(m, width=1000, height=500)