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

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements
from phon.io.write.export_to_abaqus import export_to_abaqus

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

class Test(unittest.TestCase):
    """Unit tests for test_create_cohesive_elements_2d."""

    def setUp(self):
        self.mesh = read_from_neper_inp(os.path.join(__location__,"mesh2El2d.inp"),verbose=0,mesh_dimension=2)

    def test_create_cohesive_elements(self):
        meshDim = 2
        create_cohesive_elements(self.mesh,meshDim)

        # One cohesive zone element should be created
        self.assertEqual(len(self.mesh.element_sets["cohes1_2"].ids), 1)

        # There should be six nodes (2 nodes duplicated)
        self.assertEqual(len(self.mesh.nodes), 6)

    def test_export_toabaqus(self):
        write2dEl = True
        export_to_abaqus("test2El2dCZ.inp", self.mesh, write2dEl)
    
    def tearDown(self):
        if os.path.isfile("test2El2dCZ.inp"):
            os.remove("test2El2dCZ.inp")

if __name__ == "__main__":
    unittest.main()

