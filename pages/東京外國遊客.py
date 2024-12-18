import streamlit as st
import pandas as pd
import chardet

# 定義 CSV 文件的 URL
csv_url = 'https://github.com/qaz7000810/tower/raw/refs/heads/main/%E8%A7%80%E5%85%89%E5%AE%A2%E6%80%A7%E5%88%A5.csv'

# 讀取 CSV 文件
@st.cache_data
def load_data(url):
    # 自動檢測編碼
    with open(url, 'rb') as file:
        result = chardet.detect(file.read())
    encoding = result['encoding']
    
    # 使用檢測到的編碼來讀取 CSV 文件
    data = pd.read_csv(url, encoding=encoding)
    return data

data = load_data(csv_url)

# 設置標題
st.title('行為特徵調查數據')

# 顯示數據表格
st.dataframe(data)
