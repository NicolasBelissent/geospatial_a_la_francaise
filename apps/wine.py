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

    gt_polygons = gpd.read_file("EU_PDO.gpkg")

    labels_df = pd.read_csv('PDO_EU_id.csv')

    joined = gt_polygons.merge( labels_df, on = 'PDOid')

    #create a smaller version of the merged dataset to narrow down on parameters i want to visualise

    select_df = joined.loc[:, ['PDOnam', 'Category_of_wine_product', 'geometry']]
    select_df = select_df.rename(columns={'PDOnam': 'Wine name', 'Category_of_wine_product':'Wine Category'})

    # now seeing if i can overlay country data
    wine_country_df = pd.read_csv('wine_country_data.csv')
    wine_country_df = wine_country_df.rename(columns={'Region/Country': 'country'})
    wine_country_df = wine_country_df.drop(['Continent', 'Product'], axis=1)

    # test_df = (wine_country_df[wine_country_df['country'] == 'Austria'])
    # more = test_df.loc[:, ['Variable', 'Unit', 'Quantity']].transpose().reset_index()
    # more = more.drop(['index'], axis=1)
    # more
    # more.columns = more.iloc[0]
    # more.iloc[2:]

    def reshape_dataframe(df):

        new_df = pd.DataFrame(columns = ['country', 'Surface Area' , 'Exports' , 'Imports' , 'Production'])
        
        for i,c in enumerate(pd.unique(df['country'])):
            #select country specific
            cdf = (wine_country_df[wine_country_df['country'] == c])
            
            # extract dat afrom this view and create a new row 
            mod = cdf.loc[:, ['Variable', 'Unit', 'Quantity']].transpose().reset_index()
            mod = mod.drop(['index'], axis=1)
            mod.columns = mod.iloc[0]
            mod = mod.drop([0,1])
            mod['country'] = c

            new_df = pd.concat([new_df,mod])#~,how='inner')#,on=list(mod.columns))

        return new_df

    wine_country_df = reshape_dataframe(wine_country_df)

    # adding units
    wine_country_df['Surface Area'] = wine_country_df['Surface Area'].apply(lambda x: str(x) + ' ha' if x is not None else None)
    wine_country_df['Exports'] = wine_country_df['Exports'].apply(lambda x: str(x) + ' 1000 hl' if x is not None else None)
    wine_country_df['Imports'] = wine_country_df['Imports'].apply(lambda x: str(x) + ' 1000 hl' if x is not None else None)
    wine_country_df['Production'] = wine_country_df['Production'].apply(lambda x: str(x) + ' 1000 hl' if x is not None else None)


    # get acces to the geocoords of european countries
    euro_cords_df = pd.read_csv('world_country_and_usa_states_latitude_and_longitude_values.csv')

    wine_info_loc_df = wine_country_df.merge(euro_cords_df, on='country')
    wine_info_loc_df = wine_info_loc_df.drop(['usa_state_longitude', 'usa_state_latitude', 'usa_state_code', 'usa_state'], axis=1)
    wine_info_geo_df = gpd.GeoDataFrame(wine_info_loc_df, geometry=gpd.points_from_xy(wine_info_loc_df.longitude, wine_info_loc_df.latitude))


    m = select_df.explore(column = 'Wine name',popup=True, legend=False)
    m = wine_info_geo_df.explore(m=m)    
    folium.LayerControl().add_to(m)  # use folium to add layer control
    folium_static(m)  # show map
