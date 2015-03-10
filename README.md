Phon
=====

[![Build Status](https://travis-ci.org/KristofferC/Phon.svg?branch=master)](https://travis-ci.org/KristofferC/Phon) [![Coverage Status](https://coveralls.io/repos/KristofferC/Phon/badge.png?branch=master)](https://coveralls.io/r/KristofferC/Phon?branch=master)


Phon is Python package which main purpose is to insert cohesive elements between grains
in a given mesh and export the new mesh.

The workflow with Phon can be summarized as:

* Parse a generated mesh file from ex. Neper (http://neper.sourceforge.net/)
* Insert cohesive elements between grains in the parsed mesh.
* Exports the mesh to formats readable by Abaqus and OOFEM.
* Run FE analysis on the exported mesh.

### Documentation

Documentation can be found at http://phon.readthedocs.org.

### Authors

Kristoffer Carlsson - kristoffer.carlsson@chalmers.se

### Copyright and Licensing

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