# -------------------------------------------------------
# FitCom - AI Health Coach
# Author: Anand Kumar
#
# Purpose:
# Generate human-readable fitness insights based
# on participant body composition data.
# -------------------------------------------------------

import pandas as pd


def generate_insights(df):

    insights = []

    # Only numeric columns
    numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns

    if numeric_cols.empty:
        return ["No numeric data available for analysis."]

    # -----------------------------
    # Group averages
    # -----------------------------
    for col in numeric_cols:

        avg = df[col].mean()

        insights.append(
            f"Average {col} across participants is {round(avg,2)}."
        )

    # -----------------------------
    # Best and worst performers
    # -----------------------------
    for col in numeric_cols:

        best = df.loc[df[col].idxmax()]
        worst = df.loc[df[col].idxmin()]

        insights.append(
            f"{best['Name']} shows the highest {col} ({best[col]})."
        )

        insights.append(
            f"{worst['Name']} shows the lowest {col} ({worst[col]})."
        )

    return insights