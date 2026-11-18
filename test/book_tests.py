
import unittest
import pandas as pd
import tempfile
from pathlib import Path
from unittest.mock import patch
from io import StringIO

import library_cleaning as lc


class TestLibraryCleaning(unittest.TestCase):

    # =====================================
    # 1. TEST LOAD BOOKS
    # =====================================

    def test_load_books(self):

        with tempfile.TemporaryDirectory() as folder:

            file_path = Path(folder) / "books.csv"

            df = pd.DataFrame({
                "Book checkout": ["01/01/2026"],
                "Book Returned": ["05/01/2026"]
            })

            df.to_csv(file_path, index=False)

            result = lc.load_books(file_path)

            self.assertEqual(len(result), 1)
            self.assertIn("Book checkout", result.columns)


    # =====================================
    # 2. TEST CLEAN CHECKOUT DATE
    # =====================================

    def test_clean_checkout_date(self):

        df = pd.DataFrame({
            "Book checkout": ['" 01/01/2026 "']
        })

        result = lc.clean_checkout_date(df)

        self.assertEqual(
            result["Book checkout"].iloc[0],
            "01/01/2026"
        )


    # =====================================
    # 3. TEST CONVERT DATES
    # =====================================

    def test_convert_dates(self):

        df = pd.DataFrame({
            "Book checkout": ["01/01/2026"],
            "Book Returned": ["05/01/2026"]
        })

        result = lc.convert_dates(df)

        self.assertTrue(
            pd.api.types.is_datetime64_any_dtype(
                result["Book checkout"]
            )
        )

        self.assertTrue(
            pd.api.types.is_datetime64_any_dtype(
                result["Book Returned"]
            )
        )


    # =====================================
    # 4. TEST VALIDATE DATES
    # =====================================

    def test_validate_dates(self):

        df = pd.DataFrame({
            "Book checkout": pd.to_datetime([
                "01/01/2026",
                "10/01/2026",
                None
            ]),
            "Book Returned": pd.to_datetime([
                "05/01/2026",
                "05/01/2026",
                "15/01/2026"
            ])
        })

        result = lc.validate_dates(df)

        expected = [True, False, False]

        self.assertEqual(
            result["Date Valid"].tolist(),
            expected
        )


    # =====================================
    # 5. TEST SPLIT VALID AND INVALID
    # =====================================

    def test_split_valid_invalid(self):

        df = pd.DataFrame({
            "Book checkout": pd.to_datetime([
                "01/01/2026",
                "10/01/2026"
            ]),
            "Book Returned": pd.to_datetime([
                "05/01/2026",
                "05/01/2026"
            ]),
            "Date Valid": [True, False]
        })

        valid, invalid = lc.split_valid_invalid(df)

        self.assertEqual(len(valid), 1)
        self.assertEqual(len(invalid), 1)

        self.assertTrue(valid["Date Valid"].all())
        self.assertFalse(invalid["Date Valid"].any())


    # =====================================
    # 6. TEST SAVE OUTPUT FILES
    # =====================================

    def test_save_books(self):

        with tempfile.TemporaryDirectory() as folder:

            valid_file = Path(folder) / "valid.csv"
            invalid_file = Path(folder) / "invalid.csv"

            valid = pd.DataFrame({
                "Book checkout": ["01/01/2026"],
                "Date Valid": [True]
            })

            invalid = pd.DataFrame({
                "Book checkout": ["10/01/2026"],
                "Date Valid": [False]
            })

            lc.save_books(
                valid,
                invalid,
                valid_file,
                invalid_file
            )

            self.assertTrue(valid_file.exists())
            self.assertTrue(invalid_file.exists())

            saved_valid = pd.read_csv(valid_file)
            saved_invalid = pd.read_csv(invalid_file)

            self.assertEqual(len(saved_valid), 1)
            self.assertEqual(len(saved_invalid), 1)

            self.assertNotIn("Date Valid", saved_valid.columns)
            self.assertNotIn("Date Valid", saved_invalid.columns)


    # =====================================
    # 7. TEST DATA QUALITY SUMMARY
    # =====================================

    def test_data_quality_summary(self):

        original = pd.DataFrame({
            "Book": ["A", "B", "C"]
        })

        valid = pd.DataFrame({
            "Book": ["A", "B"]
        })

        invalid = pd.DataFrame({
            "Book": ["C"]
        })

        result = lc.data_quality_summary(
            original,
            valid,
            invalid
        )

        self.assertEqual(result["Total records"], 3)
        self.assertEqual(result["Valid records"], 2)
        self.assertEqual(result["Invalid records"], 1)


    # =====================================
    # 8. TEST COMPLETE MAIN PROGRAM
    # =====================================

    def test_main_program(self):

        with tempfile.TemporaryDirectory() as folder:

            test_folder = Path(folder)

            input_file = (
                test_folder /
                "03_Library Systembook_Cleaned.csv"
            )

            df = pd.DataFrame({
                "Book checkout": [
                    "01/01/2026",
                    "10/01/2026"
                ],
                "Book Returned": [
                    "05/01/2026",
                    "05/01/2026"
                ]
            })

            df.to_csv(input_file, index=False)

            # Replace the original folder with
            # the temporary test folder.

            with patch.object(
                lc,
                "Path",
                return_value=test_folder
            ):

                with patch("sys.stdout", new=StringIO()) as output:

                    lc.main()

                    captured_output = output.getvalue()

            valid_file = (
                test_folder /
                "03_Library Systembook_Cleaned_2.csv"
            )

            invalid_file = (
                test_folder /
                "03_Library Systembook_Invalid_Dates.csv"
            )

            self.assertTrue(valid_file.exists())
            self.assertTrue(invalid_file.exists())

            valid = pd.read_csv(valid_file)
            invalid = pd.read_csv(invalid_file)

            self.assertEqual(len(valid), 1)
            self.assertEqual(len(invalid), 1)

            self.assertIn(
                "DATA QUALITY SUMMARY",
                captured_output
            )

            self.assertIn(
                "Total records: 2",
                captured_output
            )


# =====================================
# RUN ALL TESTS
# =====================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
