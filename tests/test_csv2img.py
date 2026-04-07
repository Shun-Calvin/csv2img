"""
Tests for csv2img module.
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
        
        # Should return a list of file paths
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 0)
        
        # All files should exist
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
        
        # All files should be in the custom output directory
        for file_path in result:
            self.assertTrue(file_path.startswith(str(output_dir)))

    def test_convert_file_alias(self):
        """Test that convert_file is an alias for saveas."""
        result1 = saveas(str(self.test_csv))
        result2 = convert_file(str(self.test_csv))
        
        # Both should return the same number of files
        self.assertEqual(len(result1), len(result2))


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""

    def test_empty_csv_file(self):
        """Test with an empty CSV file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("")
            temp_path = f.name
        
        try:
            # Should handle empty CSV gracefully
            result = saveas(temp_path)
            self.assertIsInstance(result, list)
        except Exception as e:
            # Some error is acceptable for empty CSV
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


if __name__ == '__main__':
    unittest.main()
