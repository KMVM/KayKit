# KayKit 26 - by Kieran Morley

# Module Import
import maya.cmds as cmds
import maya.OpenMaya as om

# Core Functions

def KayKitDefault():
    # Resets default prefixes when called after module import
    def SetPrefixDefaults():
        global RigPrefixDefaults
        RigPrefixDefaults = {"skin":"skin_", "rig":"rig_", "fk":"fk_", "ik":"ik_", "ctrl":"ctrl_", "grp":"grp_"} 
    SetPrefixDefaults()    

# Module Import Call

KayKitDefault()

# ________________________________________________________

# KayKit 26 - Tools

def KayHelp(commandname="", ):
    
    # Defines the print function used to display information to the user
    
    def KayHelpInfo(helpinfo_msg="", IsWarning=False):
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
    kayhelptj = "Given a target joint, generates a twist joint in the parent skeletal system that is autoweighted if a valid skincluster is attached to the joint system, before inserting a duplicate into a matching rig or skin joint hierarchy as needed."
    kayhelpsp = "Sets a default prefix KayKit uses to identify types of systems. \nVariables:\n - Prefix (valid string inputs: skin, rig, fk, ik, ctrl, grp)\n - Replace (new prefix string to use, including _)"
    kayhelpdss = "Defines a skeletal system from a joint named root with a matching prefix. This returns a list that can be used to make changes to the system. \nVariables:\n - Type (valid string inputs: skin, rig)"
    
    # Defines dictionary of help hints
    kayhelpdoc = {"ReturnSelection":kayhelprs, "BindRigToSkin":kayhelpbrs, "TwistJoint": kayhelptj, "SetPrefix":kayhelpsp, "DefineSkeletalSystem":kayhelpdss} # Each valid command name should be assigned a hint text variable as its key pair
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


# ________________________________________________________
 
def SetPrefix(Prefix="", Replace=""):
    if Prefix == "":
        KayHelp("SetPrefix")  
    elif Replace == "":
        KayHelp("SetPrefix")       
    else:
        global RigPrefixDefaults
        if RigPrefixDefaults.get(Prefix) != None:
            RigPrefixDefaults[Prefix] = Replace
        else:
            om.MGlobal.displayError("Prefix reassignment failed, incorrect prefix type or replace data type?")   
               
# ________________________________________________________   
                    
def ReturnSelection(SpecificType="None", ComplexHierarchy=False):
    
# Gets relatives from a selected object and removes all shape nodes.

    def IgnoreShapeRelatives(Relatives):
        
        FoundShapes = []
        
        if Relatives:
            for item in Relatives:
                if cmds.nodeType(item) != "transform":
                    FoundShapes = FoundShapes + [item]
                    
            for item in FoundShapes:
                Relatives.remove(item)
                
        return(FoundShapes)       

    if SpecificType == "None":
        Selection = cmds.ls(sl=True)
        Relatives = cmds.listRelatives(Selection[0], ad=True)   
        Relatives.reverse()            
            
    else:
        Selection = cmds.ls(sl=True, type=SpecificType)
        
        Relatives = cmds.listRelatives(Selection[0], ad=True)
        for elem in Relatives:
            elemtype = cmds.objectType(elem)
            if elemtype != SpecificType:
                Relatives.remove(elem)
                
    IgnoreShapeRelatives(Relatives)             

    # Returns list based on complex hierarchy argument        
    if ComplexHierarchy == True:
        if len(Selection) > 1:
            om.MGlobal.displayWarning(f"Discarded multiple selections, '{Selection[0]}' is now the parent of returned hierarchy.")
        Selection = Selection[:1] # Currently will only get the first selection's hierarchy in complex hierarchy mode
        return(Selection + Relatives)
    else:
        return(Selection)          
        
# ________________________________________________________ 

def DefineSkeletalSystem(Type="None"):
    
    # No User Input
    
    if Type == "None":
        KayHelp("DefineSkeletalSystem")
        return
        
    # User Selected Type To Define    
    
    sk_skinsystem = []
    sk_rigsystem = []
    
    if Type == "skin":
        root = cmds.ls(n=f"{SkinPrefix}_root")[0]
        sk_skinsystem = [root] + cmds.listRelatives(type="joint", ad=True)
    
    elif Type == "rig":
        root = cmds.ls(n=f"{RigPrefix}_root")[0]
        sk_rigsystem = [root] + cmds.listRelatives(type="joint", ad=True)
          
    else:
        om.MGlobalDisplayError("Invalid type of skeletal system specified for definition. Valid types: 'skin', 'rig'")
    
    return()            

# ________________________________________________________

def BindRigToSkin(InputSkinSystem="None", SkinPrefix="skin_", RigPrefix = "rig_"):
    
    def GetSkinSystem():
        
        SelectedJoints = cmds.ls(sl=True, type="joint")
        if SelectedJoints:
            Relatives = cmds.listRelatives(SelectedJoints[0], ad=True)
            return(Relatives + SelectedJoints)
        else:
            return()    
        
    def CreateRigSystem(SkinSystem):
        
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
    
    if SkinSystem == False:
        print("No valid input")
    else:    
        CreateRigSystem(SkinSystem)

# ________________________________________________________
    
def TwistJoint():
    pass

# ________________________________________________________
        
# Development Only
if __name__ == "__main__":
    DefineSkeletalSystem()
    pass





  
