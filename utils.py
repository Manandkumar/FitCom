# ============================================================
# FitCom - Utility Functions
# Author: Anand Kumar
#
# Description:
# Contains reusable helper functions used across the
# FitCom analytics platform.
#
# Includes:
# • BMI calculation
# • Fitness score calculation
# • Health status indicators
# ============================================================


# ------------------------------------------------------------
# BMI Calculation
# ------------------------------------------------------------
# Calculates Body Mass Index.
#
# Formula:
# BMI = Weight (kg) / Height (m)^2
# ------------------------------------------------------------

def calculate_bmi(weight, height_in):

    if height_in == 0:
        return None

    height_m = height_in * 0.0254

    bmi = weight / (height_m ** 2)

    return round(bmi, 2)


# ------------------------------------------------------------
# Fitness Score Calculation
# ------------------------------------------------------------
# Computes an overall fitness score based on key metrics.
#
# Metrics considered:
# • BMI
# • Body Fat %
# • Visceral Fat
# • Body Water %
#
# Output range:
# 0 - 100
# ------------------------------------------------------------

def calculate_fitness_score(row):

    score = 100

    if row["BMI"] > 25:
        score -= (row["BMI"] - 25) * 2

    if row["BodyFat"] > 20:
        score -= (row["BodyFat"] - 20) * 1.5

    if row["VisceralFat"] > 10:
        score -= (row["VisceralFat"] - 10) * 2

    if row["BodyWater"] < 50:
        score -= (50 - row["BodyWater"]) * 1.5

    return max(0, round(score))