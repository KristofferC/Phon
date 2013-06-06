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

def export_to_oofem(filename, mesh, write_2d_elements=False, f=None):

        append_to_file = False	
        if f is None:
            f = open(filename, 'w')
        else:
            append_to_file = True

        # Lengths
        n_nodes = len(mesh.nodes)
        n_elements_3d = len(mesh.elements_3d)
        n_elements_2d = len(mesh.elements_2d)

        n_elements = n_elements_3d
        if write_2d_elements:
            n_elements += n_elements_2d


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
            f.write("bc 3 1 1 1\n")


        # Two dimensional elements
        if write_2d_elements:   
            for element_type in mesh.element_2d_indices.keys():
                element_name = element_2d_dictionary[(element_type, "oofem")]
                for element_id in mesh.element_2d_indices[element_type]:
                    f.write(element_name + " %d " % (element_id)) 
                    f.write("nodes " + str(len(mesh.elements_2d[element_id].vertices)) + " ")
                    # Code below changes "[1,2,3]" to "1 2 3"
                    f.write(''.join('{} '.format(k) for k in mesh.elements_2d[element_id].vertices)[:-1])
                    f.write( "mat 1")
                    f.write("\n")

        # Three dimensional elements
        for element_type in mesh.element_3d_indices.keys():
            element_name = element_3d_dictionary[(element_type, "oofem")]
            for element_id in mesh.element_3d_indices[element_type]:
                f.write(element_name + " %d " % (element_id)) 
                f.write("nodes " + str(len(mesh.elements_3d[element_id].vertices)) + " ")
                # Code below changes "[1,2,3]" to "1, 2, 3"
                f.write(''.join('{} '.format(k) for k in mesh.elements_3d[element_id].vertices)[:-1])   
                f.write(" mat 1 crossSect 1")
                f.write("\n")    
        
        """
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
        """

        f.write("SimpleCS 1\n")
        f.write("IsoLE 1 d 1. E 30.e6 n 0.2 tAlpha 1.2e-5\n")
        f.write("BoundaryCondition  1 loadTimeFunction 1 prescribedvalue 0.0\n")
        f.write("PeakFunction 1 t 1.0 f(t) 1.\n")

        if not append_to_file:
            #f.write("*End Part")
            f.close()

def write_column_broken_array(array, f):
    for idx, i in enumerate(array):
        if (idx + 1) % 15 == 0:
            f.write('\n')
        if idx == (len(array) - 1):
            f.write(str(i) + "\n\n")
        else:
            f.write(str(i) + ", ")
