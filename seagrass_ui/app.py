import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
#from shapely.geometry import Point, Polygon

latitude= None
longitude = None
# Add at the beginning of your script
if 'locations' not in st.session_state:
    st.session_state.locations = []

m = folium.Map(location=[38.0, 15.6], zoom_start=5)

# Add all existing markers
for loc in st.session_state.locations:
    st.write(loc['lat'],loc['lng'])
    folium.Marker(
        (loc['lat'], loc['lng']),
        popup=f"Lat: {loc['lat']:.4f}, Long: {loc['lng']:.4f}",
        tooltip=f"Lat: {loc['lat']:.4f}, Long: {loc['lng']:.4f}"
    ).add_to(m)

st.title("Seagrass in the Mediterranean Sea")
map_data = st_folium(
        m,
        width=1000, height=600,
        returned_objects=["last_clicked"],
    )

if map_data["last_clicked"]:
    latitude = map_data["last_clicked"]["lat"]
    longitude = map_data["last_clicked"]["lng"]

    # Save the new location to session state
    st.session_state.locations =[{
        'lat': latitude,
        'lng': longitude
    }]
    st.rerun()



if  st.session_state.locations:
    st.write(st.session_state.locations[0])
    # Display the coordinates in the sidebar
    st.sidebar.subheader("Selected Location")
    st.sidebar.write(f"Latitude: {st.session_state.locations[0].get('lat')}")
    st.sidebar.write(f"Longitude: {st.session_state.locations[0].get('lng')}")
    st.sidebar.write(f'Salinity: TO FILL IN')
    st.sidebar.write(f'Seagrass: TO FILL IN')
    st.sidebar.write(f'Temperature: TO FILL IN')

        # Force a rerun to show the new marker


#def seagrass_prediction(latitude, longitude):
    #return #TO ADD
