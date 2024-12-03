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
        # 先讀取整個 CSV 文件
        data = pd.read_csv(
            path,
            encoding="iso-8859-1"  # 指定編碼
        )
        st.write("Data loaded successfully")
        st.write("Columns in the dataset:", data.columns.tolist())  # 顯示數據集中的列名稱
        return data
    except Exception as e:
        st.write(f"Error loading data: {e}")
        return pd.DataFrame()

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
