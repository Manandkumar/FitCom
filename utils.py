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

def calculate_health_score(data):
    score = 0

    # BMI
    bmi = data.get("BMI", 0)
    if 18.5 <= bmi <= 24.9:
        score += 20
    elif 25 <= bmi <= 29.9:
        score += 10

    # Body Fat
    bf = data.get("BodyFat", 0)
    if 10 <= bf <= 20:
        score += 20
    elif 20 < bf <= 25:
        score += 10

    # Muscle Mass
    mm = data.get("MuscleMass", 0)
    if mm > 40:
        score += 15

    # Visceral Fat
    vf = data.get("VisceralFat", 0)
    if vf < 10:
        score += 15

    # BMR
    bmr = data.get("BMR", 0)
    if bmr > 1200:
        score += 10

    # Weight consistency
    wt = data.get("Weight", 0)
    if 50 <= wt <= 90:
        score += 10

    return min(score, 100)