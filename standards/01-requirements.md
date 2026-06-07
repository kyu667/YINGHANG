# 01 · 需求 / 活 PRD 〔本项目活记忆 · AI 维护〕

> **作用**:这是本项目唯一的需求文档。所有新功能、缺陷、技术债都追加到这里,不要另起多个 PRD 文件。
> **更新时机**:每次有新需求、需求变更、验收标准变化时更新。

---

## 1. 需求来源

| 类型 | 来源 | 进入方式 |
|---|---|---|
| 功能需求 Feature | 课程作业 | 写成用户故事 |
| 缺陷 Bug | 测试 / 本地验证 | 写复现步骤和期望结果 |
| 技术债 Tech Debt | 开发 / Review | 写影响和修复目标 |

---

## 2. Issue 生命周期

| 阶段 | 状态 | 动作 |
|---|---|---|
| 提出 | Open | 写清场景、目标、验收标准 |
| 排期 | Backlog / Todo | 决定优先级 |
| 开发 | In Progress | 从 main 开 feature 分支 |
| 评审 | In Review | 提 PR,等待 CI |
| 合并 | Done | PR 合并 main |
| 验收 | Verified | 按验收标准确认 |

---

## 3. 用户故事模板

```text
### US-<编号> <一句话标题> · 状态: Backlog
作为 <角色>,
我想要 <能力>,
以便 <价值>。

验收标准:
- AC1: Given <前提>,When <动作>,Then <可验证结果>。
- AC2: <补充标准>

技术备注:
- <可选:约束、边界、风险>
```

---

## 4. 需求清单

### US-1 项目工程化初始化与 CI · 状态: Backlog

作为 **项目开发者**,
我想要 项目具备基础工程结构、代码检查与 CI 流水线,
以便 后续每次提交都能自动验证代码质量。

验收标准:
- AC1: Given 项目目录,When 创建完成,Then 包含 `app/`、`tests/`、`data/`、`.github/workflows/`、`Dockerfile`、`pyproject.toml`、`requirements.txt`、`requirements-dev.txt`。
- AC2: Given 代码提交,When CI 触发,Then 依次执行 `ruff format --check .`、`ruff check .`、`pytest --cov --cov-fail-under=80`、`docker build` 四道门禁。
- AC3: Given CI 完成,When 所有门禁通过,Then CI 显示绿色;任一失败则红色。
- AC4: Given 本地开发,When 执行 `docker build -t bank-predict . && docker run -d -p 8004:8501 bank-predict`,Then 容器启动后 `curl http://localhost:8004/_stcore/health` 返回 200。
- AC5: Given 项目根目录,When 打开浏览器访问 `http://localhost:8004`,Then 显示 Streamlit 应用首页。

技术备注:
- 不含 CD,只做 CI + 本地 Docker 部署验证。
- ruff 配置写入 `pyproject.toml`,行宽 100,目标 Python 3.11。

---

### US-2 数据加载与预处理模块 · 状态: Backlog

作为 **开发者**,
我想要 一个可复用的数据加载模块,
以便 为数据分析页面和模型训练提供统一的数据入口。

验收标准:
- AC1: Given `data/train.csv` 存在,When 调用 `load_train_data()`,Then 返回 pandas DataFrame,包含 21 列特征 + subscribe 目标列。
- AC2: Given `data/test.csv` 存在,When 调用 `load_test_data()`,Then 返回 DataFrame,包含 21 列特征(无 subscribe 列)。
- AC3: Given 原始数据含 'unknown' / 'nonexistent' 标记,When 加载数据,Then 正确识别为缺失值并统一处理。
- AC4: Given 数据加载模块,When 编写单元测试,Then 覆盖:正常加载、文件不存在、空文件、缺失值处理。
- AC5: Given 数据目录,When Docker 构建,Then `data/` 目录随镜像打包。

技术备注:
- CSV 为 UTF-8 编码,分隔符为逗号。
- 需要返回特征列名列表,便于后续页面动态生成表单。

---

### US-3 数据分析交互页面 · 状态: Backlog

作为 **业务分析师**,
我想要 通过可视化界面探索银行营销数据,
以便 快速理解客户特征分布与认购行为规律。

验收标准:
- AC1: Given 访问"数据分析"页面,When 页面加载,Then 显示数据概览指标:总记录数、认购率(yes 占比)、平均年龄、客户职业数等。
- AC2: Given 数据分析页面,When 选择"年龄分布"维度,Then 展示年龄分布的直方图/饼图。
- AC3: Given 数据分析页面,When 选择"职业 vs 认购率"维度,Then 展示各职业认购率的柱状图。
- AC4: Given 数据分析页面,When 选择"教育水平"与"婚姻状况"维度,Then 展示交叉分析图表(堆叠柱状图/热力图)。
- AC5: Given 数据分析页面,When 用户筛选(如选择特定月份、职业),Then 图表实时更新,仅展示筛选后数据。
- AC6: Given 页面渲染,When 在 Docker 容器中访问,Then 所有图表正常显示,无报错。

