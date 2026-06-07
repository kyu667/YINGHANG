import os

import pandas as pd
import pytest


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "age": [30, 45, 28],
            "job": ["admin.", "technician", "services"],
            "marital": ["married", "single", "divorced"],
            "education": ["high.school", "university.degree", "basic.9y"],
            "default": ["no", "no", "yes"],
            "housing": ["yes", "no", "yes"],
            "loan": ["no", "yes", "no"],
            "subscribe": ["no", "yes", "no"],
        }
    )


@pytest.fixture
def data_dir():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
