## Geospatial a la Francaise: A Frenchman's take on geospatial data science.

This is a Streamlit web application that displays different geospatial data visualizations. The app consists of two pages:

1. A page to visualize the origin of different cheeses worldwide, using the Folium package in Python.
2. A page to visualize statistics about wine production and consumption across Europe, using Geopandas and GeoPackage data.

### Setup and Installation

To run this web app locally, follow these steps:

1. Clone the repository to your local machine.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the app using `streamlit run app.py`.
4. The app will open in your browser at `localhost:8501`.

### Cheese Visualization Page

The Cheese Visualization page displays a world map with markers for the origin of different cheeses. The user can select a cheese type from a dropdown menu to see the specific location where it originated. The map is created using the Folium package in Python.

![image](https://user-images.githubusercontent.com/34235544/233347779-028d6320-ed0d-4a0d-bcbd-7b74b3b11815.png)

### Wine Statistics Page

The Wine Statistics page displays a choropleth map of Europe, showing wine production and consumption statistics by country. The user can select whether to view production or consumption data using a radio button. The map is created using Geopandas and GeoPackage data.

![image](https://user-images.githubusercontent.com/34235544/233404515-d8679d1f-04c7-4a68-8edf-17c0cf36bba7.png)

### Data Sources

The cheese origin data was sourced from ArcGIS: https://www.arcgis.com/home/item.html?id=52636e04c969420fb4f68cf74caa7281

The wine production and consumption data was sourced from the International Orgainsation of Vine and Wine: https://www.oiv.int/what-we-do/data-discovery-report?oiv

### Contact Information

If you have any questions or issues with the web app, please contact the developer at nicolas.belissent@gmail.com.
