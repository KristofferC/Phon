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

def export_to_abaqus(filename, trigs=False, f=None):
        write_no_end = False	
        if f == None:
            f = open(filename, 'w')
	else:
            write_no_end = True

        # Header
        f.write('*Part, name=' + self.name.upper() + "\n")


        # Nodes
        f.write('*Node\n')
        for node in mesh.nodes:
            f.write("%d, " % (node.id))
            f.write("%.12f, %.12f, %.12f\n" % (node.x, node.y, node.z))


        # Two dimensional elements
        if trigs:
            f.write("\n*Element, type=")
            if len(self.tris[0].vertices) == 3:
                f.write("CPE3\n")
            if len(self.tris[0].vertices) == 6:
                f.write("CPE6\n")
            for tri in self.tris:
                f.write("%d, " % format(tri.id))
                # Code below changes "[1,2,3]" to "1, 2, 3"
                f.write(''.join('{},'.format(k) for k in tri.vertices)[:-2])
                f.write('\n')

        # Three dimensional elements
        f.write("\n*Element, type=")
        if len(self.tetras[0].vertices) == 4:
            f.write("C3D4\n"),
        if len(self.tetras[0].vertices) == 10:
            f.write("C3D10\n")

        for tetra in self.tetras:
                f.write("{0}, ".format(tetra.id))
                # Code below changes "[1,2,3]" to "1, 2, 3"
                f.write(''.join('{}, '.format(k) for k in tetra.vertices)[:-2])
                f.write('\n')

        if not len(self.cohesiveElems) == 0:
            if len(self.cohesiveElems[0].vertices) == 6:
                f.write('*Element, type=COH3D6\n')
            if len(self.cohesiveElems[0].vertices) == 15:
                f.write('*Element, type=C3D15\n')
            for cohesive in self.cohesiveElems:
                    f.write("{0}, ".format(cohesive.id))
                    f.write(''.join('{}, '.format(k) for k in
                                            cohesive.vertices)[:-2])
                    f.write('\n')
        f.write('\n')

        for idx, cohset in enumerate(self.cohesiveSets):
            f.write("*Elset, elset=" + cohset.name.upper() + "\n")
            ids = cohset.getIds()
            for idx, i in enumerate(ids):
                if (idx + 1) % 15 == 0:
                    f.write('\n')
                if idx == (len(ids) - 1):
                    f.write(str(i) + "\n\n")
                else:
                    f.write(str(i) + ", ")
        f.write("\n")

        if trigs:
            for idx, faceset in enumerate(self.faceSets):
                f.write("*Elset, elset=" + faceset.name.upper() + "\n")
                ids = faceset.getIds()
                for idx, i in enumerate(ids):
                    if (idx + 1) % 15 == 0:
                        f.write('\n')
                    if idx == (len(ids) - 1):
                        f.write(str(i) + "\n\n")
                    else:
                        f.write(str(i) + ", ")
            f.write("\n")

        for idx, polyset in enumerate(self.polySets):
            f.write("*Elset, elset=" + polyset.name.upper() + "\n")
            ids = polyset.getIds()
            for idx, i in enumerate(ids):
                if (idx + 1) % 15 == 0:
                    f.write('\n')
                if idx == (len(ids) - 1):
                    f.write(str(i) + "\n\n")
                else:
                    f.write(str(i) + ", ")
        f.write("\n")

        for idx, nodeset in enumerate(self.nodeSets):
            f.write("*Nset, nset=" + nodeset.name.upper() + "\n")
            ids = nodeset.getIds()
            for idx, i in enumerate(ids):
                if (idx + 1) % 15 == 0:
                    f.write('\n')
                if idx == (len(ids) - 1):
                    f.write(str(i) + "\n\n")
                else:
                    f.write(str(i) + ", ")

        if not write_no_end:
            f.write("*End Part")
            f.close(
