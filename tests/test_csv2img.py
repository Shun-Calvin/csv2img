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
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = Path(self.temp_dir) / "test.csv"
        self.test_csv.write_text("Name,Age,City\nAlice,30,New York\nBob,25,Los Angeles\n")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_saveas_with_valid_csv(self):
        result = saveas(str(self.test_csv))
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        for file_path in result:
            self.assertTrue(Path(file_path).exists())
            self.assertTrue(file_path.endswith('.png'))

    def test_saveas_with_none_source(self):
        with self.assertRaises(ValueError) as context:
            saveas(None)
        self.assertIn("cannot be None", str(context.exception))

    def test_saveas_with_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError) as context:
            saveas("nonexistent.csv")
        self.assertIn("not found", str(context.exception))

    def test_saveas_with_non_csv_file(self):
        txt_file = Path(self.temp_dir) / "test.txt"
        txt_file.write_text("This is a text file")
        with self.assertRaises(ValueError) as context:
            saveas(str(txt_file))
        self.assertIn("Expected a .csv file", str(context.exception))

    def test_saveas_with_custom_dpi(self):
        result = saveas(str(self.test_csv), dpi=150)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_saveas_with_custom_output_dir(self):
        output_dir = Path(self.temp_dir) / "output"
        result = saveas(str(self.test_csv), output_dir=str(output_dir))
        self.assertIsInstance(result, list)
        for file_path in result:
            self.assertTrue(file_path.startswith(str(output_dir)))

    def test_saveas_creates_output_dir(self):
        output_dir = Path(self.temp_dir) / "new" / "nested" / "dir"
        result = saveas(str(self.test_csv), output_dir=str(output_dir))
        self.assertTrue(output_dir.exists())
        self.assertGreater(len(result), 0)

    def test_convert_file_alias(self):
        result1 = saveas(str(self.test_csv))
        result2 = convert_file(str(self.test_csv))
        self.assertEqual(len(result1), len(result2))

    def test_convert_file_with_params(self):
        output_dir = Path(self.temp_dir) / "out"
        result = convert_file(str(self.test_csv), output_dir=str(output_dir), dpi=200)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)

    def test_saveas_with_path_object(self):
        result = saveas(self.test_csv)
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)


