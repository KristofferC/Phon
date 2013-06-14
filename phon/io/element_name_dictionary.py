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

"""
Currently contains some dictionaries to translate between element names
used by different softwares (external names). Internally elements are stored in the
same format Abaqus uses. Also contains list of elements what dimension different 
elements have.

TODO: The location of this file is a bit awkward at the moment.
"""

# Translates between (internal_name, "software) to external_name.
element_dictionary =  {("CPE3", "abaqus") : "CPE3",
                       ("CPE3", "oofem") : "TrplaneStrain",
                       ("C3D4", "abaqus") : "C3D4",
                       ("C3D4", "oofem") : "LTRSpace"}

# Translates between (external_name, software) to internal_name.
element_dictionary_inverse  =  {("CPE3", "abaqus") : "CPE3",
                                ("TrplaneStrain", "oofem") : "CPE3",
                                ("C3D4", "abaqus") : "C3D4",
                                ("LTRSpace", "oofem") : "C3D4"}
        
# Dimension of elements.
elements_2d = ["CPE3"]
elements_3d = ["C3D4"]