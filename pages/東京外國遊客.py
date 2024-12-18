import streamlit as st
import pandas as pd

# 定義 CSV 文件的 URL
csv_url = 'https://www.opendata.metro.tokyo.lg.jp/sangyouroudou/behavioral_characteristics_survey/H31R1behavioral_characteristics_survey1.csv'

# 讀取 CSV 文件
@st.cache_data
def load_data(url):
    data = pd.read_csv(url, encoding='shift_jis')  # 使用正確的編碼來讀取 CSV 文件
    return data

data = load_data(csv_url)

# 設置標題
st.title('行為特徵調查數據')

# 顯示數據表格
st.dataframe(data)
