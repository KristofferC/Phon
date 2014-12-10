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

"""
Module that contains the method of writing a mesh to a file that Abaqus can
 read.
"""

from collections import defaultdict
from collections import OrderedDict

from phon.mesh_objects.mesh import Mesh
from phon.io import element_dictionary
from phon.io import element_dictionary_inverse
from phon.io import elements_1d
from phon.io import elements_2d


def export_to_abaqus(filename, mesh, write_2d_elements=False, f=None):
    """
    Writes a mesh to a file in a format such that Abaqus can read it.

    :param filename: Path to the file to write the mesh to.
    :type filename: string
    :param mesh: The mesh to write to the file.
    :type mesh: :class:`Mesh`
    :param write_2d_elements: Determines if two dimensional elements and
                              element sets should be written to the file.
    :type write_2d_elements: boolean
    :param f: If given as an argument the mesh is appended to this file
              instead of opening a new one.
    :type f:  file object
    """

    write_1d_elements = False

    if f is None:
        f = open(filename, 'w')

    # Write header
    f.write('*Part, name=' + mesh.name.upper())

    # Write nodes
    f.write('\n*Node\n')
    for node_id, node in mesh.nodes.items():
        f.write("{0:d}, ".format(node_id))
        f.write("{0:.12e}, {1:.12e}, {2:.12e}\n".format(node.c[0], node.c[1], node.c[2]))

    # Recreate element indices
    element_indices = defaultdict(lambda:[],OrderedDict())
    for i, element in mesh.elements.items():
        element_indices[element.elem_type].append(i)

    # Elements
    for element_type, elements in element_indices.items():
        
        if ((write_1d_elements is False) and
                (element_dictionary_inverse[(element_type, "abaqus")] in elements_1d)):
            continue

        if ((write_2d_elements is False) and
                (element_dictionary_inverse[(element_type, "abaqus")] in elements_2d)):
            continue

        element_name = element_dictionary[(element_type, "abaqus")]
        f.write("\n*Element, type=" + element_name + "\n")
        for element_id in elements:
            f.write("%d, " % element_id)
            # Code below changes "[1,2,3]" to "1, 2, 3"
            f.write(''.join('{}, '.format(k) for k in
                            mesh.elements[element_id].vertices)[:-2])
            f.write("\n")

    # Element sets
    for element_set_name, element_set in mesh.element_sets.items():

        if ((write_1d_elements is False) and
                (element_dictionary_inverse[(element_type, "abaqus")] in elements_1d)):
            continue

        if ((write_2d_elements is False) and
                (mesh.element_sets[element_set_name].dimension == 2)):
            continue

        if element_set_name[0:4] == "edge":
            continue

        if len(element_set.ids) == 0:
            continue

        f.write("\n*Elset, elset=" + element_set_name + "\n")
        write_column_broken_array(element_set.ids, f)

    # Node sets
    for node_set_name, node_set in mesh.node_sets.items():
        f.write("\n*Nset, nset=" + node_set_name + "\n")
        write_column_broken_array(node_set.ids, f)


    # Surfacecd p sets
    for element_side_name, element_side_set in mesh.element_side_sets.items():
        f.write("\n*SURFACE, type=Element, NAME=" + element_side_name + "\n")
        for element_side in element_side_set.sides:
            # Tet side order:
            # [[0, 2, 1], [0, 1, 3], [1, 2, 3], [0, 3, 2]]
            # 1,2,3     1, 2, 4,    2, 3, 4,    1, 4, 3
            # Seems to match with the def. in abq, so here we go:
            f.write("{}, S{}\n".format(element_side.elem, element_side.side))

    f.write("*End Part")
    f.close()


def write_column_broken_array(int_array, f):
    """
    Writes an array to a file and inserts a new line every fifteen element
    as required by Abaqus.

    :param array: The array to write to the file
    :type array: array
    :param f: The file to write the array to
    :type f: file object

    """
    for idx, i in enumerate(int_array):
        if (idx + 1) % 15 == 0:
            f.write('\n')
        if idx == (len(int_array) - 1):
            f.write(str(i) + "\n")
        else:
            f.write(str(i) + ", ")
