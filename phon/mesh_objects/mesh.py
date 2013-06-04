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

class Mesh:
    """ Represents a mesh which includes nodes, elements, element sets
    and node sets.
    """

    def __init__(self, name, nodes=None, nodeSets=None,
                 element_sets_2d=None, element_sets_3d=None,
                 cohesiveElems=None, cohesiveSets=None,
                 volumes=None, materials=None):

        #: Name of the mesh
        self.name = name

        # Nodes
        self.nodes = {}


        # 2D elements in the mesh
        # Represented by a int : list dictionary
        self.elements_2d = {}

        # 3D elements in the mesh
        self.elements_3d = {}

        # Element sets
        self.element_sets_2d = {}
        self.element_sets_3d = {}

        # Node sets
        self.node_sets = {}

