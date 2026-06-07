import streamlit as st

from app.models.data_loader import get_feature_columns, load_train_data
from app.models.predictor import Predictor

st.title("🔮 在线预测")
st.markdown("通过点选表单输入客户特征,预测该客户是否会认购定期存款。")

predictor = Predictor()

if not predictor.model_loaded:
    st.warning("⚠️ 模型文件不存在,请先执行训练脚本: `python -m app.ml.train`")
    st.stop()

# build feature options from training data
df = load_train_data()
features = get_feature_columns()

# get unique values for categorical features
cat_features = df[features].select_dtypes(include="object").columns.tolist()
num_features = df[features].select_dtypes(include="number").columns.tolist()

feature_options = {}
for col in cat_features:
    vals = sorted(df[col].dropna().unique().tolist())
    feature_options[col] = vals
for col in num_features:
    feature_options[col] = (float(df[col].min()), float(df[col].max()), float(df[col].mean()))

st.subheader("客户特征输入")

# group features
personal = ["age", "job", "marital", "education"]
financial = ["default", "housing", "loan"]
campaign = [
    "contact",
    "month",
    "day_of_week",
    "duration",
    "campaign",
    "pdays",
    "previous",
    "poutcome",
]
economic = ["emp_var_rate", "cons_price_index", "cons_conf_index", "lending_rate3m", "nr_employed"]

user_input = {}

with st.expander("👤 个人信息", expanded=True):
    cols = st.columns(2)
    for i, col in enumerate(personal):
        with cols[i % 2]:
            if col in cat_features:
                opts = feature_options[col]
                user_input[col] = st.selectbox(f"{col}", opts, key=f"pred_{col}")
            else:
                mn, mx, mean = feature_options[col]
                user_input[col] = st.slider(f"{col}", mn, mx, float(mean), key=f"pred_{col}")

with st.expander("💰 财务状况"):
    cols = st.columns(3)
    for i, col in enumerate(financial):
        with cols[i % 3]:
            opts = feature_options[col]
            user_input[col] = st.selectbox(f"{col}", opts, key=f"pred_{col}")

with st.expander("📞 营销信息"):
    cols = st.columns(2)
    for i, col in enumerate(campaign):
        with cols[i % 2]:
            if col in cat_features:
                opts = feature_options[col]
                user_input[col] = st.selectbox(f"{col}", opts, key=f"pred_{col}")
            else:
                mn, mx, mean = feature_options[col]
                user_input[col] = st.slider(f"{col}", mn, mx, float(mean), key=f"pred_{col}")

with st.expander("📈 经济指标"):
    cols = st.columns(2)
    for i, col in enumerate(economic):
        with cols[i % 2]:
            mn, mx, mean = feature_options[col]
            user_input[col] = st.slider(f"{col}", mn, mx, float(mean), key=f"pred_{col}")

st.divider()

col_btn1, col_btn2, _ = st.columns([1, 1, 4])
predict_clicked = col_btn1.button("🔍 开始预测", type="primary", use_container_width=True)
reset_clicked = col_btn2.button("🔄 重置", use_container_width=True)

if reset_clicked:
    st.rerun()

if predict_clicked:
    try:
        result = predictor.predict(user_input)

        st.subheader("预测结果")
        prob = result["probability"]

        col_a, col_b, col_c = st.columns(3)

        if result["subscribe"]:
            col_a.metric("预测结果", "✅ 会认购")
        else:
            col_a.metric("预测结果", "❌ 不会认购")

        col_b.metric("认购概率", f"{prob:.1%}")
        col_c.metric("置信度", result["confidence"])

        # progress bar
        st.progress(prob, text=f"认购概率: {prob:.1%}")

        # suggestion
        if prob >= 0.7:
            st.success("该客户认购概率较高,建议优先跟进营销。")
        elif prob >= 0.4:
            st.info("该客户有一定认购意愿,可作为次级跟进目标。")
        else:
            st.warning("该客户认购概率偏低,建议将资源投入到更高潜力客户。")

        st.caption(f"响应时间: {result['response_time_ms']}ms")

    except Exception as e:
        st.error(f"预测失败: {e}")
