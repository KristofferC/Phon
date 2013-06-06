element_dictionary =  {("CPE3", "abaqus") : "CPE3",
                       ("CPE3", "oofem") : "TrplaneStrain",
                       ("C3D4", "abaqus") : "C3D4",
                       ("C3D4", "oofem") : "LTRSpace"}

element_dictionary_inverse  =  {("CPE3", "abaqus") : "CPE3",
                                ("TrplaneStrain", "oofem") : "CPE3",
                                ("C3D4", "abaqus") : "C3D4",
                                ("LTRSpace", "oofem") : "C3D4"}
        

elements_2d = ["CPE3"]
elements_3d = ["C3D4"]