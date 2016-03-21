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

from phon.io.read.read_from_abaqus_inp import read_from_abaqus_inp
from phon.io.read.read_from_abaqus_inp import to_number


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Test(unittest.TestCase):
    """Unit tests for read_from_neper_inp."""

    def setUp(self):
        self.mesh = read_from_abaqus_inp(os.path.join(__location__, "mesh_test_files/n10-id1.inp"), verbose=0)
        self.mesh_aba = read_from_abaqus_inp(os.path.join(__location__, "mesh_test_files/n10_id1_from_abaq.inp"), verbose=0)

    def test_read_from_neper_inp(self):
        """Test Phons reader for Neper inp files."""

        for mesh in [self.mesh, self.mesh_aba]:
            # Test nodes
            self.assertEqual(len(mesh.nodes), 289)
            self.assertTrue(mesh.nodes[287].c[0] - 0.91031946481 < 10E-9)
            self.assertTrue(mesh.nodes[1].c[1] - 0.0 < 10E-9)
            self.assertTrue(mesh.nodes[289].c[2] - 0.886838138103 < 10E-9)

            # Test elements
            self.assertEqual(len(mesh.elements), 1683)
            self.assertTrue((mesh.elements[1].elem_type == "CPE3") or
                            (mesh.elements[1].elem_type == "CPE6"))
            self.assertEqual(mesh.elements[5].vertices, [43, 39, 40])
            self.assertEqual(mesh.elements[684].vertices, [38, 5, 52])
            self.assertTrue((mesh.elements[686].elem_type == "C3D4") or
                            (mesh.elements[686].elem_type == "C3D10"))
            self.assertEqual(mesh.elements[685].vertices, [44, 155, 61, 154])
            self.assertEqual(mesh.elements[1683].vertices, [283, 127, 246, 284])

            self.assertEqual(len(mesh.node_sets), 44)

        # We need double tests due for strings due to Abaqus capitalizing things.

        # Test element sets
        self.assertEqual(len(self.mesh.element_sets), 66)
        self.assertEqual(self.mesh.element_sets["face22"].name, "face22")
        self.assertEqual(self.mesh.element_sets["face36"].ids[3], 434)
        self.assertEqual(self.mesh_aba.element_sets["face22"].name, "face22")
        self.assertEqual(self.mesh_aba.element_sets["face36"].ids[3], 434)

        self.assertEqual(self.mesh.element_sets["poly6"].name, "poly6")
        self.assertEqual(self.mesh.element_sets["poly10"].ids[8], 1584)
        self.assertEqual(self.mesh_aba.element_sets["poly6"].name, "poly6")
        self.assertEqual(self.mesh_aba.element_sets["poly10"].ids[8], 1584)

        # Test node sets
        self.assertEqual(len(self.mesh.node_sets["z0"].ids), 44)
        self.assertEqual(self.mesh.node_sets["x1z1body"].ids[1], 116)
        self.assertEqual(self.mesh.node_sets["x1y0z1"].ids, [32])
        self.assertEqual(len(self.mesh_aba.node_sets["z0"].ids), 44)
        self.assertEqual(self.mesh_aba.node_sets["x1z1body"].ids[1], 116)
        self.assertEqual(self.mesh_aba.node_sets["x1y0z1"].ids, [32])

    def test_to_number(self):
        self.assertEqual(to_number("1.3"), 1.3)
        self.assertEqual(to_number("1"), 1)


if __name__ == "__main__":
    unittest.main()
