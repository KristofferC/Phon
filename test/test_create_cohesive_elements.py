__copyright__ = "Copyright (C) 2013 Kristoffer Carlsson"

__license__ = """
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import unittest
import os
import filecmp

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements
from phon.mesh_tools.create_cohesive_elements import get_grains_connected_to_face
from phon.mesh_tools.create_cohesive_elements import get_node_id_grain_lut


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


# TODO: Add test for order = 2
# TODO: Add test for qudraterial elements
# TODO: Add tests for gmsh files
# TODO: Add tests for more helper functions.
class Test(unittest.TestCase):
    """Unit tests for test_create_cohesive_elements."""

    def setUp(self):
        self.mesh = read_from_neper_inp(os.path.join(__location__, "inp_test_files/n10-id1.inp"), verbose=0)
        self.mesh_2d = read_from_neper_inp(os.path.join(__location__, "inp_test_files/n10-id1_2d.inp"))

    def test_get_grains_connected_to_face(self):
        node_id_grain_lut = get_node_id_grain_lut(self.mesh)
        self.assertEqual(get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face35"],
                                                      node_id_grain_lut), [6])
        self.assertEqual(get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face18"],
                                                      node_id_grain_lut), [3, 5])
        self.assertEqual(get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face4"],
                                                      node_id_grain_lut), [1, 10])

    # TODO: A little bit too few asserts in this test...
    def test_create_cohesive_elements(self):
        create_cohesive_elements(self.mesh, mesh_dimension=3)
        export_to_abaqus("n10-id1_coh.inp", self.mesh, False)
        self.assertEqual(len(self.mesh.element_sets["cohes9_2"].ids), 6)
        self.assertTrue(filecmp.cmp("n10-id1_coh.inp",
                                    os.path.join(__location__, "inp_test_files/n10-id1_coh_ref.inp")))

        create_cohesive_elements(self.mesh_2d, mesh_dimension=2)
        export_to_abaqus("n10_id1_2d_coh.inp", self.mesh, write_2d_elements=True)
        self.assertTrue(filecmp.cmp("n10_id1_2d_coh.inp",
                                    os.path.join(__location__, "inp_test_files/n10-id1_2d_coh_ref.inp")))

    def tearDown(self):
        if os.path.isfile("n10-id1_coh.inp"):
            os.remove("n10-id1_coh.inp")
        if os.path.isfile("n10_id1_2d_coh.inp"):
            os.remove("n10_id1_2d_coh.inp")


if __name__ == "__main__":
    unittest.main()
