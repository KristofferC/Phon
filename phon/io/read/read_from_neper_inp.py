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

import re

from phon.mesh_objects.element import Element
from phon.mesh_objects.element_set import ElementSet
from phon.mesh_objects.node import Node
from phon.mesh_objects.mesh import Mesh
from phon.mesh_objects.node_set import NodeSet

def read_from_neper_inp(filename, verbose=0):
    """ Takes a filename containing a .inp file from the software Neper and
    creates a Mesh class instance containing the data in the file. Verbose can
    be 0, 1, 2 for increasing levels of verbosity. """

    f = open(filename, "r")

    # Read header
    re_part = re.compile("\*Part, name=(.*)")
    line = f.readline()
    match = re_part.match(line)
    if not match:
        raise ReadInpFileError("Error parsing file. Expected '*Part, "
                               "name=XXX', read '" + line + "'.")

    # Initiate a mesh class with the same name as the part
    mesh = Mesh(match.group(1))

    ######
    
    # Read nodes
    line = f.readline()
    if not (line == "*Node\n"):
        raise ReadInpFileError("Error parsing file. Expected '*Node', read '" +
                               line + "'.")
    num_nodes = 0
    while True:
        line = f.readline()
        if (line.strip() == ''):
            break
        num_nodes += 1
        if verbose == 1:
            print ("\rReading nodes, %d nodes read" % (num_nodes)),
        #: Make line into this list :[id, x, y, z]
        node_numbers = map(to_number, line.strip().split(','))
        node = Node(*node_numbers[1:])
        mesh.nodes[node_numbers[0]] = node
        if verbose == 2:
            print ("Read {0}.\n".format(node))

    ######
        
    # Read elements
    reading_elements = True
    
    line = f.readline()
    re_part = re.compile("\*Element, type=(.*)")
    match = re_part.match(line)
    
    if not match:
        raise ReadInpFileError("\nError parsing file. Expected '*Element, \
        type=XXX', got '" + line + "'.")

    elem_name = re_part.match(line).group(1)
    num_trigs = 0
    while True:
        elem_dict = {}
        line = f.readline()
        # Stop reading triangles upon linebreak
        if (line.strip() == ''):
            break
        num_trigs += 1
        if verbose == 1:
            print ("\rReading triangles, %d triangles read" % (num_trigs)),
        
        element_numbers = map(to_number, line.strip().split(','))
        element = Element(elem_name, element_numbers[1:])
        mesh.elements_2d[element_numbers[0]] = element
        if verbose == 2:
            print ("Read {0}.\n".format(tri))
            
    
            
    line = f.readline()
    re_part = re.compile("\*Element, type=(.*)")
    match = re_part.match(line)
    if not match:
        raise ReadInpFileError("\nError parsing file. Expected '*Element, \
                type=XXX', got '" + line + "'.")
    elem_name = re_part.match(line).group(1)
    num_tetras = 0
    while True:
        elem_dict = {}
        line = f.readline()
        
        if (line.strip() == ''):
            break
        
        num_tetras += 1
        if verbose == 1:
            print ("\rReading tetrahedras, %d tetrahedras "
                   "read" % (num_tetras)),
        element_numbers = map(to_number, line.strip().split(','))
        element = Element(elem_name, element_numbers[1:])
        mesh.elements_3d[element_numbers[0]] = element

        if verbose == 2:
            print ("Read {0}.\n".format(tetra))

    
    # Read sets

    re_polyset = re.compile("\*Elset, elset=(poly\d*)")
    re_faceset = re.compile("\*Elset, elset=(face\d*)")
    re_nodeset = re.compile("\*Nset, nset=(.*)")

    ##################
    # Read 2D sets #
    ##################

    line = f.readline()
    match = re_faceset.match(line)
    if not match:
        raise ReadInpFileError("\nError parsing file. Expected '*Elset, \
                elset=faceX', got '" + line + "'.")
    num_facesets = 0
    while True:
        num_facesets += 1
        if verbose == 1:
            print ("\rReading face sets, %d face sets read" % (num_facesets)),
        faceset_name = re_faceset.match(line).group(1)
        faceset = ElementSet(faceset_name)
        # Read element ids until empty line
        full_str = ""
        while not line.strip() == "":
            line = f.readline()
            full_str += line.strip()
        faceset.ids = map(to_number, full_str.split(','))
        #mesh.faceSets.append(faceset)
        mesh.element_sets_2d[faceset_name] = faceset
        if verbose == 2:
            print ("Read {0}\n".format(faceset))
        line = f.readline()
        if re_faceset.match(line.strip()):
            continue
        if re_polyset.match(line.strip()):
            break
        else:
            raise ReadInpFileError("Error parsing file. Expected either "
            "'*Elset, elset=faceX' or '*Elset, elset=polyX', "
            "got '" + line + "'.")
    if verbose == 1 or verbose == 2:
        print ""


    # Read 3D sets 
    match = re_polyset.match(line)
    if not match:
        raise ReadInpFileError("Error parsing file. Expected '*Elset, \
                elset=polyX', got '" + line + "'.")
    num_polysets = 0
    while True:
        num_polysets += 1
        if verbose == 1:
            print ("\rReading polyhedral sets, %d polyhedral "
                   "sets read" % (num_polysets)),
        polyset_name = re_polyset.match(line).group(1)
        polyset = ElementSet(polyset_name)
        # Read element ids until empty line
        full_str = ""
        while not line.strip() == "":
            line = f.readline()
            full_str += line.strip()
        polyset.ids = map(to_number, full_str.split(','))
        mesh.element_sets_3d[polyset_name] = polyset
        #mesh.polySets.append(polyset)
        if verbose == 2:
            print ("Read: {0}\n".format(polyset))
        line = f.readline()
        if re_polyset.match(line.strip()):
            continue
        if re_nodeset.match(line.strip()):
            break
        else:
            raise ReadInpFileError("Error parsing file. Expected either \
            '*Elset, elset=polyX' or '*Nset, nset=X', got '" + line + "'.")

    ##################
    # Read node sets #
    ##################
    match = re_nodeset.match(line)
    if not match:
        raise ReadInpFileError("Error parsing file. Expected '*Nset, \
                nset=X', got '" + line + "'.")
    num_nodesets = 0
    EOF = False
    while True:
        num_nodesets += 1
        if verbose == 1:
            print ("\rReading node sets, %d node sets read" % (num_polysets)),
        nodeset_name = re_nodeset.match(line).group(1)
        nodeset = NodeSet(nodeset_name)
        # Read element ids until empty line
        full_str = ""
        while (not line.strip() == ""):
            line = f.readline()
            if line.strip() == "*End Part":
                EOF = True
                break
            full_str += line.strip()
        nodeset.ids = map(to_number, full_str.split(','))
        mesh.node_sets[nodeset_name] = nodeset
        #mesh.nodeSets.append(nodeset)
        if EOF:
            break
        if verbose == 2:
            print "Read {0}".format(nodeset)
        if line == "*End Part":
            break
        line = f.readline()
        if re_nodeset.match(line.strip()):
            continue

    if verbose == 1 or verbose == 2:
        print "\nFile {0} parsed sucessfully!".format(filename)

    return mesh

class ReadInpFileError(Exception):
    """
    Exception to raise when there is a problem reading the input file to
    the parser function.
    """
    
    pass


def to_number(s):
    """
    Converts a string to a int if possible, else a float.
    """
    
    try:
        return int(s)
    except ValueError:
        return float(s)
