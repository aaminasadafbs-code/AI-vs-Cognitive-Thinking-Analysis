# Import Required Libraries
import pandas as pd
import numpy as np
from scipy.stats import f_oneway

# Load the CSV file
df = pd.read_csv("C:\\Users\\CIPL\\Downloads\\AI\\AI_PROJECT\\Exploring the Relationship Between AI Usage and Cognitive Thinking_ A Survey-Based Study  (Responses) - Form responses 1.csv")

# -------------------------------
# AI Usage Classification (Q6)
# -------------------------------

def classify_ai_usage(response):
    if response in ["Never", "Rarely"]:
        return "Low"
    elif response == "Sometimes":
        return "Moderate"
    elif response in ["Often", "Very Often"]:
        return "High"
    else:
        return np.nan
df["AI_Group"] = df["  6. How often do you use AI tools?  "].apply(classify_ai_usage)

# ---------------------------------------------------
# Convert Cognitive Thinking Questions into Scores
# ---------------------------------------------------

score = {
    "Never":1,
    "Rarely":2,
    "Sometimes":3,
    "Often":4,
    "Always":5
}

reverse_score = {
    "Never":5,
    "Rarely":4,
    "Sometimes":3,
    "Often":2,
    "Always":1
}

q11 = "  11. When you receive an answer from AI, how often do you check whether the information is correct?  "
q12 = "12. How often do you try to solve a problem yourself before asking AI for help? Never"
q13 = "  13. When AI provides a solution, how often do you try to understand how that solution was reached?  "
q14 = "14. How often do you compare AI-generated information with other sources before using it? "
q19 = "  19. How often do you accept AI-generated answers without questioning them?  "
q20 = "  20. When AI gives an answer that differs from your own understanding, what do you usually do?  "
# Apply Scores

df["Q11"] = df[q11].map(score)
df["Q12"] = df[q12].map(score)
df["Q13"] = df[q13].map(score)
df["Q14"] = df[q14].map(score)
df["Q19"] = df[q19].map(reverse_score)

# Question 20 Score

q20_score = {
    "Trust AI immediately":1,
    "Usually trust AI":2,
    "Compare both viewpoints":3,
    "Usually trust my own understanding":4,
    "Trust my own understanding completely":5
}

df["Q20"] = df[q20].map(q20_score)

# ----------------------------------------
# Cognitive Thinking Score
# ----------------------------------------

df["Cognitive_Score"] = (
    df["Q11"] +
    df["Q12"] +
    df["Q13"] +
    df["Q14"] +
    df["Q19"] +
    df["Q20"]
)

# Remove Missing Values

df = df.dropna(subset=["AI_Group","Cognitive_Score"])

# ----------------------------------------
# Create Three Groups
# ----------------------------------------

low = df[df["AI_Group"]=="Low"]["Cognitive_Score"]

moderate = df[df["AI_Group"]=="Moderate"]["Cognitive_Score"]

high = df[df["AI_Group"]=="High"]["Cognitive_Score"]

# ----------------------------------------
# Perform One-Way ANOVA
# ----------------------------------------

F,p = f_oneway(low,moderate,high)

print("One-Way ANOVA Result")
print("--------------------")
print("F-value :",F)
print("P-value :",p)

# ----------------------------------------
# Decision
# ----------------------------------------

alpha = 0.05

if p < alpha:
    print("Reject Null Hypothesis")
else:
    print("Fail to Reject Null Hypothesis")