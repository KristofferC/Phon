.. _installation:

Installation
------------

Phon can be installed on most computers with a standard Python installation. [Numpy](http://www.numpy.org/) is used internally
so this needs to be available to the Python installation.

Phon supports Python 2.7, 2.2, 3.3 and 3.4.


Git
===

The easiest way to get the latest version is by git. To download the
repository the following command is used::

    $ git clone https://github.com/KristofferC/Phon.git

This will give you a folder called "Phon". Navigate to this folder and execute the
following::

    $ python setup.py install

This should install the package to the system. To see if the installation is successful
try to import the package by executing::

    >>> import phon

in the Python terminal window.

To update to the latest version, go into your repository and execute::

    $ git pull origin master

and rerun the setup file.

Zip and Tar
===========

You can also get the latest version compressed as a .zip or .tar from the projects homepage: http://kristofferc.github.io/Phon/