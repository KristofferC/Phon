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

from phon.io import element_dictionary
from phon.io import element_dictionary_inverse
from phon.io import elements_2d
from phon.io import elements_1d


def export_to_oofem(filename, mesh, write_2d_elements):
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

    mesh_dimension = 1
    if mesh.get_number_of_2d_elements() > 0:
        mesh_dimension = 2

    if mesh.get_number_of_3d_elements() > 0:
        mesh_dimension = 3

    if mesh_dimension == 3:
        set_type_bulk = "poly"
        set_type_interface = "face"
    elif mesh_dimension == 2:
        set_type_bulk = "face"
        set_type_interface = "edge"
    else:
        print('Unsupported dimension in export_to_oofem: ', mesh_dimension)
        return

    write_crosssections = True
    write_materials = True
    write_bcs = True
    write_ltf = False

    f = open(filename, "w")

    if write_2d_elements:
        n_elements = (mesh.get_number_of_2d_elements() +
                      mesh.get_number_of_3d_elements())
    else:
        n_elements = mesh.get_number_of_3d_elements()

    n_cs = 0
    n_set = len(mesh.node_sets) + len(mesh.element_side_sets)
    for element_set_name, element_set in mesh.element_sets.items():
        if (write_2d_elements is False) and (element_set.dimension == 2):
            continue
        if (element_set.dimension == 1):
            continue
        n_set += 1
        if element_set_name[:4] == set_type_bulk or element_set_name[:5] == "cohes":
            n_cs += 1

    # Output file record
    # f.write(filename + ".out\n")

    # Job description record
    # f.write("{}\n".format(mesh.name))

    # Analysis record
    # f.write("StaticStructural 1 nsteps 1 nmodules 1\n")
    # f.write("vtkxml tstep_all domain_all primvars 1 1 cellvars 4 1 2 4 5\n")
    # Domain record
    if mesh_dimension == 3:
        f.write("domain 3d\n")
    elif mesh_dimension == 2:
        f.write("domain 2dPlaneStress\n")

    # Output manager record
    f.write("OutputManager\n")

    # Components size record
    if write_crosssections:
        f.write("ncrosssect " + str(n_cs) + " ")
    else:
        f.write("ncrosssect " + str(0) + " ")

    f.write("ndofman " + str(len(mesh.nodes)) + " ")
    f.write("nelem " + str(n_elements) + " ")

    f.write("nset " + str(n_set) + " ");

    if write_materials:
        f.write("nmat " + str(n_cs) + " ")
    else:
        f.write("nmat " + str(0) + " ")

    if write_bcs:
        num_bcs = 0
        for element_set_name, element_set in mesh.element_side_sets.items():
            if 'boundary_condition_name' in element_set.set_properties and 'boundary_condition_properties' in element_set.set_properties:
                num_bcs += 1
        f.write("nbc {} ".format(num_bcs))
    else:
        f.write("nbc 0 ")

    f.write("nic 0 ")

    if write_ltf:
        f.write("nltf 2 ")
    else:
        f.write("nltf 0 ")

    f.write("\n");

    # Write nodes
    for node_id, node in mesh.nodes.items():
        f.write("node {0:d} ".format(node_id))
        f.write("coords 3 {:.12e} {:.12e} {:.12e} ".format(
            node.c[0], node.c[1], node.c[2]))
        f.write("\n")

    # Elements
    for element_id, element in mesh.elements.items():
        if (write_2d_elements is False) and \
                (element_dictionary_inverse[(element.elem_type, "abaqus")] in elements_2d):
            continue
        if element_dictionary_inverse[(element.elem_type, "abaqus")] in elements_1d:
            continue
        element_name = element_dictionary[(element.elem_type, "oofem")]
        f.write(element_name + " {0:d} ".format(element_id))
        f.write("nodes {} ".format(str(len(element.vertices))))
        # Code below changes "[1,2,3]" to "1 2 3"
        f.write(''.join('{} '.format(k)
                        for k in element.vertices)[:-1])
        f.write("\n")

    # Crosssections
    if write_crosssections:
        cs_id = 0
        count = 0
        for element_set_name, element_set in mesh.element_sets.items():
            if (write_2d_elements is False) and (element_set.dimension == 2):
                continue
            if element_set.dimension == 1:
                continue

            count += 1
            cs_name = 'CROSS_SECTION_NAME'

            if element_set_name[:4] == set_type_bulk:
                cs_name = 'SimpleCS'
            elif element_set_name[:5] == "cohes":
                cs_name = 'InterfaceCS'

            if element_set_name[:4] == set_type_bulk or element_set_name[:5] == "cohes":
                cs_id += 1

                if 'cross_section_name' in element_set.set_properties:
                    cs_name = element_set.set_properties['cross_section_name']
                    #print 'Found cross_section_name: ', element_set.set_properties['cross_section_name']

                cs_properties = ''
                if 'cross_section_properties' in element_set.set_properties:
                    cs_properties = element_set.set_properties['cross_section_properties']
                    #print 'Found cross_section_properties: ', element_set.set_properties['cross_section_properties']

                f.write("{} {} {} material {} set {}\n".format(cs_name, str(cs_id), cs_properties, str(cs_id), count))
    else:
        f.write("######### Crosssections here\n")

    # Materials
    f.write("######### Materials here\n")
    if write_materials:
        mat_id = 0
        count = 0
        for element_set_name, element_set in mesh.element_sets.items():
            if (write_2d_elements is False) and (element_set.dimension == 2):
                continue
            if element_set.dimension == 1:
                continue

            count += 1
            mat_name = 'MATERIAL_NAME'
            mat_properties = 'MATERIAL_PROPERTIES'

            if element_set_name[:4] == set_type_bulk:
                mat_name = 'IsoLE'
            elif element_set_name[:5] == "cohes":
                mat_name = 'IntMatIsoDamage'

            if element_set_name[:4] == set_type_bulk or element_set_name[:5] == "cohes":
                mat_id += 1

                if 'material_name' in element_set.set_properties:
                    mat_name = element_set.set_properties['material_name']

                if 'material_properties' in element_set.set_properties:
                    mat_properties = element_set.set_properties['material_properties']

                f.write("{} {} {}\n".format(mat_name, count, mat_properties))
                #f.write("BULK_MATERIAL\n")

    f.write("######### Boundary conditions here\n")
    if write_bcs:

        sets_passed = 0
        for element_set_name, element_set in mesh.element_sets.items():
            if (write_2d_elements is False) and (element_set.dimension == 2):
                continue
            if (element_set.dimension == 1):
                continue

            sets_passed += 1

        count = 0
        bc_ind = 0
        for element_set_name, element_set in mesh.element_side_sets.items():

            sets_passed += 1
            count += 1
            if 'boundary_condition_name' in element_set.set_properties and 'boundary_condition_properties' in element_set.set_properties:
                bc_ind += 1
                bc_name = element_set.set_properties['boundary_condition_name']
                bc_props = element_set.set_properties['boundary_condition_properties']
                f.write("{} {} set {} {}\n".format(bc_name, bc_ind, sets_passed, bc_props))

        #disp_z = 0
        #for n in mesh.nodes.values():
        #    disp_z = max(disp_z, n.c[2])
        #f.write("BoundaryCondition 1 loadTimeFunction 1 values 3 0. 0. 0. dofs 3 1 2 3 set {}\n".format(0))
        #f.write("BoundaryCondition 2 loadTimeFunction 2 values 3 0. 0. {:e} dofs 3 1 2 3 set {}\n".format(disp_z, 0))

    f.write("######### Load time functions here\n")
    if write_ltf:
        f.write("ConstantFunction 1 f(t) 0.\n")
        f.write("PiecewiseLinFunction 2 npoints 2  f(t) 2 0. 1.   t 2 0. 1.\n")

    # Sets
    set_id = 0
    # Element sets
    for element_set_name, element_set in mesh.element_sets.items():
        if (write_2d_elements is False) and (element_set.dimension == 2):
            continue
        if (element_set.dimension == 1):
            continue
        set_id += 1
        f.write("# " + element_set_name)
        f.write("\nSet {} elements {} ".format(str(set_id), str(len(element_set.ids))))
        f.write(''.join('{} '.format(k) for k in element_set.ids)[:-1])
        f.write("\n")

    # Element side sets
    for side_set_name, side_set in mesh.element_side_sets.items():
        set_id += 1
        f.write("# " + side_set_name)
        f.write("\nSet {} elementboundaries {} ".format(
            str(set_id), str(2 * len(side_set.sides))))
        f.write(''.join('{} {}  '.format(k.elem, k.side)
                        for k in side_set.sides)[:-1])
        f.write("\n")

    # Node sets
    for node_set_name, node_set in mesh.node_sets.items():
        set_id += 1
        f.write("# " + node_set_name)
        f.write("\nSet {} nodes {} ".format(
            str(set_id), str(len(node_set.ids))))
        f.write(''.join('{} '.format(k) for k in node_set.ids)[:-1])
        f.write("\n")

        # For testing
        # f.write("\nSimpleCS 1\n")
        # f.write("IsoLE 1 d 1. E 30.e6 n 0.2 tAlpha 1.2e-5\n")
        # f.write("BoundaryCondition  1 loadTimeFunction 1 prescribedvalue 0.0\n")
        # f.write("PeakFunction 1 t 1.0 f(t) 1.\n")

    f.close()
