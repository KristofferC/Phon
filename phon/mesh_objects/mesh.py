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

from phon.io_tools import elements_2d
from phon.io_tools import elements_3d
from phon.io_tools import element_dictionary_inverse


class Mesh:

    """ Represents a mesh which includes nodes, elements, element sets
    and node sets.
    """

    def __init__(self,
                 name,
                 nodes=None,
                 elements=None,
                 element_sets=None,
                 element_side_sets=None,
                 node_sets=None):
        """
        :param name: Name of the mesh.
        :type name: string
        :param nodes: Nodes in the mesh.
        :type nodes: dict of format {node_id (int) : :class:`Node`}
        :param elements: All elements in the mesh.
        :type elements: dict of format {element_id (int) : :class:`Element`}
        :param element_sets: Different element sets
        :type element_sets: dict of format {element_set (string) : [element_ids (int)]}
        :param element_side_sets: Different element side sets
        :type element_side_sets: dict of format {element_set (string) : [element_ids (int)]}
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

        if element_sets is None:
            element_sets = OrderedDict()
        self.element_sets = element_sets

        if element_side_sets is None:
            element_side_sets = OrderedDict()
        self.element_side_sets = element_side_sets

        if node_sets is None:
            node_sets = OrderedDict()
        self.node_sets = node_sets

    def renumber_nodes(self):
        """
        Renumbers nodes so that they are "dense" on the number line.
        For example, if the mesh consist of four nodes with identifiers
        1, 2, 5, 7 this would change them to 1, 2, 3, 4. This method also
        updates the elements to use the renumbered node identifiers.

        Currently only updates nodes for 3d elements so don't do anything with 2d elements
        after calling this.

        """

        # raise("This method does not work reliably")

        # Create dictionary of old and renumbered node identifiers
        node_renumber_dict = {}
        new_nodes_dict = {}
        for i, node in enumerate(self.nodes.keys()):
            node_renumber_dict[node] = i + 1
            new_nodes_dict[i + 1] = self.nodes[node]

        self.nodes = new_nodes_dict

        # Update node identifiers in elements (only 3d).
        for element_id, element in self.elements.items():
            if (element_dictionary_inverse[
                    (element.elem_type, "abaqus")] in elements_2d):
                continue
            for i, node_id in enumerate(element.vertices):
                element.vertices[i] = node_renumber_dict[node_id]

        # Update node identifiers in node sets
        for node_set_name, node_set in self.node_sets.items():
            for i, node_id in enumerate(node_set.ids):
                node_set.ids[i] = node_renumber_dict[node_id]

    def get_number_of_2d_elements(self):
        """
        Calculates the number of two dimensional elements in the mesh.

        :return: Number of two dimensional elements.
        :rtype: int

        """
        number_of_2d_elements = 0
        for element in self.elements.values():
            if element_dictionary_inverse[
                    (element.elem_type, "abaqus")] in elements_2d:
                number_of_2d_elements += 1
        return number_of_2d_elements

    def get_number_of_3d_elements(self):
        """
        Calculates the number of three dimensional elements in the mesh.

        :return: Number of three dimensional elements
        :rtype: int

        """
        number_of_3d_elements = 0
        for element in self.elements.values():
            if element_dictionary_inverse[
                    (element.elem_type, "abaqus")] in elements_3d:
                number_of_3d_elements += 1
        return number_of_3d_elements
