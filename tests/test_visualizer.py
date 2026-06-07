import pandas as pd

from app.models.visualizer import (
    plot_age_distribution,
    plot_job_subscription_rate,
    plot_subscription_pie,
)


class TestVisualizer:
    @staticmethod
    def _sample_df():
        return pd.DataFrame(
            {
                "age": [30, 45, 28, 52, 38],
                "job": ["admin.", "technician", "services", "admin.", "technician"],
                "marital": ["married", "single", "divorced", "married", "single"],
                "education": [
                    "high.school",
                    "university.degree",
                    "basic.9y",
                    "high.school",
                    "university.degree",
                ],
                "contact": ["cellular", "telephone", "cellular", "cellular", "telephone"],
                "month": ["jan", "feb", "mar", "jan", "feb"],
                "subscribe": ["no", "yes", "no", "yes", "yes"],
            }
        )

    def test_plot_subscription_pie_returns_figure(self):
        df = self._sample_df()
        fig = plot_subscription_pie(df)
        assert fig is not None

    def test_plot_age_distribution_returns_figure(self):
        df = self._sample_df()
        fig = plot_age_distribution(df)
        assert fig is not None

    def test_plot_job_subscription_rate_returns_figure(self):
        df = self._sample_df()
        fig = plot_job_subscription_rate(df)
        assert fig is not None

    def test_plot_education_marital_heatmap_returns_figure(self):
        df = self._sample_df()
        from app.models.visualizer import plot_education_marital_heatmap

        fig = plot_education_marital_heatmap(df)
        assert fig is not None

    def test_plot_month_subscription_returns_figure(self):
        df = self._sample_df()
        from app.models.visualizer import plot_month_subscription

        fig = plot_month_subscription(df)
        assert fig is not None

    def test_plot_contact_subscription_returns_figure(self):
        df = self._sample_df()
        from app.models.visualizer import plot_contact_subscription

        fig = plot_contact_subscription(df)
        assert fig is not None
