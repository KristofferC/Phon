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


class ElementSet:
    """ Represents a set of elements """

    def __init__(self, name, dimension, ids=None):
        """
        :param name: Name of the element set.
        :type name: str
        :param dimension: The dimension of the elements in the set
        :type dimension: int
        :param ids: Identifiers of the elements in the set.
        :type ids: list of ints

        """
        self.name = name
        self.dimension = dimension

        if ids is None:
            ids = []
        self.ids = ids

        # Specific properties assigned to the set, e.g. material properties.
        self.set_properties = {}

    def get_dimension(self):
        """
        Get the dimension of the element set.

        :return: The dimension.
        :rtype: int

        """
        return self.dimension

    def __str__(self):
        """
        Returns a string representation of the element set.

        :return: The string representation
        :rtype: str

        """
        return ("Element set with name {0} containing elements with the "
                "following ids {1}".format(self.name, self.ids))

    def get_all_node_ids(self, mesh):
        """
        Gets all the nodes identifiers for the elements in the element set.

        :param mesh: The mesh
            :type mesh: :class:`phon.mesh_objects.mesh.Mesh()`
        :return: The node identifiers
        :rtype: list of ints

        """
        all_node_ids = []

        for element_id in self.ids:
            all_node_ids += mesh.elements[element_id].vertices

        return list(set(all_node_ids))
