Exporting a mesh
----------------

The mesh can currently be exported to a format readable by either `Abaqus`_ or `OOFEM`_.


Exporting to Abaqus
===================

A mesh object can be exported to abaqus as follows::

    >>> from phon.io.write.export_to_abaqus import export_to_abaqus
    >>> export_to_abaqus("output_file.inp", mesh)

This file can then be imported into Abaqus CAE.

|

.. figure:: ..\figures\abaq.png
    :width: 800
    :align: center

    Mesh were cohesive elements have been inserted

|

Exporting to OOFEM
===================

A mesh object can be exported to OOFEM as follows::

    >>> from phon.io.write.export_to_oofem import export_to_oofem
    >>> export_to_oofem("output_file.inp", mesh)

The generated file only contains the parts of the file relevant to the mesh. The rest of the
analysis records must be manually added in order to perform analyses.

.. figure:: ..\figures\oofem.png
    :width: 800
    :align: center

    Resulting stress in a crystal plasticity model exposed to uniaxial tensilie loading,
    analyzed in OOFEM.


.. _OOFEM: http://www.oofem.org/en/oofem.html
.. _Abaqus: http://www.3ds.com/products/simulia/portfolio/abaqus/