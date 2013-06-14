import unittest

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements

class Test(unittest.TestCase):
    """Unit tests for test_create_cohesive_elements."""

    def setUp(self):
        self.mesh = read_from_neper_inp("n10-id1.inp", verbose = 0)

    def test_create_cohesive_elements(self):
        create_cohesive_elements(self.mesh)
        print "wtf"
        export_to_abaqus("n10-id1_coh.inp", self.mesh)
                   

if __name__ == "__main__":
    unittest.main()
