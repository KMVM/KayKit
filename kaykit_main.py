# KayKit 26 - by Kieran Morley

# Module Import and Constants
import maya.cmds as cmds
import maya.OpenMaya as om

KAYKIT_VERSION = "KayKit26.indev.1607-01"

# Base Class Definition

# --------------------------------------------------------
class KayKitTool(object):
    
    CLASS_NAME = "KayKitTool"
    TOOL_HELPER_TEXT = {"helper":"Print help text for the user."}
    
    @classmethod
    def helper(*args, class_name="Null Class...", method="With No Method Specified", tool_helper_text="[!] Specify a method specific to the input class for more information."):
        print(f"{KAYKIT_VERSION}\n{class_name}\n{method}\n{tool_helper_text}")
                
# --------------------------------------------------------
def return_selection(type="", all_descendents=False, hierarchy_depth=512, prefer_phrase="", print_return=False):
    
    def phrase_filter(list_to_filter, preferred_phrase):
              
        # Error handling
        
        # Is list_to_filter a valid list?
        if isinstance(list_to_filter, list) == False:
            om.MGlobal.displayError(f"phrase_filter - A non-list object was input for the phrase_filter() nested function of return_selection(), which now returns an empty list. Object name: {list_to_filter}")
            return []
           
        # Is the list empty? 
        elif list_to_filter == []:
            om.MGlobal.displayError(f"phrase_filter - An empty list was used as input.")
            return []
        
        # Is the preferred phrase an invalid data type?    
        elif isinstance(preferred_phrase, str) == False:
            om.MGlobal.displayError("phrase_filter - List was returned with no modifications. Phrase filter only accepts string data type as input phrase.")
            return list_to_filter
        
        # Is the preferred phrase empty, and thus invalid?    
        elif preferred_phrase == "":
            print("phrase_filter - List was returned with no modifications. An empty string was specified as the preferred phrase.")
            return list_to_filter
        else:
            pass

        # Collects entries in the list with the specified filter phrase
        filtered_list = []
        
        for entry in list_to_filter:
            if preferred_phrase in entry:
                pass
            else:
                filtered_list.append(entry)
        
        # Return the filtered list                        
        return filtered_list
        
     
    # Function - return relatives from an input selection that are != to shapes  
    def get_relatives(selection):
        
        all_relatives = [] 
        all_shapes = []
        shapes_found = []
        
        # Error handling
        if isinstance(selection, list):
            pass
        elif type(selection, string):
            selection = [selection]
        else:
            om.MGlobal.displayError("get_relatives - Selection is not a valid list or string.")
            return []
            
        # Is selection populated? This check happens in main body but is repeated for validity
        if selection:
            # Obtaining relatives from selection
            for object in selection:
                relatives = []
                relatives = cmds.listRelatives(object, ad=True)[:hierarchy_depth]
                    
                direct_relatives = cmds.listRelatives(object, s=True) 
                for relative in direct_relatives:
                        all_shapes.append(relative)
                    
                if relatives:
                    for entry in relatives:
                        try:
                            shapes_found = shapes_found + cmds.listRelatives(entry, s=True)
                        except:
                            shapes_found = shapes_found
                            pass

                        all_relatives.append(entry)
                            
                    if shapes_found:
                       for entry in shapes_found:
                           all_shapes.append(entry)
                          
            
            # Compares the list of all_relatives to all names determined to belong to shapes and removes them                    
            for entry in all_shapes:
                if entry in all_relatives:
                    all_relatives.remove(entry)
         
        # Selection is empty, so return an empty list of relatives rather than try to get relatives from invalid objects       
        else:
            return [] 
        
        # Return list of relatives in reverse order
        all_relatives = all_relatives[::-1]
        return all_relatives   
            
    
    # Main Body - Determine list of selected objects to return to user/function

    final_selection = []
    
    # Type
    
    if type == "":
        selection = cmds.ls(sl=True)
    else:
        selection = cmds.ls(sl=True, type=type)    
    
    # Selection validity
     
    if selection:
        pass
    else: 
        return final_selection

    # Relatives

    if all_descendents:
        
        relatives = get_relatives(selection)
               
        if relatives:
            final_selection = selection + relatives   
            
        else:
            final_selection = selection
            
    else:
        final_selection = selection
        
    # Type filter (accounts for relatives)
    if type != "":
        for elem in final_selection:
            if cmds.objectType(elem) != type:
                final_selection.remove(elem)  
      
    # Phrase filter
    final_selection = phrase_filter(final_selection, prefer_phrase)        

    # Returns the final selection 
    if print_return:
        print(final_selection)
    return final_selection
    
# --------------------------------------------------------
class Prefixes(KayKitTool):
    
    #Helper Constants
    CLASS_NAME = "Prefixes"
    TOOL_HELPER_TEXT = {"set_prefix_defaults":"Reset prefixes to their default values.", "set_prefix":"Replace a prefix name. Arguments: prefix (string), replace (string)"}
    
    #Tool Constants
    RIG_PREFIX_DEFAULTS = {"skin": "skin_", "rig": "rig_", "fk": "fk_", "ik": "ik_", "ctrl": "ctrl_", "grp": "grp_"}

    #Methods
    @classmethod
    def set_prefix_defaults(*args):
        rig_prefixes = Prefixes.RIG_PREFIX_DEFAULTS
        
    @classmethod
    def set_prefix(*args, prefix="", replace=""):
        if prefix == "":
            KayKitTool.helper()
        elif replace == "":
            KayKitTool.helper()
        else:
            global rig_prefixes
            if rig_prefixes.get(prefix) != None:
                rig_prefixes[prefix] = replace
            else:
                om.MGlobal.displayError("Prefix reassignment failed, incorrect prefix type or replace data type?")
                
