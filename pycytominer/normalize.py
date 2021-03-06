"""
Normalize observation features based on specified normalization method
"""

import pandas as pd
from sklearn.preprocessing import StandardScaler, RobustScaler

from pycytominer.cyto_utils import (
    output,
    infer_cp_features,
    load_profiles,
)
from pycytominer.operations import Spherize, RobustMAD


def normalize(
    profiles,
    features="infer",
    meta_features="infer",
    samples="all",
    method="standardize",
    output_file="none",
    compression_options=None,
    float_format=None,
    spherize_center=True,
    spherize_method="ZCA-cor",
):
    """
    Normalize features

    Arguments:
    profiles - either pandas DataFrame or a file that stores profile data
    features - [default: "infer"] list of cell painting features
               if "infer", then assume cell painting features are those that do not
               start with "Cells", "Nuclei", or "Cytoplasm"
    meta_features - [default: "infer"] if specified, then output these with
                    specified features
    samples - [default: 'all'] string indicating which metadata column and
              values to use to the control samples are often used here
              the format of this variable will be used in a pd.query() function. An
              example is "Metadata_treatment == 'control'" (include all quotes)
    method - [default: 'standardize'] string indicating how the dataframe will
             be normalized. Check avail_methods for available normalization methods.
    output_file - [default: "none"] if provided, will write annotated profiles to file
                  if not specified, will return the annotated profiles. We recommend
                  that this output file be suffixed with "_normalized.csv".
    compression - [default: None] the mechanism to compress. See cyto_utils/output.py for options.
    float_format - [default: None] decimal precision to use in writing output file
                   For example, use "%.3g" for 3 decimal precision.
    spherize_center - [default: True] if data should be centered before sphering
                      (aka whitening) transform (only used if method = "spherize")
    spherize_method - [default: 'ZCA-cor'] the type of sphering (aka whitening)
                      normalization used (only used if method = "spherize")

    Return:
    A normalized DataFrame
    """

    # Load Data
    profiles = load_profiles(profiles)

    # Define which scaler to use
    method = method.lower()

    avail_methods = ["standardize", "robustize", "mad_robustize", "spherize"]
    assert method in avail_methods, "operation must be one {}".format(avail_methods)

    if method == "standardize":
        scaler = StandardScaler()
    elif method == "robustize":
        scaler = RobustScaler()
    elif method == "mad_robustize":
        scaler = RobustMAD()
    elif method == "spherize":
        scaler = Spherize(center=spherize_center, method=spherize_method)

    if features == "infer":
        features = infer_cp_features(profiles)

    # Separate out the features and meta
    feature_df = profiles.loc[:, features]
    if meta_features == "infer":
        meta_features = infer_cp_features(profiles, metadata=True)

    meta_df = profiles.loc[:, meta_features]

    # Fit the sklearn scaler
    if samples == "all":
        fitted_scaler = scaler.fit(feature_df)
    else:
        # Subset to only the features measured in the sample query
        fitted_scaler = scaler.fit(profiles.query(samples).loc[:, features])

    # Scale the feature dataframe
    feature_df = pd.DataFrame(
        fitted_scaler.transform(feature_df),
        columns=feature_df.columns,
        index=feature_df.index,
    )

    normalized = meta_df.merge(feature_df, left_index=True, right_index=True)

    if output_file != "none":
        output(
            df=normalized,
            output_filename=output_file,
            compression_options=compression_options,
            float_format=float_format,
        )
    else:
        return normalized
