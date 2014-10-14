import sys
from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_oofem import export_to_oofem
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements


inputfile = sys.argv[1]
scale = float(sys.argv[2])

mesh = read_from_neper_inp("test/n10-id1.inp", verbose=0)
create_cohesive_elements(mesh)
mesh.renumber_nodes()

# Rescale the RVE:
for node_id, node in mesh.nodes.iteritems():
    node.x *= scale
    node.y *= scale
    node.z *= scale

export_to_oofem("n10-id1_coh.in", mesh, False)
export_to_abaqus("n10-id1_coh.inp", mesh, False)
