# ============================================================
# FitCom - Comparison Engine
# Author: Anand Kumar
#
# Description:
# Provides comparative analytics between multiple
# participants in the FitCom dataset.
#
# Features:
# • Best performer detection
# • Lowest performer detection
# • Metric comparison across participants
# ============================================================

import pandas as pd


# ------------------------------------------------------------
# Compare Reports
# ------------------------------------------------------------
# Generates a comparison summary for numeric metrics.
# ------------------------------------------------------------

def compare_reports(df):

    numeric_cols = df.select_dtypes(include=["int64","float64"]).columns

    results = []

    for metric in numeric_cols:

        best_idx = df[metric].idxmax()
        worst_idx = df[metric].idxmin()

        results.append({
            "Metric": metric,
            "Best Performer": df.loc[best_idx]["Name"],
            "Best Value": df.loc[best_idx][metric],
            "Lowest Performer": df.loc[worst_idx]["Name"],
            "Lowest Value": df.loc[worst_idx][metric]
        })

    return pd.DataFrame(results)