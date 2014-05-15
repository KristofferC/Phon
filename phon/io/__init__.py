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

__all__ = ["element_name_dictionary", "read", "write"]

# This stuff here need to be done in a better way...

# Translates between (internal_name, "software) to external_name.
element_dictionary = {("CPE3", "abaqus"): "CPE3",
                      ("CPE3", "oofem"): "TrPlaneStress2d",
                      ("CPE6", "abaqus"): "CPE6",
                      ("CPE6", "oofem"): "QTrPlStr",
                      ("C3D4", "abaqus"): "C3D4",
                      ("C3D4", "oofem"): "LTRSpace",
                      ("C3D10", "abaqus"): "C3D10",
                      ("C3D10", "oofem"): "QTRSpace",
                      ("COH3D6", "abaqus"): "COH3D6",
                      ("COH3D6", "oofem"): "Interface3dtrlin",
                      ("STRI65", "abaqus"): "STRI65",
                      ("STRI65", "oofem"): "tr2shell7",
                      ("CPS4R", "abaqus"): "CPS4R",
                      ("CPS4R", "oofem"): "tr2shell7",
                      ("COH3D12", "abaqus"): "COH3D12",
                      ("COH3D12", "oofem"): "Interface3dtrquad"}

# Translates between (external_name, software) to internal_name.
element_dictionary_inverse = {("CPE3", "abaqus"): "CPE3",
                              ("TrPlaneStress2d", "oofem"): "CPE3",
                              ("CPE6", "abaqus"): "CPE6",
                              ("QTrPlStr", "oofem"): "CPE6",
                              ("C3D4", "abaqus"): "C3D4",
                              ("LTRSpace", "oofem"): "C3D4",
                              ("C3D10", "abaqus"): "C3D10",
                              ("QTRSpace", "oofem"): "C3D10",
                              ("COH3D6", "abaqus"): "COH3D6",
                              ("Interface3dtrlin", "oofem"): "COH3D6",
                              ("STRI65", "abaqus"): "STRI65",
                              ("tr2shell7", "oofem"): "STRI65",
                              ("CPS4R", "abaqus"): "CPS4R",
                              ("tr2shell7", "oofem"): "CPS4R",
                              ("COH3D12", "abaqus"): "COH3D12",
                              ("Interface3dtrquad", "oofem"): "COH3D12"}

# Dimension of elements.
elements_2d = ["CPE3", "STRI65", "CPS4R", "CPE6"]
elements_3d = ["C3D4", "C3D10", "COH3D6", "COH3D12"]
