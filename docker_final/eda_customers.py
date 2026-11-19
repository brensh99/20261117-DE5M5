import pandas as pd

df = pd.read_csv(r"/app/03_Library_SystemCustomers.csv")

print("CUSTOMERS DATA - BEFORE CLEANING")
print(df)

# Remove null values
df_cleaned = df.dropna()


print("CUSTOMERS DATA - AFTER CLEANING")
print(df_cleaned)


df_cleaned.to_csv(
    r"/app/output/03_Library_SystemCustomers_Cleaned.csv",
    index=False
)

print("Cleaned file saved successfully!")