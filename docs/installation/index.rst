.. _installation:

Installation
------------

Source
======

The easiest way to get the latest version is by git. To download the
repository the following command is used::

    $ git clone https://github.com/KristofferC/Phon.git

This will give you a folder called "Phon". Change to this folder and execute the
following::

    $ python setup.py install

This should install the package to the system. To see if the installation is sucessful
try to import the package by executing::

    >>> import phon

in the Python terminal window.

To update to the latest version, go into your repository and execute::

    $ git pull origin master

and rerun the setup file.


Documentation
=============
To build the documentation the tool `Sphinx`_ is needed. After it is installed
execute the command::

     $ make html

to build the html documentation.

.. _Sphinx: http://sphinx-doc.org/