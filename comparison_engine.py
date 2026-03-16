# -------------------------------------------------------
# FitCom - Participant Comparison Engine
# Author: Anand Kumar
#
# Purpose:
# Compare participant body composition reports and
# generate metric-wise comparison insights.
#
# Handles OCR noise safely and automatically detects
# numeric fitness metrics for comparison.
# -------------------------------------------------------

import pandas as pd
import re


# -------------------------------------------------------
# Extract numeric value safely from OCR text
# -------------------------------------------------------

def extract_number(value):
    """
    Extract numeric value from OCR text safely.

    Example:
    '22.4 %' -> 22.4
    'Weight 66 kg' -> 66
    """

    if pd.isna(value):
        return None

    numbers = re.findall(r"\d+\.\d+|\d+", str(value))

    if numbers:
        return float(numbers[0])

    return None


# -------------------------------------------------------
# Group Analysis (Averages + Best/Worst Body Fat)
# -------------------------------------------------------

def analyze_group(df):

    results = {}

    if "BodyFat" not in df.columns or "Weight" not in df.columns:
        return {"error": "Required metrics not found"}

    df["BodyFatNum"] = df["BodyFat"].apply(extract_number)
    df["WeightNum"] = df["Weight"].apply(extract_number)

    clean_df = df.dropna(subset=["BodyFatNum", "WeightNum"])

    if clean_df.empty:
        return {"error": "No valid numeric data detected"}

    results["avg_bodyfat"] = clean_df["BodyFatNum"].mean()
    results["avg_weight"] = clean_df["WeightNum"].mean()

    best = clean_df.loc[clean_df["BodyFatNum"].idxmin()]
    worst = clean_df.loc[clean_df["BodyFatNum"].idxmax()]

    results["best_bodyfat"] = best["Name"]
    results["worst_bodyfat"] = worst["Name"]

    return results


# -------------------------------------------------------
# Full Metric Comparison
# -------------------------------------------------------

def compare_reports(df):
    """
    Compare every numeric metric across participants.
    """

    results = {}

    # Ignore non-metric columns
    ignore_cols = ["Name"]

    for column in df.columns:

        if column in ignore_cols:
            continue

        # Extract numeric values
        numeric_series = df[column].apply(extract_number)

        clean_series = numeric_series.dropna()

        if clean_series.empty:
            continue

        best_index = clean_series.idxmax()
        worst_index = clean_series.idxmin()

        results[column] = {

            "best_person": df.loc[best_index]["Name"],
            "best_value": clean_series.loc[best_index],

            "worst_person": df.loc[worst_index]["Name"],
            "worst_value": clean_series.loc[worst_index]
        }

    return results