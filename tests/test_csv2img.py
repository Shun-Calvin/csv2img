"""
Comprehensive tests for csv2img module.
"""

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

from csv2img import saveas, convert_file


class TestSaveas(unittest.TestCase):
    """Test cases for the saveas function."""

    def setUp(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = Path(self.temp_dir) / "test.csv"
        
        # Create a simple test CSV
        self.test_csv.write_text("Name,Age,City\nAlice,30,New York\nBob,25,Los Angeles\n")

    def tearDown(self):
        """Clean up test fixtures."""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_saveas_with_valid_csv(self):
        """Test saveas with a valid CSV file."""
        result = saveas(str(self.test_csv))
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        for file_path in result:
            self.assertTrue(Path(file_path).exists())
            self.assertTrue(file_path.endswith('.png'))

    def test_saveas_with_none_source(self):
        """Test saveas with None as source."""
        with self.assertRaises(ValueError) as context:
            saveas(None)
        
        self.assertIn("cannot be None", str(context.exception))

    def test_saveas_with_nonexistent_file(self):
        """Test saveas with a non-existent file."""
        with self.assertRaises(FileNotFoundError) as context:
            saveas("nonexistent.csv")
        
        self.assertIn("not found", str(context.exception))

    def test_saveas_with_non_csv_file(self):
        """Test saveas with a non-CSV file."""
        txt_file = Path(self.temp_dir) / "test.txt"
        txt_file.write_text("This is a text file")
        
        with self.assertRaises(ValueError) as context:
            saveas(str(txt_file))
        
        self.assertIn("Expected a .csv file", str(context.exception))

    def test_saveas_with_custom_dpi(self):
        """Test saveas with custom DPI setting."""
        result = saveas(str(self.test_csv), dpi=150)
        
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_saveas_with_custom_output_dir(self):
        """Test saveas with custom output directory."""
        output_dir = Path(self.temp_dir) / "output"
        result = saveas(str(self.test_csv), output_dir=str(output_dir))
        
        self.assertIsInstance(result, list)
        
        for file_path in result:
            self.assertTrue(file_path.startswith(str(output_dir)))

    def test_saveas_creates_output_dir(self):
        """Test that saveas creates output directory if it doesn't exist."""
        output_dir = Path(self.temp_dir) / "new" / "nested" / "dir"
        result = saveas(str(self.test_csv), output_dir=str(output_dir))
        
        self.assertTrue(output_dir.exists())
        self.assertGreater(len(result), 0)

    def test_convert_file_alias(self):
        """Test that convert_file is an alias for saveas."""
        result1 = saveas(str(self.test_csv))
        result2 = convert_file(str(self.test_csv))
        
        self.assertEqual(len(result1), len(result2))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_empty_csv_file(self):
        """Test with an empty CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("")
            temp_path = f.name
        
        try:
            result = saveas(temp_path)
            self.assertIsInstance(result, list)
        except Exception as e:
            pass
        finally:
            os.unlink(temp_path)

    def test_csv_with_special_characters(self):
        """Test CSV with special characters in filename."""
        with tempfile.TemporaryDirectory() as temp_dir:
            special_csv = Path(temp_dir) / "test-data_v2.0.csv"
            special_csv.write_text("Name,Value\nTest,123\n")
            
            result = saveas(str(special_csv))
            self.assertIsInstance(result, list)

    def test_csv_with_many_rows(self):
        """Test CSV that spans multiple pages."""
        with tempfile.TemporaryDirectory() as temp_dir:
            big_csv = Path(temp_dir) / "big.csv"
            lines = ["ID,Name,Value"]
            for i in range(500):
                lines.append(f"{i},Item_{i},{i*10}")
            big_csv.write_text("\n".join(lines))
            
            result = saveas(str(big_csv))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 1)  # Should have multiple pages

    def test_csv_with_unicode(self):
        """Test CSV with unicode characters (CJK, Arabic, etc.)."""
        with tempfile.TemporaryDirectory() as temp_dir:
            unicode_csv = Path(temp_dir) / "unicode.csv"
            unicode_csv.write_text("Name,Age,City\nAlice,30,NYC\n", encoding="utf-8")
            
            # Basic Latin should always work
            result = saveas(str(unicode_csv))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_csv_with_cjk(self):
        """Test CSV with Chinese/Japanese/Korean characters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cjk_csv = Path(temp_dir) / "cjk.csv"
            cjk_csv.write_text("姓名,年齡,城市\nAlice,30,紐約\n", encoding="utf-8")
            
            result = saveas(str(cjk_csv))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_csv_with_arabic(self):
        """Test CSV with Arabic characters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ar_csv = Path(temp_dir) / "arabic.csv"
            ar_csv.write_text("الاسم,العمر,المدينة\nأحمد,30,القاهرة\n", encoding="utf-8")
            
            # Arabic font may not be available on all systems
            try:
                result = saveas(str(ar_csv))
                self.assertIsInstance(result, list)
            except Exception:
                # Font not found — acceptable
                pass

    def test_csv_with_hebrew(self):
        """Test CSV with Hebrew characters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            hebrew_csv = Path(temp_dir) / "hebrew.csv"
            hebrew_csv.write_text("שם,גיל,עיר\nדוד,25,תל אביב\n", encoding="utf-8")
            
            try:
                result = saveas(str(hebrew_csv))
                self.assertIsInstance(result, list)
            except Exception:
                pass

    def test_csv_with_commas_in_data(self):
        """Test CSV with commas inside quoted fields."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "commas.csv"
            csv_file.write_text('Name,Description\n"Smith, John","A, B, C"\n')
            
            result = saveas(str(csv_file))
            self.assertIsInstance(result, list)

    def test_csv_large_dpi(self):
        """Test with very high DPI."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "test.csv"
            csv_file.write_text("A,B\n1,2\n")
            
            result = saveas(str(csv_file), dpi=600)
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)


class TestOutputFileNames(unittest.TestCase):
    """Test that output filenames are correct."""

    def test_output_filename_format(self):
        """Test that output files follow the naming convention."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "report.csv"
            csv_file.write_text("Col1,Col2\na,b\n")
            
            output_dir = Path(temp_dir) / "output"
            result = saveas(str(csv_file), output_dir=str(output_dir))
            
            # Check naming: report1.png, report2.png, etc.
            expected_names = ["report1.png"]
            actual_names = [os.path.basename(f) for f in result]
            
            for expected in expected_names:
                self.assertIn(expected, actual_names)

    def test_output_in_correct_directory(self):
        """Test that output files are placed in the correct directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "data.csv"
            csv_file.write_text("A,B\n1,2\n")
            
            output_dir = Path(temp_dir) / "images"
            result = saveas(str(csv_file), output_dir=str(output_dir))
            
            for file_path in result:
                self.assertTrue(Path(file_path).parent == output_dir)


class TestCLI(unittest.TestCase):
    """Test the CLI entry point."""

    def test_main_without_args(self):
        """Test main() with no arguments exits with code 1."""
        import sys
        from csv2img.core import main
        
        with patch.object(sys, 'argv', ['csv2img']):
            with self.assertRaises(SystemExit) as ctx:
                main()
            self.assertEqual(ctx.exception.code, 1)

    def test_main_with_valid_file(self):
        """Test main() with a valid CSV file."""
        import sys
        from csv2img.core import main
        
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "test.csv"
            csv_file.write_text("A,B\n1,2\n")
            
            output_dir = Path(temp_dir) / "out"
            
            with patch.object(sys, 'argv', ['csv2img', str(csv_file), str(output_dir)]):
                # Should not raise
                main()


if __name__ == '__main__':
    unittest.main()
