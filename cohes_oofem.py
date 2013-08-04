from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_oofem import export_to_oofem
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements



mesh = read_from_neper_inp("n2-id1.inp", verbose=0)
create_cohesive_elements(mesh)
mesh.renumber_nodes()
export_to_oofem("n2-id1_coh_2.inp", mesh, False)
