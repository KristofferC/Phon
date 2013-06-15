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
                 name,
                 nodes=None,
                 elements=None,
                 element_indices=None,
                 element_sets=None,
                 node_sets=None):
        """
        Create a new :class:`Mesh` object.

        :param name: Name of the mesh.
        :type name: string
        :param nodes: Nodes in the mesh.
        :type nodes: dict of format {node_id (int) : :class:`Node`}
        :param elements: All elements in the mesh.
        :type elements: dict of format {element_id (int) : :class:`Element`}
        :param element_indices: Elements sorted according to their type
        :type element:indices: dict of format {element_type (string) : [element_ids (int)]}
        :param element_sets: Different element sets
        :type element_sets: dict of format {element_set (string) : [element_ids (int)]}
        :param node_sets:
        :type node_sets: dict of format {node_set (string) : [node_ids (int)]}

        """

        self.name = name

        if nodes is None:
            nodes = OrderedDict()
        self.nodes = nodes

        if elements is None:
            elements = OrderedDict()
        self.elements = elements

        if element_indices is None:
            element_indices = OrderedDict()
        self.element_indices = element_indices

        if element_sets is None:
            element_sets = OrderedDict()
        self.element_sets = element_sets

        if node_sets is None:
            node_sets = OrderedDict()
        self.node_sets = node_sets

    # TODO: Test this function
    def _renumber_nodes(self):
        """
        Renumbers nodes so that they are "dense" on the number line.
        For example, if the mesh consist of four nodes with identifiers
        1, 2, 5, 7 this would change them to 1, 2, 3, 4. This method also
        updates the elements to use the renumbered node identifiers.
        TODO: This might be a useful function in general for the mesh class
        so it could be moved to be a method of the mesh class.

        """

        # Create dictionary of old and renumbered node identifiers
        node_renumber_dict = {}
        for i, node in enumerate(self.nodes.keys()):
            node_renumber_dict[node] = i

        # Update node identifiers in elements
        for element_id in self.elements.keys():
            for element in self.elements[element_id]:
                for i, node_id in enumerate(element.vertices):
                    element.vertices[i] = node_renumber_dict[node_id]

        # Update node identifiers in node sets
        for node_set_name in self.node_sets.keys():
            node_set = self.node_sets[node_set_name]
            for i, node_id in enumerate(node_set.ids):
                node_set.ids[i] = node_renumber_dict[node_id]

    def get_number_of_2d_elements(self):
        """
        Calculates the number of two dimensional elements in the mesh.

        :return: Number of two dimensional elements.
        :rtype: int
        """
        number_of_2d_elements = 0
        for element_type in self.element_indices.keys():
            print element_type
            if element_dictionary_inverse[(element_type, "abaqus")] in elements_2d:
                number_of_2d_elements += len(self.element_indices[element_type])
        return number_of_2d_elements

    def get_number_of_3d_elements(self):
        """
        Calculates the number of three dimensional elements in the mesh.

        :return: Number of three dimensional elements
        :rtype: int
        """
        number_of_3d_elements = 0
        for element_type in self.element_indices.keys():
            if element_dictionary_inverse[(element_type, "abaqus")] in elements_3d:
                number_of_3d_elements += len(self.element_indices[element_type])
        return number_of_3d_elements