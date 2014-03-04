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

from collections import defaultdict

from phon.mesh_objects.element import Element
from phon.mesh_objects.element_set import ElementSet
from phon.mesh_objects.node import Node


def create_cohesive_elements(mesh):
    """
    Creates and inserts cohesive elements between the grains in the mesh.
    The element sets, ordering of vertices in elements etc etc need to
    follow the convention from Neper.

    :param mesh: The mesh
    :type mesh: :class:`Mesh`
    """

    n_nodes = len(mesh.nodes)
    cohesive_id_offset = max(mesh.elements.keys()) + 1
    mesh.element_indices["COH3D6"] = []
    #nodes_in_face_sets = get_nodes_in_all_face_sets(mesh)
    node_id_grain_LUT = get_node_id_grain_LUT(mesh)

    for element_set_name in mesh.element_sets.keys():
        if not element_set_name[0:4] == "face":
            continue
        face_set = mesh.element_sets[element_set_name]
        grains_connected_to_face = get_grains_connected_to_face(mesh,
                                                                face_set,
                                                                node_id_grain_LUT)

        # Ignore sets at boundary
        if len(grains_connected_to_face) == 1:
            continue

        grain_id_1 = grains_connected_to_face[0]
        grain_id_2 = grains_connected_to_face[1]
        cohesive_set_name = ("cohes" + str(grain_id_1) + "_" +
                             str(grain_id_2))
        cohesive_set = ElementSet(cohesive_set_name, dimension=3)
        mesh.element_sets[cohesive_set_name] = cohesive_set

        # For each node in face make two new at the same place
        for node_id in face_set.get_all_node_ids(mesh):
            original_node = mesh.nodes[node_id]
            new_node_id_1 = node_id + n_nodes * grain_id_1
            new_node_id_2 = node_id + n_nodes * grain_id_2
            mesh.nodes[new_node_id_1] = Node(original_node.x, original_node.y, original_node.z)
            mesh.nodes[new_node_id_2] = Node(original_node.x, original_node.y, original_node.z)

            # Reconnect the tetrahedron with a vertex in the node that is being duplicated
            # to one of the new nodes.
            grain_ids, tetra_ids = get_tetra_and_grain_with_node_id(mesh, node_id, grain_id_1, grain_id_2)
            for grain_id, tetra_id in zip(grain_ids, tetra_ids):
                idx = mesh.elements[tetra_id].vertices.index(node_id)
                mesh.elements[tetra_id].vertices[idx] = node_id + n_nodes * grain_id

            # If we are adding nodes at the boundary these need to be 
            # added to the correct boundary node set. We also need to
            # remove old nodes from the node sets.
            for node_set_name, node_set in mesh.node_sets.iteritems():
                if node_id in node_set.ids:
                    node_set.ids.remove(node_id)
                    node_set.ids.extend([new_node_id_1, new_node_id_2])

        # Create the cohesive elements
        for triangle_element_id in face_set.ids:
            triangle_element = mesh.elements[triangle_element_id]
            cohesive_index_order = [1, 0, 2, 4, 3, 5]
            vertices_cohesive = [0, 0, 0, 0, 0, 0]

            for i, node_id in enumerate(triangle_element.vertices):
                vertices_cohesive[cohesive_index_order[i]] = node_id + n_nodes * grain_id_1
                vertices_cohesive[cohesive_index_order[i + 3]] = node_id + n_nodes * grain_id_2

            cohesive_element = Element("COH3D6", vertices_cohesive)
            mesh.elements[cohesive_id_offset] = cohesive_element
            mesh.element_indices["COH3D6"].append(cohesive_id_offset)
            mesh.element_sets[cohesive_set_name].ids.append(cohesive_id_offset)
            cohesive_id_offset += 1


def get_nodes_in_all_face_sets(mesh):
    """
    This function finds all nodes that sits in a face.
    :param mesh:
    :type mesh: :class:`Mesh`
    :return: The node identifiers in all faces
    :rtype: list[ints]
    """
    nodes_in_face_sets = set()
    for element_set_name, element_set in mesh.element_sets.iteritems():
        if not element_set_name.startswith("face"):
            continue
        nodes_in_face_sets.add(element_set.get_all_node_ids(mesh))
    return list(nodes_in_face_sets)


