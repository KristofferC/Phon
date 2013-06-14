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

from phon.io.element_name_dictionary import element_dictionary
from phon.io.element_name_dictionary import element_dictionary_inverse
from phon.io.element_name_dictionary import elements_2d
from phon.io.element_name_dictionary import elements_3d

def export_to_oofem(filename, mesh, write_2d_elements=False):
        f = open(filename, "w")

        # Lengths
        n_nodes = len(mesh.nodes)

        if write_2d_elements:
            n_elements = mesh.get_number_of_2d_elements() + mesh.get_number_of_3d_elements()
        else:
            n_elements = mesh.get_number_of_3d_elements()


        # Output file record
        f.write(filename + ".out\n")

        # Job description record
        f.write("Voronoi\n")

        # Analysis record
        f.write("LinearStatic 1 nsteps 1 nmodules 1\n")
        f.write("vtkxml tstep_all domain_all primvars 1 1 vars 4 1 2 4 5 stype 1 0\n")
        # Domain record
        f.write("domain 3d\n")

        # Output manager record
        f.write("OutputManager tstep_all dofman_all element_all\n")

        # Components size record

        f.write("ndofman " + str(n_nodes) + " ")
        f.write("nelem " + str(n_elements) + " ")
        f.write("ncrosssect 1" + " ")
        f.write("nmat 1" + " ")
        f.write("nbc 1" + " ")
        f.write("nic 0" + " ")
        f.write("nltf 1\n")

        # Write nodes
        for node_id in sorted(mesh.nodes.keys()):
            node = mesh.nodes[node_id]
            f.write("node %d " % (node_id))
            f.write("coords 3 %.12f %.12f %.12f " % (node.x, node.y, node.z))
            f.write("\n")
            #f.write("bc 3 1 1 1\n")

        #  Elements
        for element_type in mesh.element_indices.keys():
            if ((write_2d_elements is False) and
               (element_dictionary_inverse[(element_type, "abaqus")] in elements_2d)):
                    continue
            element_name = element_dictionary[(element_type, "oofem")]
            for element_id in mesh.element_indices[element_type]:
                f.write(element_name + " %d " % (element_id)) 
                f.write("nodes " + str(len(mesh.elements[element_id].vertices)) + " ")
                # Code below changes "[1,2,3]" to "1 2 3"
                f.write(''.join('{} '.format(k) for k in mesh.elements[element_id].vertices)[:-1])
                f.write(" mat 1 crossSect 1")
                f.write("\n")

        ## Sets
        set_id = 0
        # Element sets
        for element_set_name in mesh.element_sets.keys():
            element_set = mesh.element_sets[element_set_name]
            if ((write_2d_elements is False) and
               (element_set.dimension == 2)):
                    continue
            set_id += 1
            f.write("# " + element_set_name)
            f.write("\nSet " + str(set_id) + " elements " + str(len(element_set.ids)) + " ")
            f.write(''.join('{} '.format(k) for k in element_set.ids)[:-1])
            f.write("\n")
        
        # Node sets
        for node_set_name in mesh.node_sets.keys():
            node_set = mesh.node_sets[node_set_name]
            set_id += 1
            f.write("\n# " + node_set_name)
            f.write("\nSet " + str(set_id) + " nodes " + str(len(node_set.ids)) + " ")
            f.write(''.join('{} '.format(k) for k in node_set.ids)[:-1])


        # For testing
        f.write("\nSimpleCS 1\n")
        f.write("IsoLE 1 d 1. E 30.e6 n 0.2 tAlpha 1.2e-5\n")
        f.write("BoundaryCondition  1 loadTimeFunction 1 prescribedvalue 0.0\n")
        f.write("PeakFunction 1 t 1.0 f(t) 1.\n")


def write_column_broken_array(array, f):
    for idx, i in enumerate(array):
        if (idx + 1) % 15 == 0:
            f.write('\n')
        if idx == (len(array) - 1):
            f.write(str(i) + "\n\n")
        else:
            f.write(str(i) + ", ")
