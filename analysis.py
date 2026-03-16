# -------------------------------------------------------
# FitCom - Fitness Analysis Engine
# Author: Anand Kumar
# -------------------------------------------------------

def analyze(bodyfat):

    try:

        value = float(bodyfat.split()[0])

        if value > 25:
            return "⚠️ FitCom Insight: Body fat is high. Fat reduction recommended."

        elif value > 20:
            return "⚠️ FitCom Insight: Body fat slightly above optimal range."

        else:
            return "✅ FitCom Insight: Body fat is in a healthy range."

    except:

        return "FitCom could not analyze body fat value."