# -------------------------------------------------------- 
class ColourControl(KayKitTool):
    
    @classmethod
    def paint_joints():
        pass
    
    @classmethod
    def paint_controls():
        pass
    
    @classmethod    
    def auto_paint_joints(*args, skip_phrase_list=["skirt", "root"]):
    
        all_joints = cmds.ls(type="joint")
        
        if all_joints:
            for jnt in all_joints:
                contains_left = "left" in jnt
                contains_right = "right" in jnt
                skip = False
                
                if contains_left == False and contains_right == False:
                    continue
                 
                # Phrase Filter
                for phrase in skip_phrase_list:   
                    if phrase in jnt:
                        skip = True
                        break
                if skip == True:
                    continue 
                if contains_left:
                    cmds.color(jnt, ud=6)
                    continue
                if contains_right:
                    cmds.color(jnt, ud=1)
                    continue
                
# --------------------------------------------------------        
class Weaver(KayKitTool):
    
    @classmethod
    def weave(*args):
        selection = return_selection()
        
        if selection:
            if len(selection) <= 1:
                om.MGlobal.displayError("Selection too small, needs at least two objects selected to weave.")
                return
        else:
            om.MGlobal.displayError("Selection is empty, needs at least two objects selected to weave.")
                
        first_selection = selection[0]
        selection.pop(0)
    
        first = "None"
        last = "None"

        for entry in selection:
            if last == "None":
                last = entry
                first = last
            else:
                try:
                    cmds.parent(entry, last)
                    print(entry)
                    print(last)
                    
                except:
                    om.MGlobal.displayWarning("Unable to weave all selected objects into a hierarchy, aborting operation. This may be due to objects in a selection having relation to eachother.")
                    
                last = entry
                
                cmds.parent(first, first_selection)
                cmds.select(first_selection, r=True)     
        return
    
    @classmethod    
    def unweave(*args):
        
        selection = []
        selection = return_selection()
        
        # Check selection is populated
        if selection:
            pass
        else:
            om.Mglobal.displayError("Nothing to unweave, selection is empty.")
            return
          
        # Check for length of selection to determine behaviour    
        if len([selection]) > 1:
            pass
        else:
            if len(return_selection(all_descendents=True)) > 0:
                first_selection = selection
                selection = return_selection(all_descendents=True)

        if isinstance(selection, list):
                           
            for entry in selection:
                print(entry)
                cmds.parent(entry, w=True)
                
        cmds.select(first_selection, r=True)
            
        return
        
# --------------------------------------------------------  
def locator(replace=False):
    selection = return_selection()
    
    if selection:
        for object in selection:
            
            new_locator = cmds.spaceLocator(name=f"loc_{object}")
            cmds.matchTransform(new_locator, object)
        
            if replace == True:
                cmds.delete(object)
                
# --------------------------------------------------------  
def define_skeletal_system(type="None"):
    # No User Input

    if type == "None":
        kay_help("define_skeletal_system")
        return

    # User Selected Type To Define

    sk_skin_system = []
    sk_rig_system = []

    if type == "skin":
        root = cmds.ls(n=f"{skin_prefix}_root")[0]
        sk_skin_system = [root] + cmds.listrelatives(type="joint", ad=True)

    elif Type == "rig":
        root = cmds.ls(n=f"{rig_prefix}_root")[0]
        sk_rig_system = [root] + cmds.listrelatives(type="joint", ad=True)

    else:
        om.MGlobalDisplayError("Invalid type of skeletal system specified for definition. Valid types: 'skin', 'rig'")

    return
    
# --------------------------------------------------------  
def bind_skin_to_rig(input_skin_system="None", skin_prefix = rig_prefixes.get("skin"), rig_prefix = rig_prefixes.get("rig")):

    def get_skin_system():
        print("Here")
        joint_selection = return_selection(type="joint", all_descendents=True, print_return=True)
        if joint_selection == []:
            om.MGlobal.displayError("No joints selected")
            return []
        return joint_selection

    def create_rig_system(skin_system):
        if skin_system != True:
            om.MGlobal.displayError("No valid skin system selected, select a root joint for a skin system.")
            return()
        else:
            duplicate_skin_system = cmds.duplicate(skin_system, st=True, rc=True)
            print(duplicate_skin_system)
            rig_system = []

        # Generates a list of names for the rig system
        for name in (skin_system):
            rig_name = name.replace(skin_prefix, rig_prefix)
            rig_system.append(rig_name)

        # Renames the duplicated joints to the list of new desired names
        for name in (duplicate_skin_system):
            rig_name = rig_system[duplicate_skin_system.index(name)]
            print(rig_name)
            cmds.rename(name, rig_name)

        # Sets up parent constraints between rig and skin joint systems
        for parent_joint in rig_system:
            cmds.parentConstraint(parent_joint, skin_system[rig_system.index(parent_joint)])

        # Clear the user selection
        cmds.select(clear=True)

    if input_skin_system == "None":
        skin_system = get_skin_system()
    else:
        skin_system = input_skin_system

    if skin_system == False:
        print("No valid input")
    else:
        create_rig_system(skin_system)

# --------------------------------------------------------  
def twist_joint(end_joint="", start_joint="", auto_weight=True, no_propogation=False):
    if return_selection() == []:
        pass

    if end_joint == "":
        pass

    return_selection(type="joint")
    pass
    
# --------------------------------------------------------  

# Default
Prefixes.set_prefix_defaults()    

# Development Only
if __name__ == "__main__":
    pass
