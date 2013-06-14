import unittest
import os

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_oofem import export_to_oofem


class Test(unittest.TestCase):
    """Unit tests for export_to_oofem."""

    def setUp(self):
        self.mesh = read_from_neper_inp("n10-id1.inp")

    def test_export_to_oofem(self):
        """Test Phons exporter for oofem files."""
        number_of_2d_elements = 0
        print self.mesh.element_indices
        for element_type in self.mesh.element_indices.keys():
            print element_type
        export_to_oofem("test_file.oof", self.mesh, write_2d_elements=False)
    
    def tearDown(self):
        pass
        #if os.path.isfile("test_file.inp"):
        #    os.remove("test_file.inp")

if __name__ == "__main__":
    unittest.main()
