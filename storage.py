# -------------------------------------------------------
# FitCom - Data Storage Module
# Author: Anand Kumar
# -------------------------------------------------------

import pandas as pd
import os

FILE_NAME = "fitcom_reports.csv"


def save_report(name, metrics):

    metrics["Name"] = name

    df = pd.DataFrame([metrics])

    if os.path.exists(FILE_NAME):

        existing = pd.read_csv(FILE_NAME)

        df = pd.concat([existing, df], ignore_index=True)

    df.to_csv(FILE_NAME, index=False)