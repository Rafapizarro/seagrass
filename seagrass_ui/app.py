import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
from folium.plugins import Draw, MarkerCluster

st.set_page_config(layout="wide")
st.title("Seagrass in the Mediterranean Sea")

# Initialize session state
if 'locations' not in st.session_state:
    st.session_state.locations = []
if 'drawings' not in st.session_state:
    st.session_state.drawings = []

# Create sidebar
st.sidebar.title("Information Panel")

# Create map
m = folium.Map(location=[38.0, 15.6], zoom_start=5)

# Add existing markers
#for loc in st.session_state.locations:
#    folium.Marker(
#        [loc['lat'], loc['lng']],
#        popup=f"Lat: {loc['lat']:.4f}, Long: {loc['lng']:.4f}"
#    ).add_to(m)

# Add drawing tools
draw = Draw(
    export=False,
    position='topleft',
    draw_options={
        'polyline': False,
        'circlemarker': False,
        'polygon': True,
        'marker': True,
        'rectangle': True,
        'circle': False
    },
    edit_options={'poly': {'allowIntersection': False}}
)
draw.add_to(m)

# Display map with draw tools
map_data = st_folium(
    m,
    width=1000, height=600,
    returned_objects=["all_drawings", "last_clicked", "last_active_drawing"],
)

# Process map interactions
updated = False

# Handle clicks
if map_data["last_clicked"]:
    latitude = map_data["last_clicked"]["lat"]
    longitude = map_data["last_clicked"]["lng"]

    # Add to session state if not already there
    new_location = {'lat': latitude, 'lng': longitude}
    if new_location not in st.session_state.locations:
        st.session_state.locations.append(new_location)
        updated = True

# Handle drawn shapes
if "all_drawings" in map_data and map_data["all_drawings"]:
    st.session_state.drawings = map_data["all_drawings"]
    updated = True

# Display information in sidebar
#if st.session_state.locations:
#    st.sidebar.subheader("Selected Point")
#    last_location = st.session_state.locations[-1]
#    st.sidebar.write(f"Latitude: {last_location['lat']}")
#    st.sidebar.write(f"Longitude: {last_location['lng']}")
#    st.sidebar.write(f'Salinity: TO FILL IN')
#    st.sidebar.write(f'Seagrass: TO FILL IN')
#    st.sidebar.write(f'Temperature: TO FILL IN')

# Display drawn shapes
if st.session_state.drawings:
    st.sidebar.subheader("Drawn Shapes")
    for i, shape in enumerate(st.session_state.drawings):
        #st.sidebar.write(f"Shape infos {i+1}: {shape}")
        st.sidebar.write(f"Shape {i+1}: {shape['geometry']['type']}")
        if shape['geometry']['type'] == 'Point':
            coords = shape['geometry']['coordinates']
            st.sidebar.write(f"Longitude: {coords[0]}, Latitude: {coords[1]}")
        elif shape['geometry']['type'] == 'Polygon':
            # For polygons, display the first coordinate point
            coords = shape['geometry']['coordinates'][0]
            for i, point in enumerate(coords):
                st.sidebar.write(f"Point {i+1}: Longitude: {point[0]}, Latitude: {point[1]}")
            st.sidebar.write(f"Number of points: {len(shape['geometry']['coordinates'][0])}")
        st.sidebar.write(f'Salinity: TO FILL IN')
        st.sidebar.write(f'Seagrass: TO FILL IN')
        st.sidebar.write(f'Temperature: TO FILL IN')

# Rerun only if necessary
#if updated:
#    st.rerun()
