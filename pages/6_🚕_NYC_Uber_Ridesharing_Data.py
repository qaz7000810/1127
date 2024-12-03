# -*- coding: utf-8 -*-
# Copyright 2018-2022 Streamlit Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""An example of showing geographic data."""

import os
import numpy as np
import pandas as pd
import pydeck as pdk
import streamlit as st

# SETTING PAGE CONFIG TO WIDE MODE AND ADDING A TITLE AND FAVICON
st.set_page_config(layout="wide", page_title="NYC Ridesharing Demo", page_icon=":taxi:")

# LOAD DATA ONCE
@st.cache_resource
def load_data():
    path = "130001_public_wireless_lan_20240901.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/qaz7000810/tower/raw/refs/heads/main/130001_public_wireless_lan_20240901.csv"

    try:
        data = pd.read_csv(
            path,
            usecols=["緯度", "経度"],  # 只讀取需要的欄位
            encoding="utf-8"  # 指定編碼
        )
        st.write("Data loaded successfully")
        return data
    except Exception as e:
        st.write(f"Error loading data: {e}")
        return pd.DataFrame(columns=["緯度", "経度"])

# FUNCTION FOR MAP
def map(data, lat, lon, zoom):
    st.write(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state={
                "latitude": lat,
                "longitude": lon,
                "zoom": zoom,
                "pitch": 50,
            },
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=data,
                    get_position=["経度", "緯度"],
                    radius=100,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=True,
                    extruded=True,
                ),
            ],
        )
    )

# CALCULATE MIDPOINT FOR GIVEN SET OF DATA
@st.cache_data
def mpoint(lat, lon):
    return (np.average(lat), np.average(lon))

# STREAMLIT APP LAYOUT
data = load_data()

# LAYING OUT THE TOP SECTION OF THE APP
row1_1, row1_2 = st.columns((2, 3))

# SEE IF THERE'S A QUERY PARAM IN THE URL (e.g. ?pickup_hour=2)
# THIS ALLOWS YOU TO PASS A STATEFUL URL TO SOMEONE WITH A SPECIFIC HOUR SELECTED,
# E.G. https://share.streamlit.io/streamlit/demo-uber-nyc-pickups/main?pickup_hour=2
if not st.session_state.get("url_synced", False):
    try:
        pickup_hour = int(st.query_params["pickup_hour"])
        st.session_state["pickup_hour"] = pickup_hour
        st.session_state["url_synced"] = True
    except KeyError:
        pass

# IF THE SLIDER CHANGES, UPDATE THE QUERY PARAM
def update_query_params():
    hour_selected = st.session_state["pickup_hour"]
    st.query_params["pickup_hour"] = hour_selected

with row1_1:
    st.title("Public Wireless LAN Data")
    hour_selected = st.slider(
        "Select hour of pickup", 0, 23, key="pickup_hour", on_change=update_query_params
    )

with row1_2:
    st.write(
        """
    ##
    Examining how Public Wireless LAN Data varies over time.
    By sliding the slider on the left you can view different slices of time and explore different trends.
    """
    )

# LAYING OUT THE MIDDLE SECTION OF THE APP WITH THE MAPS
row2_1 = st.columns((1))

# SETTING THE ZOOM LOCATIONS
midpoint = mpoint(data["緯度"], data["経度"])

with row2_1:
    st.write(
        f"""**Public Wireless LAN Data from {hour_selected}:00 and {(hour_selected + 1) % 24}:00**"""
    )
    map(data, midpoint[0], midpoint[1], 11)
