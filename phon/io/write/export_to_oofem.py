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

<<<<<<< HEAD
=======
import random
import math

>>>>>>> devel
from phon.io import element_dictionary
from phon.io import element_dictionary_inverse
from phon.io import elements_2d


def export_to_oofem(filename, mesh, write_2d_elements=False):
    """
    Writes a mesh to a file in a format that OOFEM uses.

    :param filename: Path to the file to write the mesh to.
    :type filename: string
    :param mesh: The mesh to write to the file.
    :type mesh: :class:`Mesh`
    :param write_2d_elements: Determines if two dimensional elements and
                              element sets should be written to the file.
    :type write_2d_elements: boolean
    """
    f = open(filename, "w")

    # Lengths
    n_nodes = len(mesh.nodes)

    if write_2d_elements:
        n_elements = (mesh.get_number_of_2d_elements() + 
                      mesh.get_number_of_3d_elements())
    else:
        n_elements = mesh.get_number_of_3d_elements()

    # Output file record
    f.write(filename + ".out\n")

    # Job description record
    f.write("{}\n".format(mesh.name))

    # Analysis record
    #f.write("LinearStatic 1 nsteps 1 nmodules 1\n")
    #f.write("vtkxml tstep_all domain_all primvars 1 1 vars 4 1 2 4 5 stype 1 0\n")
    # Domain record
    #f.write("domain 3d\n")

    # Output manager record
    #f.write("OutputManager tstep_all dofman_all element_all\n")

    # Components size record
    f.write("ndofman " + str(n_nodes) + " ")
    f.write("nelem " + str(n_elements) + " ")
    f.write("ncrosssect 1" + " ")
    f.write("nmat 1" + " ")
    f.write("nbc 1" + " ")
    f.write("nic 0" + " ")
    f.write("nltf 1\n")

    # Write nodes
    for node_id, node in mesh.nodes.iteritems():
        f.write("node {0:d} ".format(node_id))
        f.write("coords 3 {0:.12f} {1:.12f} {2:.12f} ".format(node.x, node.y, node.z))
        f.write("\n")
        #f.write("bc 3 1 1 1\n")

    #  Elements
    for element_type in mesh.element_indices.keys():
        if (write_2d_elements is False) and \
                (element_dictionary_inverse[(element_type, "abaqus")] in elements_2d):
            continue
        element_name = element_dictionary[(element_type, "oofem")]
        for element_id in mesh.element_indices[element_type]:
            f.write(element_name + " {0:d} ".format(element_id))
            f.write("nodes {} ".format(str(len(mesh.elements[element_id].vertices))))
            # Code below changes "[1,2,3]" to "1 2 3"
            f.write(''.join('{} '.format(k) 
                            for k in mesh.elements[element_id].vertices)[:-1])

            f.write(" mat 1 crossSect 1")
            """if element_name == "Interface3dtrlin":
                f.write(" mat 2 crossSect 1")
            if element_name == "LTRSpace":
                f.write(" mat 1 crossSect 1")"""

            f.write("\n")

    # Sets
    set_id = 0
    # Element sets
    for element_set_name, element_set in mesh.element_sets.iteritems():
        if (write_2d_elements is False) and (element_set.dimension == 2):
            continue
        set_id += 1
        f.write("# " + element_set_name)
        f.write("\nSet {} elements {} ".format(str(set_id), str(len(element_set.ids))))
        f.write(''.join('{} '.format(k) for k in element_set.ids)[:-1])
        f.write("\n")
        
    # Node sets
    for node_set_name, node_set in mesh.node_sets.iteritems():
        set_id += 1
        f.write("\n# " + node_set_name)
        f.write("\nSet {} nodes {} ".format(str(set_id), str(len(node_set.ids))))
        f.write(''.join('{} '.format(k) for k in node_set.ids)[:-1])


    # For testing
    #f.write("\nSimpleCS 1\n")
    #f.write("IsoLE 1 d 1. E 30.e6 n 0.2 tAlpha 1.2e-5\n")
    #f.write("BoundaryCondition  1 loadTimeFunction 1 prescribedvalue 0.0\n")
    #f.write("PeakFunction 1 t 1.0 f(t) 1.\n")
