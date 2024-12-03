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
st.set_page_config(layout="wide", page_title="Public Wireless LAN Data", page_icon=":globe_with_meridians:")

# LOAD DATA ONCE
@st.cache_resource
def load_data():
    path = "130001_public_wireless_lan_20240901.csv"
    if not os.path.isfile(path):
        path = f"https://github.com/qaz7000810/tower/raw/refs/heads/main/130001_public_wireless_lan_20240901.csv"

    try:
        data = pd.read_csv(
            path,
            usecols=[2, 3],  # 使用列索引來讀取第三和第四列
            encoding="iso-8859-1"  # 指定編碼
        )
        data.columns = ["緯度", "経度"]  # 手動指定列名
        data["緯度"] = pd.to_numeric(data["緯度"], errors='coerce')  # 將緯度轉換為數字
        data["経度"] = pd.to_numeric(data["経度"], errors='coerce')  # 將経度轉換為數字
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

# SETTING THE ZOOM LOCATIONS
if not data.empty:
    midpoint = mpoint(data["緯度"], data["経度"])

    # DISPLAY THE MAP
    st.title("Public Wireless LAN Data")
    st.write(
        """
        Examining the geographic distribution of Public Wireless LAN Data.
        """
    )
    map(data, midpoint[0], midpoint[1], 11)
