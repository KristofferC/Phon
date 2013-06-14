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

def create_cohesive_elements(mesh):
    """
    Creates and inserts cohesive elements between the grains in the mesh.

    Just use neper with order = 1 and import with read_from_neper and everything
    will be fine.
    """

    n_nodes = len(mesh.nodes)
    cohesive_id_offset = max(mesh.elements.keys()) + 1
    mesh.element_indices["COH3D6"] = []

    for it, element_set_name in enumerate(mesh.element_sets.keys()):
        if not element_set_name[0:4] == "face":
            continue
        face_set = mesh.element_sets[element_set_name]
        grains_connected_to_face = _get_grains_connected_to_face(mesh, face_set, n_nodes)
        

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
            grain_ids, tetra_ids = _get_tetra_and_grain_with_node_id(mesh, node_id, grain_id_1, grain_id_2)
            for grain_id, tetra_id in zip(grain_ids, tetra_ids):
                idx = mesh.elements[tetra_id].vertices.index(node_id)
                mesh.elements[tetra_id].vertices[idx] = node_id + n_nodes * grain_id
  
            # If we are adding nodes at the boundary these need to be 
            # added to the correct boundary node set.
            for node_set_name in mesh.node_sets.keys():
                node_set = mesh.node_sets[node_set_name]
                if node_id in node_set.ids:
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
           


def _get_grains_connected_to_face(mesh, face_set, original_n_nodes):
    """
    This function find the grain connected to the face set given as argument.

    Three nodes on a grain boundary can all be intersected by one grain
    in which case the grain face is on the boundary or by two grains. It
    is therefore sufficient to look at the set of grains contained by any 
    three nodes in the face set and take the intersection of these sets.
    """

    grains_connected_to_face = []
    triangle_element = mesh.elements[face_set.ids[0]]

    for node_id in triangle_element.vertices:
        grains_with_node_id = _get_grains_containing_node_id(mesh, node_id,  original_n_nodes)
        grains_connected_to_face.append(set(grains_with_node_id))

    return list(set.intersection(*grains_connected_to_face))

def _get_grains_containing_node_id(mesh, node_id, original_n_nodes):
    """
    This function finds all the grains that contain the
    node with node identifier node_id.
    """

    grain_ids_with_node_id = []

    for element_set_name in mesh.element_sets.keys():
        if not element_set_name[0:4] == "poly":
            continue
        element_set = mesh.element_sets[element_set_name]
        for element_id in element_set.ids:
            vert_mod = [x % original_n_nodes for x in mesh.elements[element_id].vertices]
            if node_id in vert_mod:
                grain_ids_with_node_id.append(int(element_set_name[4:]))
                break
    grain_ids_with_node_id = list(set(grain_ids_with_node_id))
    return grain_ids_with_node_id


def _renumber_nodes(mesh):
    """
    Renumbers nodes so that they are "dense" on the number line. 
    For example, if the mesh consist of four nodes with identifiers
    1, 2, 5, 7 this would change them to 1, 2, 3, 4. This method also
    updates the elements to use the renumbered node identifiers.

    TODO: This might be a useful function in general for the mesh class
    so it could be moved to be a method of the mesh class.
    """

    # Create dictionary of old and renumberd node identifiers
    node_renumber_dict = {}
    for i, node in enumerate(mesh.nodes.keys()):
        node_renumber_dict[node] = i

    # Update node identifiers in elements
    for element_id in mesh.elements.keys():
        for element in mesh.elements[element_id]:
            for i, node_id in enumerate(element.vertices):
                element.vertices[i] = node_renumber_dict[node_id]

    # Update node identifiers in node sets
    for node_set_name in mesh.node_sets.keys():
        node_set = mesh.node_sets[node_set_name]
        for i, node_id in enumerate(node_set.ids):
            node_set.ids[i] = node_renumber_dict[node_id]


def _get_tetra_and_grain_with_node_id(mesh, node_id, grain_id_1, grain_id_2):
    """
    Find the tetrahedrons in the grain with grain identifier grain_id_1 or graind_id_2 
    that has one vertex with the node identifier node_id
    """
    tetras = []
    grains = []

    for grain_id in [grain_id_1, grain_id_2]:
        for element_id in mesh.element_sets["poly" + str(grain_id)].ids:
            element = mesh.elements[element_id]
            if node_id in element.vertices:
                tetras.append(element_id)
                grains.append(grain_id)

    return (grains, tetras)

     

