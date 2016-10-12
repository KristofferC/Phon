Exporting a mesh
----------------

The mesh can currently be exported to a format readable by either `Abaqus`_ or `OOFEM`_.

One of the arguments to the export functions is if 2D elements should be exported. The reason for this is
that currently the elements in the grain boundary are not deleted after insertion of interface elements. When
xporting a 3D mesh we might want to ignore the left over 2D elements.

Exporting to Abaqus
===================

Assume that we have a mesh stored in the ``mesh`` variable. If we want to export this to abaqus
and ignore the 2D elements in the mesh it would be done like this:

    >>> from phon.io_tools.write.export_to_abaqus import export_to_abaqus
    >>> export_to_abaqus("output_file.inp", mesh, write_2d_elements=False)

This file can then be imported into Abaqus CAE. If you are doing 2D analysis you would want to
set ``write_2d_elements=True``.


Exporting to OOFEM
===================

A mesh object can be exported to OOFEM as follows::

    >>> from phon.io_tools.write.export_to_oofem import export_to_oofem
    >>> export_to_oofem("output_file.inp", mesh, write_2d_elements=False)

The generated file only contains the parts of the file relevant to the mesh. The rest of the
analysis records must be manually added in order to perform analyses.

.. _OOFEM: http://www.oofem.org/en/oofem.html
.. _Abaqus: http://www.3ds.com/products/simulia/portfolio/abaqus/