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

from phon.mesh_objects.element import Element
from phon.mesh_objects.element_set import ElementSet
from phon.mesh_objects.node import Node
from phon.mesh_objects.mesh import Mesh
from phon.mesh_objects.node_set import NodeSet


def export_to_abaqus(filename, mesh, write_2d_elements=False, f=None):

        append_to_file = False	
        if f is None:
            f = open(filename, 'w')
        else:
            append_to_file = True

        # Write header
        f.write('*Part, name=' + mesh.name.upper())


        # Write nodes
        f.write('\n*Node\n')
        for node_id in sorted(mesh.nodes.keys()):
            node = mesh.nodes[node_id]
            f.write("%d, " % (node_id))
            f.write("%.12f, %.12f, %.12f\n" % (node.x, node.y, node.z))


        # Two dimensional elements
        if write_2d_elements:   
            for element_type in mesh.element_2d_indices.keys():
                f.write("*Element, type=" + element_type + "\n")
                for element_id in mesh.element_2d_indices[element_type]:
                     f.write("%d, " % (element_id))
                     # Code below changes "[1,2,3]" to "1, 2, 3"
                     f.write(''.join('{},'.format(k) for k in mesh.elements_2d[element_id].vertices)[:-2])
                     f.write("\n")

        # Three dimensional elements
        for element_type in mesh.element_3d_indices.keys():
            f.write("*Element, type=" + element_type + "\n")
            for element_id in mesh.element_3d_indices[element_type]:
                f.write("%d, " % (element_id))
                # Code below changes "[1,2,3]" to "1, 2, 3"
                f.write(''.join('{},'.format(k) for k in mesh.elements_3d[element_id].vertices)[:-2])    
                f.write("\n")    
        
        # Two dimensional element sets
        if write_2d_elements:
            for element_set_name in mesh.element_sets_2d.keys():
                f.write("\n*Elset, elset=" + element_set_name.upper() + "\n")
                write_column_broken_array(mesh.element_sets_2d[element_set_name].getIds(), f)

        # Three dimensional element sets
        for element_set_name in mesh.element_sets_3d.keys():
            f.write("\n*Elset, elset=" + element_set_name.upper() + "\n")
            write_column_broken_array(mesh.element_sets_3d[element_set_name].getIds(), f)

        # Node sets
        for node_set_name in mesh.node_sets.keys():
            f.write("\n*Nset, nset=" + node_set_name.upper() + "\n")
            write_column_broken_array(mesh.node_sets[node_set_name].getIds(), f)
 
        if not append_to_file:
            f.write("*End Part")
            f.close()

def write_column_broken_array(array, f):
    for idx, i in enumerate(array):
        if (idx + 1) % 15 == 0:
            f.write('\n')
        if idx == (len(array) - 1):
            f.write(str(i) + "\n\n")
        else:
            f.write(str(i) + ", ")
