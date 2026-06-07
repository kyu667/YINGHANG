import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def plot_subscription_pie(df: pd.DataFrame) -> go.Figure:
    counts = df["subscribe"].value_counts().reset_index()
    counts.columns = ["subscribe", "count"]
    fig = px.pie(
        counts,
        names="subscribe",
        values="count",
        title="认购分布",
        color="subscribe",
        color_discrete_map={"yes": "#2ca02c", "no": "#d62728"},
    )
    fig.update_traces(textinfo="percent+label")
    return fig


def plot_age_distribution(df: pd.DataFrame) -> go.Figure:
    fig = px.histogram(df, x="age", nbins=20, title="年龄分布", color_discrete_sequence=["#1f77b4"])
    fig.update_layout(bargap=0.1, xaxis_title="年龄", yaxis_title="人数")
    return fig


def plot_job_subscription_rate(df: pd.DataFrame) -> go.Figure:
    job_stats = df.groupby("job")["subscribe"].value_counts(normalize=True).unstack()
    if "yes" in job_stats.columns:
        job_stats = job_stats.sort_values("yes", ascending=False)
    fig = px.bar(
        job_stats,
        y=job_stats.index,
        x="yes" if "yes" in job_stats.columns else job_stats.columns[0],
        title="各职业认购率",
        orientation="h",
        labels={"y": "职业", "x": "认购率"},
    )
    fig.update_traces(marker_color="#2ca02c")
    return fig


def plot_education_marital_heatmap(df: pd.DataFrame) -> go.Figure:
    ct = pd.crosstab(df["education"], df["marital"])
    fig = px.imshow(
        ct,
        text_auto=True,
        aspect="auto",
        title="教育水平 vs 婚姻状况 交叉分析",
        labels={"x": "婚姻状况", "y": "教育水平", "color": "人数"},
    )
    return fig


def plot_month_subscription(df: pd.DataFrame) -> go.Figure:
    month_order = [
        "jan",
        "feb",
        "mar",
        "apr",
        "may",
        "jun",
        "jul",
        "aug",
        "sep",
        "oct",
        "nov",
        "dec",
    ]
    month_stats = df.groupby("month")["subscribe"].value_counts(normalize=True).unstack()
    if "yes" in month_stats.columns:
        month_stats = month_stats.reindex([m for m in month_order if m in month_stats.index])
        fig = px.line(
            month_stats,
            x=month_stats.index,
            y="yes",
            markers=True,
            title="各月份认购率趋势",
            labels={"x": "月份", "y": "认购率", "index": "月份"},
        )
        fig.update_traces(line_color="#2ca02c")
        return fig
    return go.Figure()


def plot_contact_subscription(df: pd.DataFrame) -> go.Figure:
    contact_stats = df.groupby("contact")["subscribe"].value_counts(normalize=True).unstack()
    if "yes" in contact_stats.columns:
        fig = px.bar(
            contact_stats,
            x=contact_stats.index,
            y="yes",
            title="联系方式 vs 认购率",
            labels={"x": "联系方式", "y": "认购率"},
            color_discrete_sequence=["#1f77b4"],
        )
        return fig
    return go.Figure()
