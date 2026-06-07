# 00 · 项目上下文 〔本项目活记忆 · AI 维护〕

> **作用**:这是项目的"身份档案"。AI 接管项目时先读这里,了解项目目标、技术栈、目录、部署取值。
> **更新时机**:架构、技术栈、目录结构、端口、部署目录、重要约束变化时更新。

---

## 1. 项目是什么

- **项目名称**: `bank-marketing-predict`
- **一句话目标**: 基于银行营销数据构建可视化分析与认购预测的 Web 应用
- **使用者/受益者**: 银行营销人员、数据分析师
- **核心功能**:
  - **数据分析交互页面**: 展示客户特征分布(年龄、职业、婚姻、教育等)、营销效果分析,支持交互式筛选与图表探索
  - **在线预测系统**: 离线训练预测模型后,通过点选式表单输入客户特征,实时预测该客户是否会认购定期存款
- **输入/数据**: 银行营销数据集 `data/train.csv`(训练+评估) 与 `data/test.csv`(预测),共 21 个特征(年龄、职业、婚姻、教育、联系方式、经济指标等),目标变量 `subscribe`(yes/no)。来源:`E:\全栈AI黑马\李大婷-AI编程3.0\课程\part1\day01\数据`。**教学公开数据,进 Git**。

## 2. 技术栈

| 层 | 选型 | 理由 |
|---|---|---|
| 语言/运行时 | Python 3.11 | 课程指定版本 |
| Web/应用框架 | Streamlit 1.x | 快速构建数据应用,内置图表与表单组件 |
| 数据处理 | pandas、numpy | 数据清洗与分析 |
| 机器学习 | scikit-learn | 离线训练分类模型(LogisticRegression / RandomForest) |
| 可视化 | plotly / matplotlib | 交互式图表与静态图表 |
| 测试 | pytest + pytest-cov | Python 标准测试框架 |
| 格式/静态检查 | ruff | 统一格式与 lint |
| 容器化 | Docker | 本地部署 |
| CI | GitHub Actions | 自动检查(ruff + pytest + docker build) |

## 3. 目录地图

```text
bank-marketing-predict/
├── standards/                     # AI 项目记忆与通用规范
│   ├── README.md
│   ├── 00-project-context.md
│   ├── 01-requirements.md
│   ├── PROGRESS.md
│   ├── 02-coding-standards.md
│   ├── 03-testing-standards.md
│   ├── 04-git-workflow.md
│   ├── 05-cicd-standards.md
│   ├── 06-ai-collab-protocol.md
│   └── templates/
├── app/                           # 应用主目录
│   ├── __init__.py
│   ├── main.py                    # Streamlit 入口(页面路由)
│   ├── pages/                     # 多页面
│   │   ├── __init__.py
│   │   ├── 01_data_analysis.py    # 数据分析交互页面
│   │   └── 02_prediction.py       # 在线预测页面(点选表单)
│   ├── models/                    # 业务逻辑
│   │   ├── __init__.py
│   │   ├── data_loader.py         # 数据加载与预处理
│   │   ├── predictor.py           # 预测服务(加载模型+推理)
│   │   └── visualizer.py          # 图表生成逻辑
│   ├── ml/                        # 机器学习
│   │   ├── __init__.py
│   │   ├── train.py               # 离线训练脚本
│   │   └── model/                 # 模型产物(.gitignore)
│   └── utils/                     # 工具函数
│       └── __init__.py
├── tests/                         # 测试
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_data_loader.py
│   ├── test_predictor.py
│   └── test_visualizer.py
├── data/                          # 数据(进 Git)
│   ├── train.csv
│   └── test.csv
├── requirements.txt               # 生产运行依赖
├── requirements-dev.txt           # 开发/CI 依赖
├── Dockerfile                     # 容器镜像
├── .github/workflows/
│   └── ci.yml                     # CI(无 CD)
├── .gitignore
├── README.md
└── pyproject.toml                 # ruff 配置
```

## 4. 质量门槛

| 类型 | 本项目标准 |
|---|---|
| 格式检查 | `ruff format --check .` |
| 静态检查 | `ruff check .` |
| 单元测试 | `pytest` |
| 覆盖率 | 核心业务逻辑 ≥80%(models/、ml/);UI 页面无覆盖率要求 |
| 构建 | `docker build` 成功 |
| 模型指标 | 训练脚本输出 AUC、准确率、分类报告 |
| 预测响应 | 单次预测 <1s |

## 5. 不变约束

- 密钥、密码不含在代码中(教学项目无敏感信息)。
- `data/` 目录(CSV 文件)进 Git;`app/ml/model/` 目录(模型产物)加入 `.gitignore`。
- **不做 CD**,本地 Docker 部署验证即可。
- **端口 8004**(容器内 Streamlit 默认 8501,Docker 映射到主机 8004)。
- `main` 分支走 feature 分支 + PR,C I 红灯不合并。
- 模型训练是离线操作(本地执行脚本),预测服务加载训练好的模型文件。

## 6. 部署/CI 占位符取值

| 占位符 | 本项目取值 | 说明 |
|---|---|---|
| `<APP>` | `bank-predict` | 镜像名/容器名 |
| `<PORT>` | `8004` | 主机端口 |
| `<PYVER>` | `3.11` | Python 版本 |
| `<HEALTHCHECK>` | `/_stcore/health` | Streamlit 健康检查端点 |
| `<STREAMLIT_PORT>` | `8501` | 容器内 Streamlit 默认端口 |
