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


class ElementSide:

    def __init__(self, elemnum, sidenum):
        self.elem = elemnum
        self.side = sidenum

    def __str__(self):
        return "Side {} of element {}".format(self.side, self.elem)


class ElementSideSet:

    """ Represents a set of element sides """

    def __init__(self, name):
        """
        :param name: Name of the set.
        :type name: str
        """
        self.name = name
        self.sides = []

    def __str__(self):
        """
        Returns a string representation of the element set.

        :return: The string representation
        :rtype: str

        """
        return ("Element side set with name {0} containing elements with the "
                "following ids {1}".format(self.name, self.sides))
