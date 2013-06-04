import unittest

from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.read.read_from_neper_inp import to_number


class Test(unittest.TestCase):
    """Unit tests for read_from_neper_inp."""

    def setUp(self):
        self.mesh = read_from_neper_inp("n10-id1.inp")

    def test_read_from_neper_inp(self):
        """Test Phons reader for neper inp files."""

        # Test nodes
        self.assertEqual(len(self.mesh.nodes), 289)
        self.assertTrue(self.mesh.nodes[287].x - 0.91031946481 < 10E-9)
        self.assertTrue(self.mesh.nodes[1].y - 0.0 < 10E-9)
        self.assertTrue(self.mesh.nodes[289].z - 0.886838138103 < 10E-9)

        # Test 2d elements
        self.assertEqual(len(self.mesh.elements_2d), 684)
        self.assertTrue((self.mesh.elements_2d[1].elem_type == "CPE3") or
                        (self.mesh.elements_2d[1].elem_type == "CPE6"))
        self.assertEqual(self.mesh.elements_2d[5].vertices, [43, 39, 40])
        self.assertEqual(self.mesh.elements_2d[684].vertices, [38, 5, 52])

        # Test 3d elements
        self.assertEqual(len(self.mesh.elements_3d), 999)
        #print self.mesh.elements_3d
        self.assertTrue((self.mesh.elements_3d[686].elem_type == "C3D4") or
                        (self.mesh.elements_3d[686].elem_type == "C3D10"))
        self.assertEqual(self.mesh.elements_3d[685].vertices, [44, 155, 61, 154])
        self.assertEqual(self.mesh.elements_3d[1683].vertices, [283, 127, 246, 284])

        # Test 2d element sets
        self.assertEqual(len(self.mesh.element_sets_2d), 56)
        self.assertEqual(self.mesh.element_sets_2d["face22"].name, "face22")
        self.assertEqual(self.mesh.element_sets_2d["face36"].ids[3], 434)
                         
        # Test 3d element sets
        self.assertEqual(len(self.mesh.element_sets_3d), 10)
        self.assertEqual(self.mesh.element_sets_3d["poly6"].name, "poly6")
        self.assertEqual(self.mesh.element_sets_3d["poly10"].ids[8], 1584)

        # Test node sets
        self.assertEqual(len(self.mesh.node_sets), 44)
        self.assertEqual(len(self.mesh.node_sets["z0"].ids), 44)
        self.assertEqual(self.mesh.node_sets["x1z1body"].ids[1], 116)
        self.assertEqual(self.mesh.node_sets["x1y0z1"].getIds(), [32])               
        
    def test_to_number(self):
        self.assertEqual(to_number("1.3"), 1.3)
        self.assertEqual(to_number("1"), 1)

        

        

if __name__ == "__main__":
    unittest.main()
