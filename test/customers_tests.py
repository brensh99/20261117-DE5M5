
import unittest
import pandas as pd
import tempfile

from pathlib import Path
from unittest.mock import patch
from io import StringIO

import customers_functions as cf


class TestCustomerCleaning(unittest.TestCase):

    # =====================================
    # 1. TEST LOAD CUSTOMERS - GOOD DATA
    # =====================================

    def test_load_customers(self):

        with tempfile.TemporaryDirectory() as folder:

            file_path = Path(folder) / "customers.csv"

            df = pd.DataFrame({
                "Customer ID": [1, 2],
                "Customer Name": ["John", "Sarah"]
            })

            df.to_csv(file_path, index=False)

            result = cf.load_customers(file_path)

            self.assertEqual(len(result), 2)
            self.assertIn("Customer ID", result.columns)


    # =====================================
    # 2. TEST LOAD CUSTOMERS - BAD FILE
    # =====================================

    def test_load_customers_bad_file(self):

        with self.assertRaises(FileNotFoundError):

            cf.load_customers("missing_customers.csv")


    # =====================================
    # 3. TEST VALIDATE CUSTOMERS - GOOD DATA
    # =====================================

    def test_validate_customers(self):

        df = pd.DataFrame({
            "Customer ID": [1, 2],
            "Customer Name": ["John", "Sarah"]
        })

        result = cf.validate_customers(df)

        self.assertEqual(len(result), 2)


    # =====================================
    # 4. TEST VALIDATE CUSTOMERS - BAD DATA
    # =====================================

    def test_validate_customers_missing_column(self):

        df = pd.DataFrame({
            "Customer ID": [1, 2],
            "Email": ["john@email.com", "sarah@email.com"]
        })

        with self.assertRaisesRegex(
            ValueError,
            "Missing required column: Customer Name"
        ):

            cf.validate_customers(df)


    # =====================================
    # 5. TEST VALIDATE CUSTOMERS - EMPTY DATA
    # =====================================

    def test_validate_customers_empty(self):

        df = pd.DataFrame(columns=[
            "Customer ID",
            "Customer Name"
        ])

        with self.assertRaisesRegex(
            ValueError,
            "Customer dataset is empty"
        ):

            cf.validate_customers(df)


    # =====================================
    # 6. TEST DROP NULLS - GOOD RESULT
    # =====================================

    def test_drop_nulls(self):

        df = pd.DataFrame({
            "Customer ID": [1, 2, 3],
            "Customer Name": ["John", None, "Sarah"]
        })

        result = cf.drop_nulls(df)

        self.assertEqual(len(result), 2)

        self.assertFalse(result.isnull().values.any())


    # =====================================
    # 7. TEST DROP NULLS - BAD EXPECTATION
    # =====================================

    @unittest.expectedFailure
    def test_drop_nulls_bad_expectation(self):

        df = pd.DataFrame({
            "Customer ID": [1, 2, 3],
            "Customer Name": ["John", None, "Sarah"]
        })

        result = cf.drop_nulls(df)

        # Deliberately incorrect expectation.
        # The actual result contains 2 rows.

        self.assertEqual(len(result), 1)


    # =====================================
    # 8. TEST SAVE CUSTOMERS
    # =====================================

    def test_save_customers(self):

        with tempfile.TemporaryDirectory() as folder:

            output_file = Path(folder) / "cleaned.csv"

            df = pd.DataFrame({
                "Customer ID": [1, 2],
                "Customer Name": ["John", "Sarah"]
            })

            cf.save_customers(df, output_file)

            self.assertTrue(output_file.exists())

            saved_data = pd.read_csv(output_file)

            self.assertEqual(len(saved_data), 2)


    # =====================================
    # 9. TEST COMPLETE MAIN PROGRAM
    # =====================================

    def test_main_program(self):

        with tempfile.TemporaryDirectory() as folder:

            test_folder = Path(folder)

            input_file = test_folder / "customers.csv"
            output_file = test_folder / "cleaned.csv"

            df = pd.DataFrame({
                "Customer ID": [1, 2, 3],
                "Customer Name": ["John", None, "Sarah"]
            })

            df.to_csv(input_file, index=False)

            with patch.object(
                cf,
                "create_file_paths",
                return_value=(input_file, output_file)
            ):

                with patch("sys.stdout", new=StringIO()) as output:

                    cf.main()

                    captured_output = output.getvalue()

            self.assertTrue(output_file.exists())

            saved_data = pd.read_csv(output_file)

            self.assertEqual(len(saved_data), 2)

            self.assertIn(
                "Cleaned file saved successfully!",
                captured_output
            )


# =====================================
# 10. RUN ALL TESTS
# =====================================

if __name__ == "__main__":
    unittest.main(verbosity=2)
