from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements

inputfile = "../test/n10-id1.inp"
mesh = read_from_neper_inp(inputfile, verbose=0)
create_cohesive_elements(mesh)
export_to_abaqus("n10-id1_coh.inp", mesh, False)
