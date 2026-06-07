# 银行营销数据分析与预测系统

基于银行营销数据构建的可视化分析与认购预测 Web 应用。

## 功能

| 功能 | 说明 |
|---|---|
| 数据分析 | 客户特征分布、认购率分析、交互式图表（饼图/柱状图/热力图/折线图），支持职业/婚姻/教育筛选 |
| 在线预测 | 点选式表单输入客户特征，实时预测认购概率（随机森林模型，AUC 89.5%） |

## 技术栈

Python 3.11 + Streamlit + scikit-learn + plotly + pytest + ruff + Docker

## 快速启动

```bash
# 1. 安装依赖
pip install -r requirements.txt -r requirements-dev.txt

# 2. 训练模型
python -m app.ml.train

# 3. 启动应用
streamlit run app/main.py --server.port 8004
```

浏览器打开 `http://localhost:8004`

## Docker 部署

```bash
docker build -t bank-predict .
docker run -d -p 8004:8501 bank-predict
```

## CI/CD

- **CI**: GitHub Actions，push/PR 自动触发 ruff format → ruff lint → train model → pytest → docker build
- **CD**: 无（本地部署）

CI 状态：![CI](https://github.com/kyu667/YINGHANG/actions/workflows/ci.yml/badge.svg)

## 项目结构

```
├── app/
│   ├── main.py                  # Streamlit 入口
│   ├── pages/
│   │   ├── 01_data_analysis.py  # 数据分析页面
│   │   └── 02_prediction.py     # 在线预测页面
│   ├── models/
│   │   ├── data_loader.py       # 数据加载
│   │   ├── predictor.py         # 预测引擎
│   │   └── visualizer.py        # 图表生成
│   └── ml/
│       ├── train.py             # 训练脚本
│       └── model/               # 模型产物（gitignore）
├── tests/                       # 20 个测试用例
├── data/                        # train.csv + test.csv
├── standards/                   # 项目规划文档
└── .github/workflows/ci.yml     # CI 流水线
```

## 模型指标

| 指标 | 值 |
|---|---|
| Accuracy | 88.6% |
| AUC | 89.5% |
| 5-Fold CV AUC | 89.3% ± 0.3% |

## 本地开发

```bash
# 格式检查
ruff format --check .
ruff check .

# 运行测试
pytest --cov=app/models --cov=app/ml --cov-fail-under=80
```
