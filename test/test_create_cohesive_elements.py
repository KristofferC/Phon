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

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements
from phon.mesh_tools.create_cohesive_elements import get_grains_connected_to_face
from phon.mesh_tools.create_cohesive_elements import get_node_id_grain_LUT


class Test(unittest.TestCase):
    """Unit tests for test_create_cohesive_elements."""

    def setUp(self):
        self.mesh = read_from_neper_inp("n10-id1.inp", verbose=0)
        self.original_n_nodes = len(self.mesh.nodes)

    def test__get_grains_connected_to_face(self):
        node_id_grain_LUT = get_node_id_grain_LUT(self.mesh)
        self.assertEqual(get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face35"],                                        node_id_grain_LUT), [6])
        self.assertEqual(get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face18"],
                                                      node_id_grain_LUT), [3, 5])
        self.assertEqual(get_grains_connected_to_face(self.mesh, self.mesh.element_sets["face4"],
                                                      node_id_grain_LUT), [1, 10])

    # TODO: A little bit too few asserts in this test.
    def test_create_cohesive_elements(self):
        create_cohesive_elements(self.mesh)
        export_to_abaqus("n10-id1_coh.inp", self.mesh, True)
        self.assertEqual(len(self.mesh.element_sets["cohes9_2"].ids), 6)

    # TODO: Add tests for more helper functions.

if __name__ == "__main__":
    unittest.main()
