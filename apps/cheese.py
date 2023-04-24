# Import pandas and folium libraries
import pandas as pd
import folium
import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd


def app():

    st.title("Cheese Explorer")

    st.markdown(
        """
    Welcome to our interactive map showcasing the origin of a selection of cheeses from around the world!

    As you explore the map, you'll discover the birthplace of each cheese and a brief description of its unique characteristics.

    Let's start our journey in France, where the world-famous Brie cheese originated. This soft and creamy cheese has a mild flavor and pairs well with fruit and crackers.

    Moving on to Italy, we find the Parmigiano-Reggiano cheese, which is known for its hard texture and nutty flavor. This cheese is often grated over pasta dishes and soups to add a rich, savory taste.

    If you're a fan of blue cheese, then you'll be interested to learn that it was first created in Roquefort, a small village in France. Roquefort cheese is made from sheep's milk and has a distinctive blue mold that gives it its unique flavor.

    Heading over to the United Kingdom, we discover cheddar cheese, a popular cheese that originated in the village of Cheddar in Somerset. This cheese has a firm texture and a sharp, tangy flavor that becomes more intense as it ages.

    Finally, let's travel to the Netherlands, where Gouda cheese was first made. This cheese has a mild, nutty flavor and comes in various ages, from young and creamy to aged and crumbly.

    We hope you enjoy exploring the origins and characteristics of these cheeses on our interactive map. Don't forget to try some of these delicious cheeses the next time you're at the grocery store or your local cheese shop!

    """
    )



    # Read in data from a JSON file and select the 'attributes' column
    aw = pd.read_json('data/cheese_data.json')['attributes']

    # Normalize the JSON data into a flat table format
    desc = pd.json_normalize(aw)

    
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
            <p style="font-family: Verdana"> Type: {1} </p>
            <p style="font-family: Verdana"> Region: {2} </p>
            <p style="font-family: Verdana"> Description: {3} </p>
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
    m = get_map(desc, start_loc=[0, 0], zoom_start=1)
    
    #folium_static(m)

    # create a div element to hold the map
    map_div = st.empty()

    # display the map using folium_static
    folium_static(m)

    # use JavaScript to set the map's width to 100%
    map_div.write(
        """
        <script>
            document.getElementsByClassName('folium-map')[0].style.width = '100%';
        </script>
        """
    )

