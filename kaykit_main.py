# KayKit 26 - by Kieran Morley

# Module Import
import maya.cmds as cmds
import maya.OpenMaya as om

# KHelp Tool

def KayHelp(commandname="", ):
    
    # Defines the print function used to display information to the user
    
    def KayHelpInfo(helpinfo_msg="A KayHelp function was called, please see the script editor output window for more information.", IsWarning=False):
        print("KayKit26")
        if IsWarning == False:
            om.MGlobal.displayInfo(helpinfo_msg)
        else:
            om.MGlobal.displayWarning(helpinfo_msg)    
        return()     
        
    # Defines a list of variables storing hint text
    kayhelpnull = f"'{commandname}' not recognised, did you forget to wrap in quotations or remove the module name?"
    kayhelpdefault = "To get help on a KayKit command, format = KayHelp('commandname')"
    kayhelprs = "Returns a list containing the selection.\nVariables:\n - SpecificType (optional, expects string containing type to filter to)\n - ComplexHierarchy (optional, expects True or False, ensures all descendents are returned"
    kayhelpbrs = "Given a selected joint, builds a list of all descendents then constructs a set of rig joints that constrain the joint hierarchy\nVariables:\n - SkinSystem (optional, a specified list of skin joints, default behaviour uses selected top level joint)"
    
    # Defines dictionary of help hints
    kayhelpdoc = {"ReturnSelection":kayhelprs, "BindRigToSkin":kayhelpbrs} # Each valid command name should be assigned a hint text variable as its key pair
    kayhelplist = kayhelpdoc.keys()
    kayhelpmsg = kayhelpdoc.get(commandname)
    kayhelpstring = ""

    # Determines if hint text should be returned

    if kayhelpmsg == None:
        kayhelpneeded = True     
    else:
        kayhelpneeded = False
        
    # Valid command as input  
      
    if kayhelpneeded == False:
        #print(f"{CommandName}: \n {kayhelpmsg}")
        KayHelpInfo(f"{commandname}: \n {kayhelpmsg}")
   
    else: # Invalid command as input  
        for entry in kayhelplist:
            entry = entry.replace(entry, f" - {entry}") 
            kayhelpstring = f"{kayhelpstring}\n {entry}" 
            
        if commandname == "":
            KayHelpInfo(kayhelpdefault + f"\nValid command names:{kayhelpstring}")
        else: 
            KayHelpInfo(kayhelpnull + f"\nValid command names:{kayhelpstring}", IsWarning=True)   

    return()
        

# KReturnSelection Tool

def ReturnSelection(SpecificType="None", ComplexHierarchy=False):
    if SpecificType == "None":
        Selection = cmds.ls(sl=True)
        Relatives = cmds.listRelatives(Selection[0], ad=True)
    else:
        Selection = cmds.ls(sl=True, type=SpecificType)
        Relatives = cmds.listRelatives(Selection[0], ad=True)
        for elem in Relatives:
            ElemType = cmds.objectType(elem)
            if ElemType == SpecificType:
                print(ElemType)
                pass
            else:
                Relatives.remove(elem)
                
    if ComplexHierarchy == True:
        return(Relatives + Selection)
    else:
        return(Selection)          


# Generate duplicate joint system from skin joints and build constraints

def BindRigToSkin(InputSkinSystem="None"):
    
    def GetSkinSystem():
        
        SelectedJoints = cmds.ls(sl=True, type="joint")
        if SelectedJoints:
            Relatives = cmds.listRelatives(SelectedJoints[0], ad=True)
            return(Relatives + SelectedJoints)
        
    def CreateRigSystem(SkinSystem):
        
        SkinPrefix = "skin_"
        RigPrefix = "rig_"
        
        DuplicateSkinSystem = cmds.duplicate(SkinSystem, st=True, rc=True)
        RigSystem = []
    
        # Gets the list of all skin joints and creates the new names to assign later
        for name in (SkinSystem):
            rig_name = name.replace(SkinPrefix, RigPrefix)
            RigSystem.append(rig_name)         
                                         
        # Renames the duplicated joints to the list of new desired names   
        for name in (DuplicateSkinSystem):
            rig_name = RigSystem[DuplicateSkinSystem.index(name)]
            cmds.rename(name, rig_name)
                                   
        # Sets up parent constraints between rig and skin joint systems
        for parentjoint in RigSystem:
            cmds.parentConstraint(parentjoint, SkinSystem[RigSystem.index(parentjoint)])
        
        # Clear the user selection    
        cmds.select(clear=True) 
    
    if InputSkinSystem == "None":
        SkinSystem = GetSkinSystem()
    else:
        SkinSystem = InputSkinSystem     
    
    CreateRigSystem(SkinSystem)
        
# Test Code
if __name__ == "__main__":
    pass



  