技术备注:
- 使用 Streamlit 组件:`st.metric`、`st.selectbox`、`st.multiselect`、`st.plotly_chart` / `st.pyplot`。
- 图表类型包括:直方图(年龄)、柱状图(职业/教育/婚姻 vs 认购率)、饼图(认购分布)、热力图(交叉分析)。
- 可视化逻辑封装在 `app/models/visualizer.py`,与页面解耦,方便测试。

---

### US-4 模型离线训练脚本 · 状态: Backlog

作为 **数据科学家**,
我想要 一个可复现的离线训练脚本,
以便 从历史数据中训练认购预测模型并保存。

验收标准:
- AC1: Given 训练数据存在,When 执行 `python -m app.ml.train`,Then 在 `app/ml/model/` 目录生成 `model.pkl` 和 `encoder.pkl`(特征编码器)。
- AC2: Given 训练完成,When 查看日志,Then 打印 AUC、准确率、精确率、召回率、F1 及分类报告。
- AC3: Given 模型文件已存在,When 再次执行训练,Then 默认覆盖旧模型(或通过 `--skip` 参数跳过)。
- AC4: Given 训练脚本,When 本地运行,Then 固定 `random_state=42` 保证可复现。
- AC5: Given 提交代码,When git push,Then `app/ml/model/` 目录不被提交(.gitignore 已排除)。

技术备注:
- 使用 scikit-learn 的 `RandomForestClassifier` 或 `LogisticRegression`。
- 类别特征(如 job、marital、education 等)使用 `LabelEncoder` 或 `OneHotEncoder`,编码器随模型一起保存。
- 训练/验证拆分比例 8:2,分层抽样(`stratify=y`)。

---

### US-5 在线预测页面(点选式表单) · 状态: Backlog

作为 **营销人员**,
我想要 通过点选下拉框输入客户特征,
以便 快速预测该客户是否会认购定期存款,辅助营销决策。

验收标准:
- AC1: Given 访问"在线预测"页面,When 页面加载,Then 显示点选式表单:每个特征对应一个下拉选择框(selectbox),选项来自训练数据中的唯一值。
- AC2: Given 表单,When 所有字段选择完毕并点击"开始预测"按钮,Then 显示预测结果:是否认购(yes/no)、认购概率(0-100%)、置信度(高/中/低)。
- AC3: Given 预测结果,When 展示结果,Then 用进度条或仪表盘可视化概率值,并用颜色区分(绿=高概率认购,红=低概率)。
- AC4: Given 表单已填写,When 点击"重置"按钮,Then 所有选择框恢复默认值,结果清空。
- AC5: Given 模型文件缺失,When 页面加载,Then 显示友好提示"模型未训练,请先执行训练脚本"。
- AC6: Given 输入非法特征组合,When 点击预测,Then 显示具体错误提示而非崩溃。
- AC7: Given 单次预测,When 从点击按钮到展示结果,Then 响应时间 <1s。

技术备注:
- 使用 Streamlit 组件:`st.selectbox`(类别特征)、`st.number_input`/`st.slider`(数值特征)、`st.button`、`st.progress`。
- 表单字段按业务含义分组:个人信息(年龄、职业、婚姻、教育)、财务(房贷、贷款、违约)、营销(接触方式、月份、星期、通话时长等)、经济指标(就业率、消费者指数等)。
- 预测结果展示:大号指标卡片 + 概率进度条 + 建议文案(如"该客户认购概率较高,建议优先跟进")。

---

### US-6 测试覆盖与最终验收 · 状态: Backlog

作为 **CI 流水线**,
我想要 完整的测试覆盖与本地部署验证,
以便 保证交付质量。

验收标准:
- AC1: Given `data_loader.py`,When 运行测试,Then 覆盖正常加载、文件缺失、空文件、数据校验场景,所有用例通过。
- AC2: Given `predictor.py`,When 运行测试,Then 覆盖正常预测、模型缺失、非法输入场景,所有用例通过。
- AC3: Given `visualizer.py`,When 运行测试,Then 覆盖图表数据生成逻辑,所有用例通过。
- AC4: Given 全部测试,When 运行 `pytest --cov=app/models --cov=app/ml --cov-fail-under=80`,Then 覆盖率 ≥80% 且全部通过。
- AC5: Given 代码提交,When CI 运行,Then ruff + pytest + docker build 三个阶段全绿。
- AC6: Given 本地部署,When `docker run -d -p 8004:8501 bank-predict`,Then 浏览器访问 `http://localhost:8004` 两个页面均正常可用。

---

## 5. 非功能需求

- **安全**:教学公开数据,无敏感信息;不涉及密钥管理。
- **可维护**:一需求一小 PR,核心逻辑与 UI 分离。
- **可测试**:`models/` 和 `ml/` 中的纯逻辑必须有单元测试;Streamlit 页面不需要 UI 测试。
- **可部署**:本地 `docker build` + `docker run` 一键启动,端口 8004。
- **性能**:单次预测 <1s,数据分析页面首屏加载 <3s。
- **不做 CD**:只做 CI 检查 + 本地 Docker 验证,不部署到远程服务器。
