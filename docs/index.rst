.. Phon documentation master file, created by
   sphinx-quickstart on Fri Jun 14 17:26:54 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Phon's documentation!
================================

Phon is a Python package that provides the functionality to read
and export mesh files to different software's. It has the following
features:

* Parses generated mesh files from Neper (http://neper.sourceforge.net/) and stores it
  into a class based representation.
* Can insert cohesive elements between grains in a Voronoi tesselated mesh.
* Can currently export the mesh to formats readable by Abaqus and OOFEM.


Contents:

.. toctree::
   :maxdepth: 3

   Installation <installation/index.rst>
   Examples <examples/index.rst>
   Library <library/index.rst>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Information
-----------

:Author: Kristoffer Carlsson
:Version: 0.1
:License: MIT License
:Source: https://github.com/KristofferC/phon