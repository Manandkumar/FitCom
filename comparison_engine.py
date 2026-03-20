# ============================================================
# FitCom - Comparison Engine (FINAL - SAFE)
# ============================================================

import pandas as pd


def compare_reports(df):

    if df.empty:
        return pd.DataFrame()

    # Select numeric columns safely
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    results = []

    for metric in numeric_cols:

        clean_df = df.dropna(subset=[metric])

        if clean_df.empty:
            continue

        try:
            best_idx = clean_df[metric].idxmax()
            worst_idx = clean_df[metric].idxmin()

            results.append({
                "Metric": metric,
                "Best Performer": clean_df.loc[best_idx].get("Name", "NA"),
                "Best Value": round(clean_df.loc[best_idx][metric], 2),
                "Lowest Performer": clean_df.loc[worst_idx].get("Name", "NA"),
                "Lowest Value": round(clean_df.loc[worst_idx][metric], 2)
            })

        except Exception:
            continue

    return pd.DataFrame(results)