class TestFormats(unittest.TestCase):
    """Test different output formats."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_csv = Path(self.temp_dir) / "test.csv"
        self.test_csv.write_text("Name,Age\nAlice,30\n")

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_png_format(self):
        result = saveas(str(self.test_csv), fmt="png")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertTrue(result[0].endswith('.png'))

    def test_jpeg_format(self):
        result = saveas(str(self.test_csv), fmt="jpeg")
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        self.assertTrue(result[0].endswith('.jpg'))

    def test_case_insensitive_format(self):
        result_upper = saveas(str(self.test_csv), fmt="JPEG")
        result_lower = saveas(str(self.test_csv), fmt="jpeg")
        self.assertEqual(len(result_upper), len(result_lower))

    def test_unsupported_format(self):
        with self.assertRaises(ValueError) as context:
            saveas(str(self.test_csv), fmt="gif")
        self.assertIn("Unsupported format", str(context.exception))

    def test_tiff_format_not_supported(self):
        with self.assertRaises(ValueError):
            saveas(str(self.test_csv), fmt="tiff")

    def test_webp_format_not_supported(self):
        with self.assertRaises(ValueError):
            saveas(str(self.test_csv), fmt="webp")


class TestDelimiter(unittest.TestCase):
    """Test different CSV delimiters."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_comma_delimiter(self):
        csv_file = Path(self.temp_dir) / "test.csv"
        csv_file.write_text("Name,Age\nAlice,30\n")
        result = saveas(str(csv_file), delimiter=",")
        self.assertGreater(len(result), 0)

    def test_tab_delimiter(self):
        csv_file = Path(self.temp_dir) / "test.tsv"
        csv_file.write_text("Name\tAge\nAlice\t30\n")
        csv_file.rename(Path(self.temp_dir) / "test.csv")
        result = saveas(str(Path(self.temp_dir) / "test.csv"), delimiter="\t")
        self.assertGreater(len(result), 0)

    def test_semicolon_delimiter(self):
        csv_file = Path(self.temp_dir) / "test.csv"
        csv_file.write_text("Name;Age\nAlice;30\n")
        result = saveas(str(csv_file), delimiter=";")
        self.assertGreater(len(result), 0)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_header_only_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "test.csv"
            csv_file.write_text("Name,Age,City\n")
            result = saveas(str(csv_file))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_single_row_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "test.csv"
            csv_file.write_text("Name,Age\nAlice,30\n")
            result = saveas(str(csv_file))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_empty_csv_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("")
            temp_path = f.name
        try:
            with self.assertRaises(ValueError) as context:
                saveas(temp_path)
            self.assertIn("empty or contains no header", str(context.exception))
        finally:
            os.unlink(temp_path)

    def test_csv_with_special_characters(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            special_csv = Path(temp_dir) / "test-data_v2.0.csv"
            special_csv.write_text("Name,Value\nTest,123\n")
            result = saveas(str(special_csv))
            self.assertIsInstance(result, list)

    def test_csv_with_many_rows_multi_page(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            big_csv = Path(temp_dir) / "big.csv"
            lines = ["ID,Name,Value"]
            for i in range(500):
                lines.append(f"{i},Item_{i},{i*10}")
            big_csv.write_text("\n".join(lines))
            result = saveas(str(big_csv))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 1)

    def test_csv_with_unicode_cjk_fails(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            unicode_csv = Path(temp_dir) / "unicode.csv"
            unicode_csv.write_text("姓名,年齡,城市\n蔡徐坤,30,北京\n", encoding="utf-8")
            with self.assertRaises(Exception):
                saveas(str(unicode_csv))

    def test_csv_with_unicode_latin(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            latin_csv = Path(temp_dir) / "latin.csv"
            latin_csv.write_text("Nom,Âge,Ville\nJean,30,Paris\n", encoding="utf-8")
            result = saveas(str(latin_csv))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_csv_with_commas_in_data(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "commas.csv"
            csv_file.write_text('Name,Description\n"Smith, John","A, B, C"\n')
            result = saveas(str(csv_file))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_many_columns(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "wide.csv"
            headers = ",".join(f"Col{i}" for i in range(20))
            data = ",".join(str(i) for i in range(20))
            csv_file.write_text(f"{headers}\n{data}\n")
            result = saveas(str(csv_file))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_single_column_csv(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "single.csv"
            csv_file.write_text("Value\n100\n200\n")
            result = saveas(str(csv_file))
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)

    def test_large_dpi(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "test.csv"
            csv_file.write_text("A,B\n1,2\n")
            result = saveas(str(csv_file), dpi=600)
            self.assertIsInstance(result, list)
            self.assertGreater(len(result), 0)


class TestOutputValidation(unittest.TestCase):
    """Test output file quality and validation."""

    def test_output_files_not_empty(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "test.csv"
            csv_file.write_text("A,B,C\n1,2,3\n")
            output_dir = Path(temp_dir) / "out"
            result = saveas(str(csv_file), output_dir=str(output_dir))
            for f in result:
                size = Path(f).stat().st_size
                self.assertGreater(size, 0, f"Output file {f} should not be empty")

    def test_output_filenames_format(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "report.csv"
            csv_file.write_text("Col1,Col2\na,b\n")
            output_dir = Path(temp_dir) / "output"
            result = saveas(str(csv_file), output_dir=str(output_dir))
            expected_names = ["report1.png"]
            actual_names = [os.path.basename(f) for f in result]
            for expected in expected_names:
                self.assertIn(expected, actual_names)

    def test_output_in_correct_directory(self):
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
        """Test main() with no arguments exits with code 0 (shows help)."""
        import sys
        from csv2img.core import main
        
        with patch.object(sys, 'argv', ['csv2img']):
            with self.assertRaises(SystemExit) as ctx:
                main()
            self.assertEqual(ctx.exception.code, 0)

    def test_main_with_valid_file(self):
        import sys
        from csv2img.core import main
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "test.csv"
            csv_file.write_text("A,B\n1,2\n")
            output_dir = Path(temp_dir) / "out"
            with patch.object(sys, 'argv', ['csv2img', str(csv_file), str(output_dir)]):
                main()

    def test_main_with_help_flag(self):
        import sys
        from csv2img.core import main
        with patch.object(sys, 'argv', ['csv2img', '--help']):
            with self.assertRaises(SystemExit):
                main()

    def test_main_with_nonexistent_file(self):
        import sys
        from csv2img.core import main
        with patch.object(sys, 'argv', ['csv2img', 'nonexistent.csv']):
            with self.assertRaises(SystemExit) as ctx:
                main()
            self.assertEqual(ctx.exception.code, 1)

    def test_main_with_all_args(self):
        import sys
        from csv2img.core import main
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = Path(temp_dir) / "test.csv"
            csv_file.write_text("A,B\n1,2\n")
            output_dir = Path(temp_dir) / "out"
            with patch.object(sys, 'argv', ['csv2img', str(csv_file), str(output_dir), '150']):
                main()


if __name__ == '__main__':
    unittest.main()
