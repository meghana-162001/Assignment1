# -*- coding: utf-8 -*-
"""dataanalysis2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10frHddtJPEX5lIn2eWLLVXYF2_9Dyahw
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from sklearn.preprocessing import LabelEncoder

# Ensure output directory exists
output_dir = "output"
os.makedirs(output_dir, exist_ok=True)

# Load cleaned dataset
cleaned_data_path = "/content/cleaned_student_performance.csv"  # Adjust if needed
df = pd.read_csv(cleaned_data_path)

# Print column names to verify structure
print("Available columns in dataset:", df.columns)

# 🔹 Convert categorical variables to numeric encoding using LabelEncoder
label_encoders = {}
for col in df.select_dtypes(include=["object"]).columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# 🔹 Compute and save detailed summary statistics
summary_stats = df.describe().T  # Transposed for better readability
summary_stats["median"] = df.median()
summary_stats["std_dev"] = df.std()
summary_stats["mode"] = df.mode().iloc[0]
summary_stats.to_csv(os.path.join(output_dir, "summary_statistics.csv"))

# 🔹 Compute and save correlation matrix
correlation_matrix = df.corr()
correlation_matrix.to_csv(os.path.join(output_dir, "correlation_matrix.csv"))

print(" Data analysis completed. Results saved.")

# 🔹 **Additional Analysis**
highest_scores = df[["math_score", "reading_score", "writing_score"]].max()
lowest_scores = df[["math_score", "reading_score", "writing_score"]].min()
average_scores = df[["math_score", "reading_score", "writing_score"]].mean()

# Save additional analysis to a text file
analysis_file = os.path.join(output_dir, "analysis_summary.txt")
with open(analysis_file, "w") as f:
    f.write("Student Performance Analysis\n")
    f.write("=============================\n\n")
    f.write(f"Highest Scores:\n{highest_scores.to_string()}\n\n")
    f.write(f"Lowest Scores:\n{lowest_scores.to_string()}\n\n")
    f.write(f"Average Scores:\n{average_scores.to_string()}\n\n")

print(" Additional numerical analysis saved.")

#  **Visualization 1: Box Plot - Math Score Distribution by Gender**
plt.figure(figsize=(6, 4))
sns.boxplot(x=df["gender"], y=df["math_score"], palette="coolwarm")
plt.title("Math Score Distribution by Gender")
plt.xlabel("Gender (Encoded)")
plt.ylabel("Math Score")
plt.grid()
plt.savefig(os.path.join(output_dir, "gender_math_score_distribution.png"))
plt.show()

#  **Visualization 2: Bar Chart - Parental Education Level vs Average Scores**
plt.figure(figsize=(8, 4))
df.groupby("parental_level_of_education")[["math_score", "reading_score", "writing_score"]].mean().plot(kind="bar", colormap="viridis")
plt.title("Parental Education Level vs Average Scores")
plt.ylabel("Average Score")
plt.xticks(rotation=45)
plt.grid()
plt.savefig(os.path.join(output_dir, "parental_education_vs_scores.png"))
plt.show()

#  **Visualization 3: Facet Grid - Test Preparation Course vs Scores**
g = sns.FacetGrid(df, col="test_preparation_course", height=4, aspect=1.2)
g.map_dataframe(sns.histplot, x="math_score", kde=True, bins=20, color="teal", alpha=0.6)
g.set_axis_labels("Math Score", "Frequency")
g.fig.suptitle("Test Preparation Course vs Math Score Distribution", fontsize=12)
plt.savefig(os.path.join(output_dir, "test_prep_vs_scores.png"))
plt.show()

#  **Visualization 4: Pie Chart - Lunch Type Distribution**
plt.figure(figsize=(6, 6))
df["lunch"].value_counts().plot(kind="pie", autopct="%1.1f%%", cmap="coolwarm", startangle=90, explode=[0.05, 0])
plt.title("Lunch Type Distribution")
plt.ylabel("")
plt.savefig(os.path.join(output_dir, "lunch_type_distribution.png"))
plt.show()

#  **Visualization 5: KDE Plot - Math Score Density by Gender**
plt.figure(figsize=(8, 4))
sns.kdeplot(data=df, x="math_score", hue="gender", fill=True, common_norm=False, palette="coolwarm", alpha=0.5)
plt.title("Math Score Density by Gender")
plt.xlabel("Math Score")
plt.ylabel("Density")
plt.grid()
plt.savefig(os.path.join(output_dir, "math_score_density_gender.png"))
plt.show()

print(" All visualizations saved in 'output/' directory.")