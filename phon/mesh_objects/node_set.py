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


class NodeSet:
    """ Represents a set of nodes """

    def __init__(self, name, ids=None):
        """
        Creates a :class:`NodeSet` class.

        :param name: The name of the node set.
        :type name: str
        :param ids: The identifiers of the nodes
        :type ids: list of ints

        """
        self.name = name

        #: The elements contained in the set
        if ids is None:
            ids = []
        self.ids = ids

    def __str__(self):
        """
        Returns a string representation of the node.

        :return: The string representation.
        :rtype: str

        """
        return("Node set with name {0} containing nodes with the "
               "following ids {1}".format(self.name, self.ids))
