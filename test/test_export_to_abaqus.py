import unittest
import os

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_abaqus import export_to_abaqus


class Test(unittest.TestCase):
    """Unit tests for read_from_neper_inp."""

    def setUp(self):
        self.mesh = read_from_neper_inp("n10-id1.inp")

    def test_export_to_abaqus(self):
        """Test Phons reader for neper inp files."""
        export_to_abaqus("test_file.inp", self.mesh)
        read_from_neper_inp("test_file.inp")
        export_to_abaqus("test_file_2.inp", self.mesh)
    
    def tearDown(self):
        pass
        if os.path.isfile("test_file.inp"):
            os.remove("test_file.inp")
        if os.path.isfile("test_file_2.inp"):
            os.remove("test_file_2.inp")

if __name__ == "__main__":
    unittest.main()
