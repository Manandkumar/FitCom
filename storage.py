# ============================================================
# FitCom - Data Storage Module (CSV Based)
# ============================================================

import pandas as pd
import os

FILE_NAME = "fitcom_reports.csv"


# ------------------------------------------------------------
# Save Report
# ------------------------------------------------------------
# Adds a new record to CSV
# Ensures Name column exists
# ------------------------------------------------------------

def save_report(name, metrics):

    # Ensure Name is always present
    metrics["Name"] = name

    new_row = pd.DataFrame([metrics])

    try:
        if os.path.exists(FILE_NAME):
            existing = pd.read_csv(FILE_NAME)
            df = pd.concat([existing, new_row], ignore_index=True)
        else:
            df = new_row

        df.to_csv(FILE_NAME, index=False)

    except Exception as e:
        print("Error saving report:", e)


# ------------------------------------------------------------
# Load Reports (Grouped by Name)
# ------------------------------------------------------------
# Returns:
# {
#   "Anand": [ {...}, {...} ],
#   "Rahul": [ {...} ]
# }
# ------------------------------------------------------------

def load_reports():

    if not os.path.exists(FILE_NAME):
        return {}

    try:
        df = pd.read_csv(FILE_NAME)

        # Safety checks
        if df.empty or "Name" not in df.columns:
            return {}

        grouped = {}

        for name, group in df.groupby("Name"):
            grouped[name] = group.to_dict(orient="records")

        return grouped

    except Exception as e:
        print("Error loading reports:", e)
        return {}


# ------------------------------------------------------------
# Delete Record (by index for a specific user)
# ------------------------------------------------------------
# Parameters:
# name  -> user name
# index -> index within user's records (not global index)
# ------------------------------------------------------------

def delete_record(name, index):

    if not os.path.exists(FILE_NAME):
        return

    try:
        df = pd.read_csv(FILE_NAME)

        if df.empty or "Name" not in df.columns:
            return

        # Filter user records
        user_df = df[df["Name"] == name]

        if user_df.empty:
            return

        # Validate index
        if index < 0 or index >= len(user_df):
            return

        # Get actual index in full dataframe
        actual_index = user_df.index[index]

        # Drop record
        df = df.drop(actual_index).reset_index(drop=True)

        # Save back
        df.to_csv(FILE_NAME, index=False)

    except Exception as e:
        print("Error deleting record:", e)