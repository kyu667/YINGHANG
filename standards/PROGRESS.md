# PROGRESS · bank-marketing-predict 〔本项目活记忆 · 状态机〕

> **作用**:这是项目的"存档点"。任意 AI、任意重启会话,读它即可知道当前做到哪、下一步做什么、踩过什么坑。
> **更新时机**:每完成一个有意义步骤、每次会话结束前。
> **格式要求**:时间倒序,最新在上;短、准、可接力。

---

## 当前状态 (最后更新: 2026-06-07 · by AI)

- **阶段**: `本地部署验证通过，等待用户验证`
- **上一步完成**: ruff ✅, pytest(19 passed/1 skipped/92%覆盖) ✅, Streamlit 启动(8004) ✅, 健康检查 ✅
- **下一步 (TODO 第一条)**: 用户浏览器验证两大功能页面
- **阻塞项**: 无

---

## 待办清单 (TODO,按优先级)

### 第一批:项目工程化初始化与 CI(US-1) — 已完成
- [x] 初始化 git 仓库
- [x] 复制数据文件(train.csv/test.csv)到 `data/`
- [x] 创建 `.gitignore`、`pyproject.toml`、`requirements.txt`、`requirements-dev.txt`、`Dockerfile`、`.github/workflows/ci.yml`
- [x] 创建目录结构与占位模块
- [x] 本地 CI 自检通过:ruff format ✅ / ruff check ✅ / pytest ✅(92%覆盖)

### 第二批:数据加载模块(US-2) — 已完成
- [x] 实现 `app/models/data_loader.py`(加载/缺失值处理/特征分类)
- [x] 编写 `tests/test_data_loader.py`(9 tests passed)
- [x] 本地自检通过

### 第三批:数据分析页面(US-3) — 已完成
- [x] 实现 `app/models/visualizer.py`(6 种图表:饼图/直方图/柱状图/热力图/折线图/柱状图)
- [x] 实现 `app/pages/01_data_analysis.py`(概览指标 + 多维筛选 + 交互式图表)
- [x] 编写 `tests/test_visualizer.py`(6 tests passed)

### 第四批:模型训练脚本(US-4) — 已完成
- [x] 实现 `app/ml/train.py`(RandomForest + LabelEncoder + StratifiedCV)
- [x] 本地训练完成:Accuracy 88.6%, AUC 89.5%, 5-CV AUC 89.3%
- [x] 模型产物:model.pkl + encoders.pkl 存入 `app/ml/model/`

### 第五批:在线预测页面(US-5) — 已完成
- [x] 实现 `app/models/predictor.py`(加载模型+编码+推理+置信度)
- [x] 实现 `app/pages/02_prediction.py`(分组表单 + 进度条 + 建议文案)
- [x] 编写 `tests/test_predictor.py`(5 tests passed, 响应时间 <1s)

### 第六批:Docker 构建与最终验收(US-6)
- [ ] `docker build` 本地构建验证(Docker Desktop 未运行，待启动后验证)
- [ ] 浏览器验证两个页面

---

## 关键决策记录 (ADR)

| 日期 | 决策 | 理由 |
|---|---|---|
| 2026-06-07 | 不实现 CD,只做 CI + 本地 Docker 部署 | 课程要求;聚焦代码质量与本地验证 |
| 2026-06-07 | 端口 8004,容器内 8501 | 课程指定;Streamlit 默认 8501,映射到主机 8004 |
| 2026-06-07 | 数据进 Git,模型不进 Git | 教学公开数据,方便复现;模型二进制大文件不应进版本控制 |
| 2026-06-07 | 先训练后预测,离线训练+在线推理 | 训练是重操作;预测是轻操作需快速响应 |
| 2026-06-07 | 预测页面采用纯下拉选择框(非手动输入) | 降低输入错误,提升营销人员使用体验 |
| 2026-06-07 | coverage 排除 `app/ml/train.py` | 训练脚本为离线工具,不计入运行时覆盖率;核心模块独立覆盖率全部 >85% |
| 2026-06-07 | ruff per-file-ignores:N999(页面数字前缀)、N806(ML 变量命名)、N802(测试方法名) | Streamlit 页面需数字前缀排序;ML 领域习惯 X/y 命名;pytest 方法名可灵活 |

---

## 已知坑 (GOTCHAS)

- Windows Docker Desktop 需要手动启动;本地 Streamlit 直连可绕过,`docker build` 留给 CI
- Anaconda Python 3.12 vs 项目目标 3.11 — 语法兼容无影响,CI runner 用 3.11
- 测试中 `patch.object` 对 `@property` 不生效,改用 `patch` 路径 mock

---

## 里程碑 (DONE)

- [x] 2026-06-07:读取数据(train.csv:22500行×22列/test.csv:未确认;21 特征 + subscribe)
- [x] 2026-06-07:填写 `00-project-context.md` 和 `01-requirements.md`,定义 6 个用户故事
- [x] 2026-06-07:初始化 `PROGRESS.md`
- [x] 2026-06-07:完成全部 5 个核心用户故事(US-1 ~ US-5),US-6 Docker 验证待 Docker 环境
- [x] 2026-06-07:CI 本地自检全绿:ruff format ✅ / ruff check ✅ / pytest 19 passed + 1 skipped / 覆盖率 92%
- [x] 2026-06-07:Streamlit 启动在 `http://localhost:8004`,健康检查 `/_stcore/health` 返回 ok
