.. Phon documentation master file, created by
   sphinx-quickstart on Fri Jun 14 17:26:54 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Phon's documentation!
================================

Phon is a Python library which has the following features:

* Parse meshes created in Abaqus' .inp and Gmsh format and stores it into an internal
  class based representation.
  Element and node sets are also parsed and stored.
* Can out of the box insert interface elements between grains in both 2D and 3D meshes
  generated with `Neper <http://neper.sourceforge.net/>`_.
* Can export back the mesh for analysis to either Abaqus .inp or `OOFEM's <http://www.oofem.org/>`_ .in format.

The most common way Phon is used right now is to generate a mesh with Neper, then using Phon the mesh is parsed, interface
elements are included and the resulting mesh is then exported for FE-analysis.

This is the central page for all of Phon's documentation.

Contents
=========

.. toctree::
   :maxdepth: 2

   Installation <installation/index.rst>
   Usage <examples/index.rst>

.. Modules <modules.rst>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`

Information
-----------

:Author: Kristoffer Carlsson - kristoffer.carlsson@chalmers.se
:Version: 0.4
:License: MIT License
:Source: https://github.com/KristofferC/phon