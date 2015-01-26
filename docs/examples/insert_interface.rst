Create cohesive elements
------------------------

Cohesive elements are elements modelling an interface law between for example
grains in a model of a polycrystalline material. Phon has support for inserting
these elements into a mesh. This is done with the function
:func:`phon.mesh_tools.create_cohesive_elements.create_cohesive_elements()`. It
is currently only possible to export a mesh with cohesive elements to the Abaqus format.

The function generates element sets of the cohesive elements. These have the name
``cohesX_Y`` where X and Y are identifiers to the two grains that share the grain
boundary.

An example of a mesh being read, cohesive elements inserted into it and then getting exported
is shown below.::

    >>> from phon.io.read.read_from_neper_inp import read_from_neper_inp
    >>> from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements
    >>> from phon.io.write.export_to_abaqus import export_to_abaqus
    >>> mesh = read_from_neper_inp("n10-id1.inp")
    >>> create_cohesive_elements(mesh)
    >>> export_to_abaqus("cohesive_file.inp", mesh)

If you want to insert
  interface elements in a mesh generated with some other software you need to provide element sets with the same name used by Neper must