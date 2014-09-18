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

import numpy as np

from phon.mesh_objects.element import Element
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements

#TODO: Rewrite this with numpy...

def create_matrix(mesh, thickness, order):
    """
    This method creates elements that are similar to the cohesive
    elements except that they have a finite width. The cohesive
    elements are made thicker by pulling them apart in the normal
    direction of the cohesive element.

    :param thickness: Thickness of the generated elements
    :type thickness: Float
    :param mesh: The mesh
    :type mesh: :class:`Mesh`

    """

    corner_sets = ["x0y0z0", "x0y0z1", "x0y1z0", "x0y1z1",
                   "x1y0z0", "x1y0z1", "x1y1z0", "x1y1z1"]

    edge_sets = ["x0y1", "x0z1", "x0y0", "x0z0",
                 "x1y0", "x1z1", "x1y1", "x1z0",
                 "y0z1", "y0z0", "y1z0", "y1z1"]

    face_sets = ["x0", "x1", "y0", "y1", "z0", "z1"]

    # Loop over every cohesive element set:
    create_cohesive_elements(mesh)

    normal_vec = {}
    # Pre calculate the normals
    for element_set_name in mesh.element_sets.keys():
        if "coh_face" in element_set_name:
            element_set = mesh.element_sets[element_set_name]
            for element_id in element_set.ids:

                normal_vec[element_id] = _calculate_normal(mesh, mesh.elements[element_id])
    for element_set_name in mesh.element_sets.keys():
        if "coh_face" in element_set_name:
            node_already_moved = []
            element_set = mesh.element_sets[element_set_name]

            # Loop over elements in face set
            for element_id in element_set.ids:
                element = mesh.elements[element_id]

                # Loop over the nodes in the element
                for i, node_id in enumerate(element.vertices):

                    if node_id in node_already_moved:
                        continue
                    node_already_moved.append(node_id)
                    node = mesh.nodes[node_id]

                    r = find_displacement_vector(mesh, node_id, corner_sets,
                                                 edge_sets, face_sets, normal_vec[element_id], thickness)

                    node.x += r[0]
                    node.y += r[1]
                    node.z += r[2]

                   # if node.x > 1.0 or node.x < 0.0:
                   #     node.x -= r[0]
                   # if abs(node.y) > 1.0 or node.y < 0.0:
                   #     node.y -= r[1]
                   # if abs(node.z) > 1.0 or node.z < 0.0:
                   #     node.z -= r[2]


def find_displacement_vector(mesh, node_id, corner_sets, edge_sets, face_sets, normal_vec, thickness):

    # For now ignore projection stuff
    # TODO: Fix

    return normal_vec * thickness / 2.0


    for node_set_name in corner_sets:
        if node_id in mesh.node_sets[node_set_name].ids:
            return [0, 0, 0]

    for node_set_name in edge_sets:
        if node_id in mesh.node_sets[node_set_name].ids:

            return project_on_line(node_set_name, normal_vec, thickness)

    for node_set_name in face_sets:
        if node_id in mesh.node_sets[node_set_name].ids:
            if node_id == 2942:
                print "hejj"
            return project_on_plane(node_set_name, normal_vec, thickness)


def project_on_line(node_set_name, normal_gb, thickness):
    line_dirs = {"x0y1": np.array([0, 0, 1]),
                 "x0z1": np.array([0, 1, 0]),
                 "x0y0": np.array([0, 0, 1]),
                 "x0z0": np.array([0, 1, 0]),
                 "x1y0": np.array([0, 0, 1]),
                 "x1z1": np.array([0, 1, 0]),
                 "x1y1": np.array([0, 0, 1]),
                 "x1z0": np.array([0, 1, 0]),
                 "y0z1": np.array([1, 0, 0]),
                 "y0z0": np.array([1, 0, 0]),
                 "y1z0": np.array([1, 0, 0]),
                 "y1z1": np.array([1, 0, 0])}

    line_dir = line_dirs[node_set_name]
    length_line = thickness / 2.0 / np.dot(line_dir, normal_gb)
    return line_dir * length_line


def project_on_plane(node_set_name, normal_gb, thickness):
    normal_planes = {"z0": np.array([0, 0, -1]),
                     "z1": np.array([0, 0, 1]),
                     "x0": np.array([-1, 0, 0]),
                     "x1": np.array([1, 0, 0]),
                     "y0": np.array([0, -1, 0]),
                     "y1": np.array([0, 1, 0])}

    normal_plane = normal_planes[node_set_name]

    np_dot_ng = np.dot(normal_plane, normal_gb)
    projection = normal_gb - np_dot_ng * normal_plane
    projection_normed = projection / np.linalg.norm(projection)
    length_plane = thickness / 2.0 / np.dot(projection, normal_gb)

    return projection_normed * length_plane


def _calculate_normal(mesh, element):
    """
    Calculates the normal to a cohesive element normalized
    to a length of 1.

    :param element: The cohesive element
    :type element: :class:`Element`
    :return: Array with the normal in the form [x,y,z]
    :rtype: Array with numbers
    """

    node_1 = mesh.nodes[element.vertices[0]]
    node_2 = mesh.nodes[element.vertices[1]]
    node_3 = mesh.nodes[element.vertices[2]]

    point_1 = np.array([node_1.x, node_1.y, node_1.z])
    point_2 = np.array([node_2.x, node_2.y, node_2.z])
    point_3 = np.array([node_3.x, node_3.y, node_3.z])

    crs = np.cross(point_2 - point_1, point_3 - point_1)
    return crs / np.linalg.norm(crs)
