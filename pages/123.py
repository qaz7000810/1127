import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

st.set_page_config(layout="wide")

markdown = """
A Streamlit map template
<https://github.com/opengeos/streamlit-map-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

st.title("Marker Cluster")

# 讀取 CSV 檔案並轉換為 DataFrame
views = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E6%9D%B1%E4%BA%AC%E6%99%AF%E9%BB%9E.csv")
heat_data = pd.read_csv("https://raw.githubusercontent.com/lztzm/Gis_Final_Project/refs/heads/main/%E5%90%84%E5%8D%80%E6%99%AF%E9%BB%9E%E6%95%B8%E9%87%8F.csv")

# 確保緯度與經度欄位存在
if '緯度' not in views.columns or '經度' not in views.columns:
    st.error("CSV檔案中缺少緯度或經度欄位！")
else:
    # 獲取所有的行政區
    districts = views['市町村名'].unique()
    
    # 添加選擇行政區的 selectbox
    selected_district = st.sidebar.selectbox('選擇行政區', districts)
    
    # 根據選擇的行政區過濾景點資料
    filtered_views = views[views['市町村名'] == selected_district]

    # 初始化地圖
    m = leafmap.Map(center=[35.68388267239132, 139.77317043877568], zoom=12)

    # 添加點標記
    m.add_points_from_xy(
        filtered_views,
        x="經度",
        y="緯度",
        spin=True,
        add_legend=True,
    )

    # 添加熱區地圖
    heatmap_layer = leafmap.folium.FeatureGroup(name="熱區地圖")
    m.add_heatmap(
        heat_data,
        latitude="緯度",
        longitude="經度",
        value="景點數量",
        name="Heat map",
        radius=20,
    )

    # 新增圖層控制
    leafmap.folium.LayerControl().add_to(m)

    # 顯示地圖
    m.to_streamlit(height=700)