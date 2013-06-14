import unittest

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements

from phon.mesh_tools.create_cohesive_elements import _get_grains_connected_to_face
from phon.mesh_tools.create_cohesive_elements import _get_grains_containing_node_id
from phon.mesh_tools.create_cohesive_elements import _get_tetra_and_grain_with_node_id


class Test(unittest.TestCase):
    """
    Unit tests for test_create_cohesive_elements.
    """

    def setUp(self):
        self.mesh = read_from_neper_inp("n10-id1.inp", verbose = 0)
        self.original_n_nodes = len(self.mesh.nodes)
        create_cohesive_elements(self.mesh)

    def test_create_cohesive_elements(self):
        export_to_abaqus("n10-id1_coh.inp", self.mesh, True)
        self.assertEqual(len(self.mesh.element_sets["cohes9_2"].ids), 6)


    
    def test__get_grains_connected_to_face(self):
        self.assertEqual(_get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face35"], 
                          self.original_n_nodes), [6])
        self.assertEqual(_get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face18"], 
                          self.original_n_nodes), [3, 5])
        self.assertEqual(_get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face4"], 
                          self.original_n_nodes), [1, 10])

    def test__get_grains_containing_node_id(self):
        self.assertEqual(_get_grains_containing_node_id(self.mesh, 244, self.original_n_nodes), [6])
        self.assertEqual(_get_grains_containing_node_id(self.mesh, 8, original_n_nodes = 289), 
                         [1, 2, 3, 4, 5, 7, 10])

                   
if __name__ == "__main__":
    unittest.main()
