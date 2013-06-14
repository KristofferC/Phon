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

from collections import OrderedDict
from phon.io.element_name_dictionary import elements_2d
from phon.io.element_name_dictionary import elements_3d
from phon.io.element_name_dictionary import element_dictionary_inverse

class Mesh:
    """ Represents a mesh which includes nodes, elements, element sets
    and node sets.
    """

    def __init__(self,
                 name=None, 
                 nodes=None, 
                 elements=None,
                 element_indices=None,
                 element_sets=None,
                 node_sets=None):

        #: Name of the mesh
        self.name = name

        # Nodes
        # {1 : node1,
        #  2 : node2,
        #  3 : node3}
        self.nodes = OrderedDict()


        # 3D elements in the mesh
        # {1 : element1,
        #  2 : element2,
        #  3 : element3}
        self.elements = OrderedDict()
        

        # {"C3D : 1,2,3, ..., indices,
        #  "C6D : 1,2,3, ..., indices}
        self.element_indices = OrderedDict()

        # Element sets
        # {Poly1 : id1, id2, ...,
        #  Poly2 : id1, id2, ...}
        self.element_sets = OrderedDict()

        # Node sets
        # {X0 : id1, id2, ...,
        #  X1 : id1, id2, ...}
        self.node_sets = OrderedDict()

    def get_number_of_2d_elements(self):
        number_of_2d_elements = 0
        for element_type in self.element_indices.keys():
            print element_type
            if element_dictionary_inverse[(element_type, "abaqus")] in elements_2d:
                number_of_2d_elements += len(self.element_indices[element_type])
        return number_of_2d_elements

    def get_number_of_3d_elements(self):
        number_of_3d_elements = 0
        for element_type in self.element_indices.keys():
            if element_dictionary_inverse[(element_type, "abaqus")] in elements_3d:
                number_of_3d_elements += len(self.element_indices[element_type])
        return number_of_3d_elements