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


# This stuff here need to be done in a better way...

# Translates between (internal_name, software) to external_name.
element_dictionary = {("T3D2", "abaqus"): "T3D2",
                      ("T3D2", "oofem"): "intelline1",
                      ("T3D4", "abaqus"): "T3D4",
                      ("T3D4", "oofem"): "intelline2B",
                      ("CPE3", "abaqus"): "CPE3",
                      ("CPE3", "oofem"): "TrPlaneStress2d",
                      ("CPE6", "abaqus"): "CPE6",
                      ("CPE6", "oofem"): "QTrPlStr",
                      ("C3D4", "abaqus"): "C3D4",
                      ("C3D4", "oofem"): "LTRSpace",
                      ("C3D10", "abaqus"): "C3D10",
                      ("C3D10", "oofem"): "QTRSpace",
                      ("COH3D6", "abaqus"): "COH3D6",
                      ("COH3D6", "oofem"): "IntElSurfTr1",
                      ("COH3D12", "abaqus"): "COH3D12",
                      ("COH3D12", "oofem"): "UNKNOWN_OOFEM_NAME",
                      ("STRI65", "abaqus"): "STRI65",
                      ("STRI65", "oofem"): "tr2shell7",
                      ("CPS4R", "abaqus"): "CPS4R",
                      ("CPS4R", "oofem"): "tr2shell7",
                      ("C3D8", "abaqus"): "C3D8",
                      ("COH3D8", "abaqus"): "COH3D8",
                      ("COH2D4", "abaqus"): "COH2D4",
                      ("COH2D4", "oofem"): "intelline1",
                      ("COH2D6", "abaqus"): "COH2D6",
                      ("COH2D6", "oofem"): "intelline2",
                      ("S4R", "abaqus"): "S4R",
                      ("COH3D12", "oofem"): "IntElSurfTr2"}


# Translates between (external_name, software) to internal_name.
element_dictionary_inverse = {("T3D2", "abaqus"): "T3D2",
                              ("intelline1B", "oofem"): "T3D2",
                              ("T3D4", "abaqus"): "T3D4",
                              ("intelline2", "oofem"): "T3D4",
                              ("CPE3", "abaqus"): "CPE3",
                              ("TrPlaneStress2d", "oofem"): "CPE3",
                              ("CPE6", "abaqus"): "CPE6",
                              ("CPE4", "abaqus"): "CPE4",
                              ("QTrPlStr", "oofem"): "CPE6",
                              ("C3D4", "abaqus"): "C3D4",
                              ("LTRSpace", "oofem"): "C3D4",
                              ("C3D10", "abaqus"): "C3D10",
                              ("QTRSpace", "oofem"): "C3D10",
                              ("COH3D6", "abaqus"): "COH3D6",
                              ("IntElSurfTr1", "oofem"): "COH3D6",
                              ("STRI65", "abaqus"): "STRI65",
                              ("tr2shell7", "oofem"): "STRI65",
                              ("CPS4R", "abaqus"): "CPS4R",
                              ("tr2shell7", "oofem"): "CPS4R",
                              ("COH3D12", "abaqus"): "COH3D12",
                              ("C3D8", "abaqus"): "C3D8",
                              ("COH3D8", "abaqus"): "COH3D8",
                              ("COH2D4", "abaqus"): "COH2D4",
                              ("intelline1", "oofem"): "COH2D4",
                              ("COH2D6", "abaqus"): "COH2D6",
                              ("intelline2", "oofem"): "COH2D6",
                              ("S4R", "abaqus"): "S4R",
                              ("IntElSurfTr2", "oofem"): "COH3D12"}

# If different software have different node_order we need to override it in the export.
node_order_override = {("COH2D4", "abaqus"): [0, 1, 3, 2], ("CPE3", "abaqus"): [0, 2, 1]}

# Dimension of elements.
elements_1d = ["T3D2", "T3D4"]
elements_2d = ["CPE3", "STRI65", "CPS4R", "CPE6", "CPE4", "S4R", "COH2D4", "COH2D6"]
elements_3d = ["C3D4", "C3D10", "C3D10", "COH3D6", "COH3D12", "COH3D8"]
