from phon.io.read.read_from_neper_inp import read_from_neper_inp
from phon.io.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements

inputfile = "../test/inp_test_files/n10-id1.inp"
mesh = read_from_neper_inp(inputfile, verbose=0)
create_cohesive_elements(mesh, 3)
export_to_abaqus("n10-id1_coh.inp", mesh, write_2d_elements=False)
