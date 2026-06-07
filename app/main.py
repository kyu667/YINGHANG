import streamlit as st

st.set_page_config(page_title="银行营销数据分析与预测", page_icon="📊", layout="wide")

analysis_page = st.Page("pages/01_data_analysis.py", title="数据分析", icon="📊")
prediction_page = st.Page("pages/02_prediction.py", title="在线预测", icon="🔮")

pg = st.navigation({"功能导航": [analysis_page, prediction_page]})

pg.run()
