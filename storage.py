# ============================================================
# FitCom - Data Storage Module
# Author: Anand Kumar
#
# Description:
# Handles persistent storage of body composition reports.
# Data is stored in a CSV file that acts as a lightweight
# database for the FitCom dashboard.
#
# Responsibilities:
# • Save new reports
# • Append data to existing dataset
# • Maintain structured dataset format
# ============================================================

import pandas as pd
import os

FILE_NAME = "fitcom_reports.csv"


# ------------------------------------------------------------
# Save Report
# ------------------------------------------------------------
# Adds a new user report to the CSV database.
#
# Parameters
# ----------
# name : str
#     Name of the participant
#
# metrics : dict
#     Dictionary containing body composition metrics
#
# Example
# -------
# save_report("Anand", metrics_dict)
# ------------------------------------------------------------

def save_report(name, metrics):

    new_row = pd.DataFrame([metrics])

    # If the CSV already exists, append new data
    if os.path.exists(FILE_NAME):

        existing = pd.read_csv(FILE_NAME)

        df = pd.concat([existing, new_row], ignore_index=True)

    else:

        df = new_row

    df.to_csv(FILE_NAME, index=False)