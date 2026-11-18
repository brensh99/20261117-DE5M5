
import pandas as pd
from pathlib import Path


# =====================================
# 1. CREATE FILE PATHS
# =====================================

def create_file_paths():

    data_folder = Path(
        r"C:\Users\Admin\Desktop\20261117-DE5M5\data"
    )

    input_file = data_folder / "03_Library SystemCustomers.csv"

    output_file = data_folder / "03_Library SystemCustomers_Cleaned.csv"

    return input_file, output_file


# =====================================
# 2. LOAD CUSTOMER DATA
# =====================================

def load_customers(file_path):
    """Load customer data from a CSV file."""

    return pd.read_csv(file_path)


# =====================================
# 3. VALIDATE CUSTOMER DATA
# =====================================

def validate_customers(df):
    """Check that customer data has the required columns."""

    required_columns = ["Customer ID", "Customer Name"]

    for column in required_columns:

        if column not in df.columns:
            raise ValueError(
                f"Missing required column: {column}"
            )

    if df.empty:
        raise ValueError("Customer dataset is empty.")

    return df


# =====================================
# 4. REMOVE NULL VALUES
# =====================================

def drop_nulls(df):
    """Remove rows containing null values."""

    return df.dropna().copy()


# =====================================
# 5. SAVE CLEANED CUSTOMER DATA
# =====================================

def save_customers(df, output_file):
    """Save cleaned customer data to CSV."""

    df.to_csv(output_file, index=False)


# =====================================
# 6. MAIN PROGRAM
# =====================================

def main():

    # Create file paths
    input_file, output_file = create_file_paths()

    # Load customer data
    df = load_customers(input_file)

    print("CUSTOMERS DATA - BEFORE CLEANING")
    print(df)

    # Validate customer data
    df = validate_customers(df)

    # Remove null values
    df_cleaned = drop_nulls(df)

    print("\nCUSTOMERS DATA - AFTER CLEANING")
    print(df_cleaned)

    # Save cleaned data
    save_customers(df_cleaned, output_file)

    print("\nCleaned file saved successfully!")


# =====================================
# 7. RUN PROGRAM
# =====================================

if __name__ == "__main__":
    main()
