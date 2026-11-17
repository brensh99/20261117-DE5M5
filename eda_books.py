import pandas as pd
from IPython.display import display

# =====================================
# 1. LOAD CLEANED SYSTEM BOOK DATA
# =====================================

df_books = pd.read_csv(
    r"C:\Users\Admin\Desktop\20261117-DE5M5\data\03_Library Systembook_Cleaned.csv"
)

print("ORIGINAL SYSTEM BOOK DATA")
display(df_books)


# =====================================
# 2. CLEAN CHECKOUT DATE
# REMOVE EXTRA QUOTATION MARKS
# =====================================

df_books['Book checkout'] = (
    df_books['Book checkout']
    .astype(str)
    .str.replace('"', '', regex=False)
    .str.strip()
)


# =====================================
# 3. CONVERT BOTH DATE COLUMNS
# =====================================

df_books['Book checkout'] = pd.to_datetime(
    df_books['Book checkout'],
    format='%d/%m/%Y',
    errors='coerce'
)

df_books['Book Returned'] = pd.to_datetime(
    df_books['Book Returned'],
    format='%d/%m/%Y',
    errors='coerce'
)


# =====================================
# 4. CHECK DATE VALIDITY
# CHECKOUT MUST BE BEFORE RETURN
# =====================================

df_books['Date Valid'] = (
    (df_books['Book checkout'] < df_books['Book Returned']) &
    df_books['Book checkout'].notna() &
    df_books['Book Returned'].notna()
)


# =====================================
# 5. SEPARATE VALID AND INVALID DATA
# =====================================

df_books_valid = df_books[
    df_books['Date Valid'] == True
].copy()

df_books_invalid = df_books[
    df_books['Date Valid'] == False
].copy()


# =====================================
# 6. DISPLAY VALID RECORDS
# =====================================

print("SYSTEM BOOK - VALID DATES")
display(df_books_valid)


# =====================================
# 7. DISPLAY INVALID RECORDS
# =====================================

print("SYSTEM BOOK - INVALID DATES")
display(df_books_invalid)


# =====================================
# 8. SAVE VALID RECORDS
# =====================================

df_books_valid.drop(columns=['Date Valid']).to_csv(
    r"C:\Users\Admin\Desktop\20261117-DE5M5\data\03_Library Systembook_Cleaned_2.csv",
    index=False
)


# =====================================
# 9. SAVE INVALID RECORDS
# =====================================

df_books_invalid.drop(columns=['Date Valid']).to_csv(
    r"C:\Users\Admin\Desktop\20261117-DE5M5\data\03_Library Systembook_Invalid_Dates.csv",
    index=False
)


# =====================================
# 10. DATA QUALITY SUMMARY
# =====================================

print("DATA QUALITY SUMMARY")
print("---------------------")
print("Total records:", len(df_books))
print("Valid records:", len(df_books_valid))
print("Invalid records:", len(df_books_invalid))

print("\nBoth output files saved successfully!")