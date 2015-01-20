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

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_matrix import create_matrix


__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


class Test(unittest.TestCase):
    """Unit tests for test_create_matrix."""

    def setUp(self):
        self.mesh = read_from_neper_inp(os.path.join(__location__, "inp_test_files/n10-id1.inp"), verbose=0)
        # self.mesh_order_2 = read_from_neper_inp("n10-id1_order_2.inp", verbose=0)

    # TODO: Right now only testing runtime errors... Add real tests
    def test_create_fence_elements(self):
        thickness = 0.05

        # Test finite thickness cohesive with order 1
        create_matrix(self.mesh, thickness, mesh_dimension=3)
        export_to_abaqus("n10-id1_fence.inp", self.mesh, write_2d_elements=False)

    def tearDown(self):
        if os.path.isfile("n10-id1_fence.inp"):
            os.remove("n10-id1_fence.inp")

            # TODO: Add tests for the helper functions.


if __name__ == "__main__":
    unittest.main()
