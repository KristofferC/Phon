from phon.mesh_objects.element_side_set import ElementSideSet
from phon.mesh_objects.element_side_set import ElementSide


def create_element_sides(mesh, mesh_dimension=3):
    """
    Creates elements of mesh_dimension - 1 along the interfaces
    between grains.

    :param mesh: The mesh
    :type: mesh: :class:`Mesh`
    :param mesh_dimension: The dimension of the bulk elements
    :type mesh_dimension: int
    """
    if mesh_dimension == 3:
        set_type_bulk = "poly"
        set_type_interface = "face"
    elif mesh_dimension == 2:
        set_type_bulk = "face"
        set_type_interface = "edge"
    else:
        raise UnsupportedDimensionError

    element_to_grain = [0] * len(mesh.elements)
    node_to_elements = [list() for n in range(0, len(mesh.nodes))]
    for element_set_name, element_set in mesh.element_sets.iteritems():
        if not element_set_name.startswith(set_type_bulk):
            continue
        grain = int(element_set_name[4:])
        for el_num in element_set.ids:
            element_to_grain[el_num - 1] = grain
            for n in mesh.elements[el_num].vertices:
                node_to_elements[n - 1].append(el_num)

    mesh.element_side_sets["outer"] = ElementSideSet("outer")
    for element_set_name, face_set in mesh.element_sets.iteritems():
        if not element_set_name[0:4] == set_type_interface:
            continue

        # We should create a proper element-side-set out of this "face-set", we'll just give it the same name though
        for face_id in face_set.ids:
            connected_tets = []
            face = mesh.elements[face_id]
            for element_id in node_to_elements[face.vertices[0] - 1]:
                element = mesh.elements[element_id]

                if mesh_dimension == 3:
                    # Need to determine which of the faces of the tet are active
                    if set(face.vertices) == {element.vertices[0], element.vertices[1], element.vertices[3]}:
                        connected_tets.append(ElementSide(element_id, 1))
                    elif set(face.vertices) == {element.vertices[0], element.vertices[2], element.vertices[1]}:
                        connected_tets.append(ElementSide(element_id, 2))
                    elif set(face.vertices) == {element.vertices[0], element.vertices[3], element.vertices[2]}:
                        connected_tets.append(ElementSide(element_id, 3))
                    elif set(face.vertices) == {element.vertices[1], element.vertices[2], element.vertices[3]}:
                        connected_tets.append(ElementSide(element_id, 4))
                elif mesh_dimension == 2:
                    # print 'face.vertices: ', face.vertices

                    if len(face.vertices) == 2:
                        # Linear element
                        if set(face.vertices) == {element.vertices[0], element.vertices[1]}:
                            connected_tets.append(ElementSide(element_id, 1))
                        elif set(face.vertices) == {element.vertices[1], element.vertices[2]}:
                            connected_tets.append(ElementSide(element_id, 2))
                        elif set(face.vertices) == {element.vertices[2], element.vertices[0]}:
                            connected_tets.append(ElementSide(element_id, 3))

                if len(face.vertices) == 3:
                    # Quadratic elements
                    if set(face.vertices) == {element.vertices[0], element.vertices[3], element.vertices[1]}:
                        # print 'Found side 1.'
                        connected_tets.append(ElementSide(element_id, 1))
                    elif set(face.vertices) == {element.vertices[1], element.vertices[4], element.vertices[2]}:
                        # print 'Found side 2.'
                        connected_tets.append(ElementSide(element_id, 2))
                    elif set(face.vertices) == {element.vertices[2], element.vertices[5], element.vertices[0]}:
                        # print 'Found side 3.'
                        connected_tets.append(ElementSide(element_id, 3))

            # print 'len(connected_tets): ', len(connected_tets)

            if len(connected_tets) == 1:
                # Create a set for the entire surrounding domain
                mesh.element_side_sets["outer"].sides.extend(connected_tets)
                # Create a set for the single facet
                # mesh.element_side_sets[element_set_name].sides.extend(connectes_tets)
            elif len(connected_tets) == 2:
                pass
                # print("Doing nothing here for now...\n")
                # Must be 2 connected tets in this case
                # Do some clever data structure for preparing cohesive zones here
                # mesh.element_internal_boundaries[sort(set_name].()


class UnsupportedDimensionError(Exception):
    """
    Exception to raise when wrong dimension given to create_element_sides

    """

    def __init__(self, status):
        """Creates an exception with a status."""
        Exception.__init__(self, status)
        self.status = status

    def __str__(self):
        """Return a string representation of the :exc:`UnsupportedDimensionError`."""
        return str(self.status)