def get_grains_connected_to_face(mesh, face_set, node_id_grain_LUT):
    """
    This function find the grain connected to the face set given as argument.

    Three nodes on a grain boundary can all be intersected by one grain
    in which case the grain face is on the boundary or by two grains. It
    is therefore sufficient to look at the set of grains contained by any 
    three nodes in the face set and take the intersection of these sets.

    :param mesh: The mesh
    :type mesh: :class:`Mesh`
    :param face_set: The face set to find grains connected to
    :type: face_set: :class:`ELementSet`
    :param node_id_grain_LUT: Lookup table to find what grains contain
                              what nodes.
    :type node_id_grain_LUT: defaultdict
    :return: The grain identifiers that intersect the face.
    :rtype: list of ints
    """

    grains_connected_to_face = []
    triangle_element = mesh.elements[face_set.ids[0]]

    for node_id in triangle_element.vertices:
        grains_with_node_id = node_id_grain_LUT[node_id]
        grains_connected_to_face.append(set(grains_with_node_id))

    return list(set.intersection(*grains_connected_to_face))


def get_node_id_grain_LUT(mesh):
    """
    This function creates a (default) dictionary that
    works as a lookup table for what grains contain
    what nodes.
    :param mesh: The mesh
    :type: mesh: :class:`Mesh`
    :param node_list: The list of node identifiers that is to be used
                      as keys in the dict
    :type node_list: list[ints]
    :return: Dictionary d where d[node_id] gives a set of the grain identifiers
             that contain the node.
    :rtype: defaultdict
    """
    d = defaultdict(set)
    for element_set_name, element_set in mesh.element_sets.iteritems():
        if not element_set_name.startswith("poly"):
            continue
        for element_id in element_set.ids:
            vertices = mesh.elements[element_id].vertices
            for node_id in vertices:
                d[node_id].add(int(element_set_name[4:]))
    return d


def get_grains_containing_node_id(mesh, node_id, original_n_nodes):
    """
    This function finds all the grains that contain the
    node with node identifier node_id.

    :param mesh: The mesh
    :type: mesh: :class:`Mesh`
    :param node_id: The identifier of the node
    :type node_id: int
    :param original_n_nodes: The number of nodes in the mesh before any duplication
                             of nodes has taken place.
    :type original_n_nodes: int
    """

    grain_ids_with_node_id = []

    for element_set_name, element_set in mesh.element_sets.iteritems():
        if not element_set_name[0:4] == "poly":
            continue
        for element_id in element_set.ids:
            vert_mod = [x % original_n_nodes for x in mesh.elements[element_id].vertices]
            if node_id in vert_mod:
                grain_ids_with_node_id.append(int(element_set_name[4:]))
                break
    grain_ids_with_node_id = list(set(grain_ids_with_node_id))
    return grain_ids_with_node_id


def get_tetra_and_grain_with_node_id(mesh, node_id, grain_id_1, grain_id_2):
    """
    Find the tetrahedrons that has one vertex with the node identifier node_id
    and if it belongs to grain with identifier grain_id_1 or grain_id_2

    :param mesh: The mesh.
    :type mesh: :class:`Mesh`
    :param node_id: THe node to find the tet
    :type node_id: int
    :param grain_id_1: Identifier for the first grain.
    :type grain_id_1: int
    :param grain_id_2: Identifier for the second grain.
    :type grain_id_2: int
    :return: Returns a tuple of the grain identifier the tetrahedron is
             in and the identifier of the element.
    :rtype: tuple (int, int)

    """
    tetras = []
    grains = []

    for grain_id in [grain_id_1, grain_id_2]:
        for element_id in mesh.element_sets["poly" + str(grain_id)].ids:
            element = mesh.elements[element_id]
            if node_id in element.vertices:
                tetras.append(element_id)
                grains.append(grain_id)

    return grains, tetras
