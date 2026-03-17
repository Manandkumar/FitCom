# ============================================================
# FitCom - Data Storage Module (CSV Based)
# ============================================================

import pandas as pd
import os

FILE_NAME = "fitcom_reports.csv"


# ------------------------------------------------------------
# Save Report
# ------------------------------------------------------------

def save_report(name, metrics):

    # Ensure Name is stored (CRITICAL)
    metrics["Name"] = name

    new_row = pd.DataFrame([metrics])

    if os.path.exists(FILE_NAME):
        existing = pd.read_csv(FILE_NAME)
        df = pd.concat([existing, new_row], ignore_index=True)
    else:
        df = new_row

    df.to_csv(FILE_NAME, index=False)


# ------------------------------------------------------------
# Load Reports (Grouped by Name)
# ------------------------------------------------------------

def load_reports():

    if not os.path.exists(FILE_NAME):
        return {}

    df = pd.read_csv(FILE_NAME)

    # Safety checks
    if df.empty or "Name" not in df.columns:
        return {}

    grouped = {}

    for name, group in df.groupby("Name"):
        grouped[name] = group.to_dict(orient="records")

    return grouped