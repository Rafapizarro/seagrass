import streamlit as st
import folium
from streamlit_folium import st_folium
import numpy as np
import pandas as pd
from folium.plugins import Draw, MarkerCluster
import json
import os


from api import APIRequest
from pred_style.pred_color import get_pred_color, get_pred_opacity
from pred_style.pred_dim import get_pred_radius

CLASSES = ["Not reported", "Posidoniaceae", "Cymodoceaceae", "Hydrocharitaceae"]

if "prediction_points" not in st.session_state:
    st.session_state.prediction_points = []
if "locations" not in st.session_state:
    st.session_state.locations = []
if "drawings" not in st.session_state:
    st.session_state.drawings = []
if "needs_rerun" not in st.session_state:
    st.session_state.needs_rerun = False


def feed_predictions_state(predictions):
    if predictions:
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


@st.cache_data(ttl=3600)
def get_api_prediction(endpoint="", query=None):
    response = APIRequest().get(endpoint, query)
    return response["preds"]


st.set_page_config(layout="wide")
st.title("Seagrass in the Mediterranean Sea")

st.sidebar.title("Information Panel")

fig = folium.Figure()
m = folium.Map(location=[38, 16], zoom_start=4.4).add_to(fig)

if st.session_state.prediction_points:
    marker_cluster = MarkerCluster().add_to(m)

    new_predictions = st.session_state.prediction_points

    for idx, row in enumerate(new_predictions):
        targets_details = [
            f"<li>{CLASSES[idx]} : {(p / sum(row['targets'][1:])) * 100:.2f}%</li>"
            for idx, p in enumerate(row["targets"][1:])
        ]
        no_seagrass_pred = row["targets"][0]

        check_chlorophyll = (
            f"Chlorophyll: {row['features']['chlorophyll']:.2f}<br>"
            if row["features"]["chlorophyll"] is not None
            else "No chlorophyll data<br>"
        )

        seagrass_presence = (1 - no_seagrass_pred) * 100

        msgpopup = (
            f"Seagrass presence : {seagrass_presence:.2f}%<br><br>"
            if seagrass_presence >= 0.01
            else "Seagrass presence : >0.01%<br><br>"
        )
        msgpopup += f"Families :<br/><ul>{''.join(targets_details)}</ul>"
        msgpopup += (
            f"Characteristics :<br>Salinity: {row['features']['salinity']:.2f}<br>"
        )
        msgpopup += check_chlorophyll
        msgpopup += f"Depth: {row['features']['depth']:.2f}<br>"

        color = get_pred_color(row["targets"])
        opacity = get_pred_opacity(row["targets"])
        radius = get_pred_radius(row["targets"])

        folium.CircleMarker(
            location=[float(row["coordinates"][0]), float(row["coordinates"][1])],
            radius=5,
            popup=folium.Popup(
                f"<div style='width:200px'>{opacity}<br>Coordinates: {row['coordinates'][0]} {row['coordinates'][1]}<br><br> {msgpopup}</div>".format(
                    radius
                ),
                parse_html=False,
                max_width="100%",
            ),
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
        "polygon": False,
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

            if coords[0] and coords[1]:
                preds = get_api_prediction(
                    endpoint="point",
                    query={
                        "latitude": [coords[1]],
                        "longitude": [coords[0]],
                    },
                )
                if "error" in preds[0]:
                    st.sidebar.write(f"Error: {preds[0]['error']}")
                else:
                    feed_predictions_state(preds)

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

                if "error" in preds[0]:
                    st.sidebar.write(f"Error: {preds[0]['error']}")
                else:
                    feed_predictions_state(preds)

        st.sidebar.write(f"Salinity: TO FILL IN")
        st.sidebar.write(f"Seagrass: TO FILL IN")
        st.sidebar.write(f"Temperature: TO FILL IN")

if st.session_state.needs_rerun:
    st.session_state.needs_rerun = False
    st.experimental_rerun()
