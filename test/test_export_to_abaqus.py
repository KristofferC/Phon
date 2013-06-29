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


class Test(unittest.TestCase):
    """Unit tests for export_to_abaqus."""

    def setUp(self):
        self.mesh = read_from_neper_inp("n10-id1.inp")

    def test_export_to_abaqus(self):
        """Test Phons reader for neper inp files."""
        export_to_abaqus("test_file.inp", self.mesh, write_2d_elements=True)
        read_from_neper_inp("test_file.inp")
        export_to_abaqus("test_file_2.inp", self.mesh)
    
    def tearDown(self):
        """if os.path.isfile("test_file.inp"):
            os.remove("test_file.inp")
        if os.path.isfile("test_file_2.inp"):
            os.remove("test_file_2.inp")"""

if __name__ == "__main__":
    unittest.main()
