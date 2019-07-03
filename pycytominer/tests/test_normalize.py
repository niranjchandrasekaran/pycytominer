import pandas as pd
from pycytominer.normalize import normalize

# Build data to use in tests
data_df = pd.DataFrame(
    {
        "Metadata_plate": ["a", "a", "a", "a", "b", "b", "b", "b"],
        "Metadata_treatment": [
            "drug",
            "drug",
            "control",
            "control",
            "drug",
            "drug",
            "control",
            "control",
        ],
        "x": [1, 2, 8, 2, 5, 5, 5, 1],
        "y": [3, 1, 7, 4, 5, 9, 6, 1],
        "z": [1, 8, 2, 5, 6, 22, 2, 2],
        "zz": [14, 46, 1, 6, 30, 100, 2, 2],
    }
).reset_index(drop=True)


def test_normalize_standardize_allsamples():
    """
    Testing normalize pycytominer function
    method = "standardize"
    meta_variables = "none"
    samples="all"
    """
    normalize_result = normalize(
        population_df=data_df,
        variables=["x", "y", "z", "zz"],
        meta_variables="none",
        samples="all",
        method="standardize",
    ).round(1)

    expected_result = pd.DataFrame(
        {
            "Metadata_plate": ["a", "a", "a", "a", "b", "b", "b", "b"],
            "Metadata_treatment": [
                "drug",
                "drug",
                "control",
                "control",
                "drug",
                "drug",
                "control",
                "control",
            ],
            "x": [-1.1, -0.7, 1.9, -0.7, 0.6, 0.6, 0.6, -1.1],
            "y": [-0.6, -1.3, 0.9, -0.2, 0.2, 1.7, 0.6, -1.3],
            "z": [-0.8, 0.3, -0.6, -0.2, 0.0, 2.5, -0.6, -0.6],
            "zz": [-0.3, 0.7, -0.8, -0.6, 0.2, 2.3, -0.7, -0.7],
        }
    ).reset_index(drop=True)

    assert normalize_result.equals(expected_result)


def test_normalize_standardize_ctrlsamples():
    """
    Testing normalize pycytominer function
    method = "standardize"
    meta_variables = "none"
    samples="Metadata_treatment == 'control'"
    """
    normalize_result = normalize(
        population_df=data_df,
        variables=["x", "y", "z", "zz"],
        meta_variables="none",
        samples="Metadata_treatment == 'control'",
        method="standardize",
    ).round(1)

    expected_result = pd.DataFrame(
        {
            "Metadata_plate": ["a", "a", "a", "a", "b", "b", "b", "b"],
            "Metadata_treatment": [
                "drug",
                "drug",
                "control",
                "control",
                "drug",
                "drug",
                "control",
                "control",
            ],
            "x": [-1.1, -0.7, 1.5, -0.7, 0.4, 0.4, 0.4, -1.1],
            "y": [-0.7, -1.5, 1.1, -0.2, 0.2, 2.0, 0.7, -1.5],
            "z": [-1.3, 4.0, -0.6, 1.7, 2.5, 14.8, -0.6, -0.6],
            "zz": [5.9, 22.5, -0.9, 1.7, 14.2, 50.6, -0.4, -0.4],
        }
    ).reset_index(drop=True)

    assert normalize_result.equals(expected_result)


def test_normalize_robustize_allsamples():
    """
    Testing normalize pycytominer function
    method = "standardize"
    meta_variables = "none"
    samples="all"
    """
    normalize_result = normalize(
        population_df=data_df,
        variables=["x", "y", "z", "zz"],
        meta_variables="none",
        samples="all",
        method="robustize",
    ).round(1)

    expected_result = pd.DataFrame(
        {
            "Metadata_plate": ["a", "a", "a", "a", "b", "b", "b", "b"],
            "Metadata_treatment": [
                "drug",
                "drug",
                "control",
                "control",
                "drug",
                "drug",
                "control",
                "control",
            ],
            "x": [-0.8, -0.5, 1.4, -0.5, 0.5, 0.5, 0.5, -0.8],
            "y": [-0.4, -0.9, 0.7, -0.1, 0.1, 1.2, 0.4, -0.9],
            "z": [-0.6, 1.0, -0.3, 0.3, 0.6, 4.1, -0.3, -0.3],
            "zz": [0.1, 1.1, -0.3, -0.1, 0.6, 2.8, -0.2, -0.2],
        }
    ).reset_index(drop=True)

    assert normalize_result.equals(expected_result)


def test_normalize_robustize_ctrlsamples():
    """
    Testing normalize pycytominer function
    method = "standardize"
    meta_variables = "none"
    samples="Metadata_treatment == 'control'"
    """
    normalize_result = normalize(
        population_df=data_df,
        variables=["x", "y", "z", "zz"],
        meta_variables="none",
        samples="Metadata_treatment == 'control'",
        method="robustize",
    ).round(1)

    expected_result = pd.DataFrame(
        {
            "Metadata_plate": ["a", "a", "a", "a", "b", "b", "b", "b"],
            "Metadata_treatment": [
                "drug",
                "drug",
                "control",
                "control",
                "drug",
                "drug",
                "control",
                "control",
            ],
            "x": [-0.6, -0.4, 1.1, -0.4, 0.4, 0.4, 0.4, -0.6],
            "y": [-0.7, -1.3, 0.7, -0.3, 0.0, 1.3, 0.3, -1.3],
            "z": [-1.3, 8.0, 0.0, 4.0, 5.3, 26.7, 0.0, 0.0],
            "zz": [9.6, 35.2, -0.8, 3.2, 22.4, 78.4, 0.0, 0.0],
        }
    ).reset_index(drop=True)

    assert normalize_result.equals(expected_result)
