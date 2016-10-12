Reading and querying mesh
-------------------------

Reading a mesh is in Phon the process of parsing a file containing nodes, elements, and eventual sets (element sets
and node sets). This information is then stored in a class based format in Phon which is easy to query and modify
the mesh.

It is currently possible to read a mesh exported to Abaqus' .inp format or Gmsh's .msh format.

Read an Abaqus mesh
===================

The function to read an Abaqus mesh is  :func:`phon.io.read.read_from_abaqus_inp.read_from_abaqus_inp`.

To read the mesh, the function is first imported and then used like this::

    >>> from phon.io_tools.read.read_from_abaqus_inp import read_from_abaqus_inp
    >>> mesh = read_from_abaqus_inp("n10-id1.inp")

The mesh is now stored as an instance of the :class:`phon.mesh_objects.mesh()` class.

An example Abaqus mesh file can
be found `here <https://raw.githubusercontent.com/KristofferC/Phon/8714c92ffadbb66a32cf091b548950e57ddcffd9/test/n10-id1.inp>`_.


Gmsh
====
The function to read a Gmsh mesh is  :func:`phon.io_tools.read.read_from_gmsh.read_from_gmsh`.

It is currently used a bit differently than the function to read from Abaqus meshes. The gmsh reader
assumes that each grain has a separate mesh file called *fileX.msh* where *file* is the basename and *X* is
the grain id. The gmsh reader can then be called as::

    >>> from phon.io_tools.read.read_from_gmsh import read_from_gmsh
    >>> basename = "gmsh_grain_file"
    >>> n_grains = 3
    >>> mesh = read_from_gmsh(base, n_grains)

An example of a microstructure with 3 grains split over 3 .msh files can be seen `here <https://github.com/KristofferC/Phon/tree/master/test/mesh_test_files>`_.

Querying and modifying the mesh
===============================

We can now query the mesh object for information about the mesh and modify it.

A few example follows here:

* The number of elements in the mesh::

    >>> print(len(mesh.elements))
    1683


* The number of nodes in the mesh::

    >>> print(len(mesh.nodes))
    289

* A node set with a certain name::

    >>> print(mesh.node_sets["x0y0"])
    Node set with name x0y0 containing nodes with the following ids [1, 3, 34, 39, 40, 131, 132]

* Information about a specific node::

    >>> print(mesh.nodes[10])
    Node located at (0.722422, 0.420036, 0.196344)

* Changing a nodes location::

    >>> mesh.nodes[10].c[0] = 1337.0
    >>> print(mesh.nodes[10])
    Node located at (1337.000000, 0.420036, 0.196344):

* Information about a specific element::

    >>> print(mesh.elements[701])
    Element of type C3D4 containing the vertices with id [168, 150, 154, 60].


For more information of the different properties to query from the mesh
look at the documentation of :mod:`phon.mesh_objects`.
