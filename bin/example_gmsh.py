import argparse
import ntpath

from phon.io_tools.read.read_from_gmsh import read_from_gmsh
from phon.io_tools.write.export_to_oofem import export_to_oofem
from phon.io_tools.write.export_to_abaqus import export_to_abaqus
from phon.mesh_tools.create_cohesive_elements import create_cohesive_elements

parser = argparse.ArgumentParser(description="Imports gmsh .msh files to a mesh, "
                                             "creates cohesive elements "
                                             "and exports it to either OOFEM or Abaqus. Mesh files "
                                             "should each have one .msh file per grain with  the name "
                                             "'meshfileX.msh' where X is the grain id.")


requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument("-b", "--basefilename", help="The basename of the files, that is everything before the "
                                                        "grain id and the file extension.", required=True)

requiredNamed.add_argument("-n", "--n_grains", help="The number of total grains, you should have "
                                                    "one .msh file for each grain.", required=True, type=int)

requiredNamed.add_argument('-o', '--output', choices=["abaqus", "oofem"], help='Software to export the mesh to.',
                           required=True)

parser.add_argument("-s", '--scale', help="Scale to scale all the nodes with.", type=float)
parser.add_argument('-v', '--verbose', action='count', help="Level of verbosity, -v for level 1, -vv for level 2 etc.",
                    default=0)

args = parser.parse_args()

mesh = read_from_gmsh(args.basefilename, args.n_grains, args.verbose)

create_cohesive_elements(mesh, mesh_dimension=3)

# Rescale the RVE:
if args.scale:
    for node_id, node in mesh.nodes.items():
        node.c *= args.scale

print("Exporting to " + args.output + "...")
if args.output == "abaqus":
    export_to_abaqus(ntpath.basename(args.basefilename) + "_coh.inp", mesh, write_2d_elements=False)
if args.output == "oofem":
    export_to_oofem(ntpath.basename(args.basefilename) + "_coh.in", mesh, write_2d_elements=False)

print("Done!")