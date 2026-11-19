
import pandas as pd

# ==========================================
# 1. SET FILE PATHS
# ==========================================

folder = r"C:\Users\Admin\Desktop\20261117-DE5M5\final"

input_file = folder + r"\03_Library_SystemCustomers.csv"
cleaned_file = folder + r"\03_Library_SystemCustomers_Cleaned.csv"
metrics_file = folder + r"\03_Library_SystemCustomers_Metrics.csv"

# ==========================================
# 2. LOAD CUSTOMER DATA
# ==========================================

df = pd.read_csv(input_file)

print("CUSTOMERS DATA - BEFORE CLEANING")
print(df)

# ==========================================
# 3. CALCULATE METRICS BEFORE CLEANING
# ==========================================

rows_before = len(df)
columns_before = len(df.columns)
missing_values_before = df.isnull().sum().sum()

# ==========================================
# 4. CLEAN CUSTOMER DATA
# ==========================================

df_cleaned = df.dropna()

print("\nCUSTOMERS DATA - AFTER CLEANING")
print(df_cleaned)

# ==========================================
# 5. CALCULATE METRICS AFTER CLEANING
# ==========================================

rows_after = len(df_cleaned)
missing_values_after = df_cleaned.isnull().sum().sum()

rows_removed = rows_before - rows_after

cleaning_percentage = (
    (rows_removed / rows_before) * 100
    if rows_before > 0 else 0
)

rows_retained_percentage = (
    (rows_after / rows_before) * 100
    if rows_before > 0 else 0
)

# ==========================================
# 6. DISPLAY CLEANING METRICS
# ==========================================

print("\n========== DATA CLEANING METRICS ==========")

print("Rows before cleaning:", rows_before)
print("Rows after cleaning:", rows_after)
print("Columns:", columns_before)
print("Missing values before:", missing_values_before)
print("Missing values after:", missing_values_after)
print("Rows removed:", rows_removed)
print("Cleaning percentage:", round(cleaning_percentage, 2), "%")
print("Rows retained:", round(rows_retained_percentage, 2), "%")

print("===========================================")

# ==========================================
# 7. SAVE CLEANED CUSTOMER DATA
# ==========================================

df_cleaned.to_csv(
    cleaned_file,
    index=False
)

# ==========================================
# 8. CREATE POWER BI METRICS DATASET
# ==========================================

metrics = pd.DataFrame({
    "Dataset": ["Library System Customers"],
    "Rows_Before_Cleaning": [rows_before],
    "Rows_After_Cleaning": [rows_after],
    "Columns": [columns_before],
    "Missing_Values_Before": [missing_values_before],
    "Missing_Values_After": [missing_values_after],
    "Rows_Removed": [rows_removed],
    "Cleaning_Percentage": [round(cleaning_percentage, 2)],
    "Rows_Retained_Percentage": [round(rows_retained_percentage, 2)]
})

# ==========================================
# 9. SAVE METRICS FOR POWER BI
# ==========================================

metrics.to_csv(
    metrics_file,
    index=False
)

# ==========================================
# 10. CONFIRM SAVED FILES
# ==========================================

print("\n========== FILES SAVED SUCCESSFULLY ==========")
print("Original file:", input_file)
print("Cleaned file:", cleaned_file)
print("Metrics file:", metrics_file)
print("==============================================")
