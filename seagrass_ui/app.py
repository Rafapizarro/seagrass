import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
from folium.plugins import Draw, MarkerCluster
<<<<<<< HEAD
import json
import os

from seagrass_ui.api import APIRequest
from seagrass_ui.pred_style.pred_color import get_pred_color, get_pred_opacity
from seagrass_ui.pred_style.pred_dim import get_pred_radius

mocked_data = [
    {
        "coordinates": [41.8125, 4.2083],
        "targets": [0.1, 0.2, 0.3, 0.2, 0.2],
    },
    {
        "coordinates": [41.7708, 4.2083],
        "targets": [0.1, 0.1, 0.25, 0.25, 0.3],
    },
    {
        "coordinates": [41.8542, 4.2083],
        "targets": [0.4, 0.2, 0.1, 0.2, 0.1],
    },
    {
        "coordinates": [41.9375, 4.2083],
        "targets": [
            0.0949656128883362,
            0.9012578460155054927,
            0.0012579282047227025,
            0.0012594683794304729,
            0.0012590594124048948,
        ],
    },
    {
        "coordinates": [41.9792, 4.2083],
        "targets": [
            0.0949656128883362,
            0.0012578460155054927,
            0.0012579282047227025,
            0.9012594683794304729,
            0.0012590594124048948,
        ],
    },
    {
        "coordinates": [42.0208, 4.2083],
        "targets": [
            0.9949656128883362,
            0.0012578460155054927,
            0.0012579282047227025,
            0.0012594683794304729,
            0.0012590594124048948,
        ],
    },
]


@st.cache_data(ttl=3600)
def get_api_prediction(endpoint="", query=None):
    response = APIRequest().get(endpoint, query)
    return response["preds"]
    #return mocked_data


if "prediction_points" not in st.session_state:
    st.session_state.prediction_points = []
if "locations" not in st.session_state:
    st.session_state.locations = []
if "drawings" not in st.session_state:
    st.session_state.drawings = []
if "needs_rerun" not in st.session_state:
    st.session_state.needs_rerun = False
=======
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b

st.set_page_config(layout="wide")
st.title("Seagrass in the Mediterranean Sea")

<<<<<<< HEAD
st.sidebar.title("Information Panel")

fig = folium.Figure()
m = folium.Map(location=[38, 16], zoom_start=4.4).add_to(fig)

if st.session_state.prediction_points:
    marker_cluster = MarkerCluster().add_to(m)

    new_predictions = st.session_state.prediction_points

    for idx, row in enumerate(new_predictions):
        targets_details = [f"{p:.2f}" for p in row["targets"]]
        msgpopup = f"Prediction: {'-'.join(targets_details)}"

        # prediction_value = row["targets"][0]
        # color = "green" if prediction_value > 0.5 else "red"
        color = get_pred_color(row["targets"])
        opacity = get_pred_opacity(row["targets"])
        radius = get_pred_radius(row["targets"])

        folium.CircleMarker(
            location=[float(row["coordinates"][0]), float(row["coordinates"][1])],
            radius=5,
            popup=f"Coordinates: {row['coordinates']} <br> {msgpopup}".format(radius),
            weight=1,
            fill_color=color,
            fill=False,
            opacity=opacity,
            fill_opacity=opacity,
        ).add_to(m)


draw = Draw(
    export=False,
    position="topleft",
    draw_options={
        "polyline": False,
        "circlemarker": False,
        "polygon": True,
        "marker": True,
        "rectangle": True,
        "circle": False,
    },
    edit_options={"poly": {"allowIntersection": False}},
)
draw.add_to(m)

map_data = st_folium(
    fig,
    width=1000,
    height=600,
    returned_objects=["all_drawings", "last_clicked", "last_active_drawing"],
)

new_drawings = False
if "all_drawings" in map_data and map_data["all_drawings"]:
    if map_data["all_drawings"] != st.session_state.drawings:
        st.session_state.drawings = map_data["all_drawings"]
        new_drawings = True

selected_points = [[], []]
if st.session_state.drawings:
    st.sidebar.subheader("Drawn Shapes")

    for i, shape in enumerate(st.session_state.drawings):
        st.sidebar.write(f"Shape {i + 1}: {shape['geometry']['type']}")

        if shape["geometry"]["type"] == "Point":
            coords = shape["geometry"]["coordinates"]
            st.sidebar.write(f"Longitude: {coords[0]}, Latitude: {coords[1]}")

        elif shape["geometry"]["type"] == "Polygon" and new_drawings:
            coords = shape["geometry"]["coordinates"][0]
            for j, point in enumerate(coords):
                st.sidebar.write(
                    f"Point {j + 1}: Longitude: {point[0]}, Latitude: {point[1]}"
                )
                selected_points[0].append(point[0])
                selected_points[1].append(point[1])

            st.sidebar.write(f"Number of points: {len(coords)}")

            if selected_points[0] and selected_points[1]:
                preds = get_api_prediction(
                    endpoint="predict",
                    query={
                        "latitudes": [min(selected_points[1]), max(selected_points[1])],
                        "longitudes": [
                            min(selected_points[0]),
                            max(selected_points[0]),
                        ],
                    },
                )

                if preds:
                    existing_coords = {
                        (p["coordinates"][0], p["coordinates"][1])
                        for p in st.session_state.prediction_points
                    }

                    has_new_predictions = False
                    for p in preds:
                        if (
                            p["coordinates"][0],
                            p["coordinates"][1],
                        ) not in existing_coords:
                            st.session_state.prediction_points.append(p)
                            has_new_predictions = True

                    if has_new_predictions:
                        st.session_state.needs_rerun = True

        st.sidebar.write(f"Salinity: TO FILL IN")
        st.sidebar.write(f"Seagrass: TO FILL IN")
        st.sidebar.write(f"Temperature: TO FILL IN")

if st.session_state.needs_rerun:
    st.session_state.needs_rerun = False
    st.experimental_rerun()
=======
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
>>>>>>> 18dbd0ae0e921d8370ea73d4380007ece1d3e54b
