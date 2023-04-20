import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium_static
import folium
import geopandas as gpd
import numpy as np
import pandas as pd


def reshape_dataframe(df):
    
    # create an empty DataFrame with the desired columns
    new_df = pd.DataFrame(columns = ['country', 'Surface Area' , 'Exports' , 'Imports' , 'Production'])
    
    # loop through each unique country in the 'country' column of the input DataFrame
    for i,c in enumerate(pd.unique(df['country'])):
        
        # select data for the current country
        cdf = (df[df['country'] == c])
        
        # transpose the data and convert the first row to column names
        mod = cdf.loc[:, ['Variable', 'Unit', 'Quantity']].transpose().reset_index()
        mod = mod.drop(['index'], axis=1)
        mod.columns = mod.iloc[0]
        mod = mod.drop([0,1])
        
        # add a 'country' column to the transposed data and set it to the current country name
        mod['country'] = c

        # concatenate the transposed data with the existing DataFrame
        new_df = pd.concat([new_df,mod])
    
    # return the reshaped DataFrame
    return new_df


def app():

    st.title("Wine Worldwide")

    st.markdown(
        """
    """
    )
    # load geospatial data from a Geopackage file and wine data from a csv file
    gt_polygons = gpd.read_file("data/EU_PDO.gpkg")
    labels_df = pd.read_csv('data/PDO_EU_id.csv')

    # merge the two datasets on a common column 'PDOid'
    joined = gt_polygons.merge(labels_df, on='PDOid')

    # create a new DataFrame by selecting only the desired columns from the merged dataset and renaming them
    select_df = joined.loc[:, ['PDOnam', 'Category_of_wine_product', 'geometry']]
    select_df = select_df.rename(columns={'PDOnam': 'Wine name', 'Category_of_wine_product':'Wine Category'})

    # load wine country data from a csv file, reshape it and convert the units of certain columns
    wine_country_df = pd.read_csv('wine_country_data.csv')
    wine_country_df = wine_country_df.rename(columns={'Region/Country': 'country'})
    wine_country_df = wine_country_df.drop(['Continent', 'Product'], axis=1)
    wine_country_df = reshape_dataframe(wine_country_df)
    wine_country_df['Surface Area'] = wine_country_df['Surface Area'].apply(lambda x: str(x) + ' ha' if x is not None else None)
    wine_country_df['Exports'] = wine_country_df['Exports'].apply(lambda x: str(x) + ' 1000 hl' if x is not None else None)
    wine_country_df['Imports'] = wine_country_df['Imports'].apply(lambda x: str(x) + ' 1000 hl' if x is not None else None)
    wine_country_df['Production'] = wine_country_df['Production'].apply(lambda x: str(x) + ' 1000 hl' if x is not None else None)

    # load a DataFrame containing geocoordinates of European countries from a csv file
    euro_cords_df = pd.read_csv('data/world_country_and_usa_states_latitude_and_longitude_values.csv')

    # merge the wine country data with the coordinates DataFrame
    wine_info_loc_df = wine_country_df.merge(euro_cords_df, on='country')
    wine_info_loc_df = wine_info_loc_df.drop(['usa_state_longitude', 'usa_state_latitude', 'usa_state_code', 'usa_state'], axis=1)
    wine_info_geo_df = gpd.GeoDataFrame(wine_info_loc_df, geometry=gpd.points_from_xy(wine_info_loc_df.longitude, wine_info_loc_df.latitude))

    # use Folium to create an interactive map and add layers to it
    m = select_df.explore(column='Wine name', popup=True, legend=False)  # add the wine name layer to the map
    m = wine_info_geo_df.explore(m=m)  # add the wine country information layer to the map
    folium.LayerControl().add_to(m)  # add a layer control to the map
    folium_static(m)  # show the map
