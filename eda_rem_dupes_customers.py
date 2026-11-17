import pandas as pd
from IPython.display import display

df = pd.read_csv(r"C:\Users\Admin\Desktop\20261117-DE5M5\data\03_Library SystemCustomers.csv")

print("CUSTOMERS DATA - BEFORE CLEANING")
display(df)

# Remove null values
df_cleaned = df.dropna()


print("CUSTOMERS DATA - AFTER CLEANING")
display(df_cleaned)


df_cleaned.to_csv(
    r"C:\Users\Admin\Desktop\20261117-DE5M5\data\03_Library SystemCustomers_Cleaned.csv",
    index=False
)

print("Cleaned file saved successfully!")