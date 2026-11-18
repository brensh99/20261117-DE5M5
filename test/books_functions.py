
import pandas as pd
from pathlib import Path


# =====================================
# 1. LOAD DATA
# =====================================

def load_books(file_path):
    """Load library book data from a CSV file."""
    return pd.read_csv(file_path)


# =====================================
# 2. CLEAN CHECKOUT DATE
# =====================================

def clean_checkout_date(df):
    """Remove quotation marks and whitespace from checkout dates."""
    df = df.copy()

    df['Book checkout'] = (
        df['Book checkout']
        .astype(str)
        .str.replace('"', '', regex=False)
        .str.strip()
    )

    return df


# =====================================
# 3. CONVERT DATE COLUMNS
# =====================================

def convert_dates(df):
    """Convert checkout and returned dates to datetime."""
    df = df.copy()

    df['Book checkout'] = pd.to_datetime(
        df['Book checkout'],
        format='%d/%m/%Y',
        errors='coerce'
    )

    df['Book Returned'] = pd.to_datetime(
        df['Book Returned'],
        format='%d/%m/%Y',
        errors='coerce'
    )

    return df


# =====================================
# 4. VALIDATE DATES
# =====================================

def validate_dates(df):
    """Check that checkout dates are before return dates."""
    df = df.copy()

    df['Date Valid'] = (
        (df['Book checkout'] < df['Book Returned']) &
        df['Book checkout'].notna() &
        df['Book Returned'].notna()
    )

    return df


# =====================================
# 5. SEPARATE VALID AND INVALID DATA
# =====================================

def split_valid_invalid(df):
    """Separate records into valid and invalid datasets."""

    valid = df[df['Date Valid']].copy()
    invalid = df[~df['Date Valid']].copy()

    return valid, invalid


# =====================================
# 6. SAVE OUTPUT FILES
# =====================================

def save_books(valid, invalid, valid_path, invalid_path):

    valid.drop(columns=['Date Valid']).to_csv(
        valid_path,
        index=False
    )

    invalid.drop(columns=['Date Valid']).to_csv(
        invalid_path,
        index=False
    )


# =====================================
# 7. DATA QUALITY SUMMARY
# =====================================

def data_quality_summary(original, valid, invalid):

    summary = {
        'Total records': len(original),
        'Valid records': len(valid),
        'Invalid records': len(invalid)
    }

    return summary


# =====================================
# 8. MAIN PROGRAM
# =====================================

def main():

    data_folder = Path(
        r"C:\Users\Admin\Desktop\20261117-DE5M5\data"
    )

    input_file = data_folder / "03_Library Systembook_Cleaned.csv"

    valid_file = data_folder / "03_Library Systembook_Cleaned_2.csv"

    invalid_file = data_folder / "03_Library Systembook_Invalid_Dates.csv"

    # Load data
    df_books = load_books(input_file)

    # Clean and process dates
    df_books = clean_checkout_date(df_books)
    df_books = convert_dates(df_books)
    df_books = validate_dates(df_books)

    # Separate records
    valid, invalid = split_valid_invalid(df_books)

    # Save results
    save_books(valid, invalid, valid_file, invalid_file)

    # Display summary
    summary = data_quality_summary(df_books, valid, invalid)

    print("\nDATA QUALITY SUMMARY")
    print("---------------------")

    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nBoth output files saved successfully!")


if __name__ == "__main__":
    main()
