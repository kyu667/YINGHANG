import streamlit as st

from app.models.data_loader import load_train_data
from app.models.visualizer import (
    plot_age_distribution,
    plot_contact_subscription,
    plot_education_marital_heatmap,
    plot_job_subscription_rate,
    plot_month_subscription,
    plot_subscription_pie,
)

st.title("📊 数据分析")
st.markdown("探索银行营销数据,理解客户特征分布与认购行为规律。")

df = load_train_data()

# overview metrics
st.subheader("数据概览")
total = len(df)
sub_rate = (df["subscribe"] == "yes").mean() * 100
avg_age = df["age"].mean()
job_count = df["job"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("总记录数", f"{total:,}")
col2.metric("认购率", f"{sub_rate:.1f}%")
col3.metric("平均年龄", f"{avg_age:.0f}")
col4.metric("职业种类", str(job_count))

st.divider()

# filter sidebar
st.sidebar.header("筛选条件")
all_jobs = ["全部"] + sorted(df["job"].dropna().unique().tolist())
selected_job = st.sidebar.selectbox("职业", all_jobs)
all_marital = ["全部"] + sorted(df["marital"].dropna().unique().tolist())
selected_marital = st.sidebar.selectbox("婚姻状况", all_marital)
all_education = ["全部"] + sorted(df["education"].dropna().unique().tolist())
selected_education = st.sidebar.selectbox("教育水平", all_education)

filtered = df.copy()
if selected_job != "全部":
    filtered = filtered[filtered["job"] == selected_job]
if selected_marital != "全部":
    filtered = filtered[filtered["marital"] == selected_marital]
if selected_education != "全部":
    filtered = filtered[filtered["education"] == selected_education]
st.sidebar.caption(f"筛选后记录数: {len(filtered):,}")

# charts
col_left, col_right = st.columns(2)
with col_left:
    st.plotly_chart(plot_subscription_pie(filtered), use_container_width=True)
with col_right:
    st.plotly_chart(plot_age_distribution(filtered), use_container_width=True)

st.plotly_chart(plot_job_subscription_rate(filtered), use_container_width=True)

col_a, col_b = st.columns(2)
with col_a:
    st.plotly_chart(plot_education_marital_heatmap(filtered), use_container_width=True)
with col_b:
    st.plotly_chart(plot_month_subscription(filtered), use_container_width=True)

st.plotly_chart(plot_contact_subscription(filtered), use_container_width=True)
