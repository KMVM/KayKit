# KayKit 26 - by Kieran Morley

# ________________________________________________________

# Module Import
import maya.cmds as cmds
import maya.OpenMaya as om


# Define Module Default Functions

def kaykit_default():
    def set_prefix_defaults():
        RIG_PREFIX_DEFAULTS = {"skin": "skin_", "rig": "rig_", "fk": "fk_", "ik": "ik_", "ctrl": "ctrl_", "grp": "grp_"}
        global rig_prefixes
        rig_prefixes = RIG_PREFIX_DEFAULTS 
         
    # Set module defaults       
    set_prefix_defaults()

# KayKit defaults, currently can also be used to reset the defaults and will run on each import.

kaykit_default()


# ________________________________________________________

def kay_help(command_name=""):
    # Defines the print function used to display information to the user

    def kay_help_info(help_info_msg="", is_warning=False):
        print("KayKit26")
        if is_warning == False:
            om.MGlobal.displayInfo(help_info_msg)
        else:
            om.MGlobal.displayWarning(help_info_msg)
        return

        # Defines a list of variables storing hint text

    kay_help_null = f"'{command_name}' not recognised, did you forget to wrap in quotations or remove the module name?"
    kay_help_default = "To get help on a KayKit command, format = kay_help('commandname')"
    kay_help_rs = "Returns a list containing the selection.\nArguments:\n - type (optional, expects string containing type to filter to)\n - all_descendents (optional, expects True or False, ensures all descendents are returned)\n - hierarchy_depth (optional, integer value for how many relatives to return.\n - print_return (optional, expects True or False, prints return of function to the script editor.\n - prefer_phrase (optional, will filter the initial selection to objects containing the phrase, not accounting for objects collected as descendents.)"
    kay_help_bsr = "Given a selected joint, builds a list of all descendents then constructs a set of rig joints that constrain the joint hierarchy\nArguments:\n - skin_system (optional, a specified list of skin joints, default behaviour uses selected top level joint)"
    kay_help_tj = "Given a target joint, generates a twist joint in the parent skeletal system that is autoweighted if a valid skincluster is attached to the joint system, before inserting a duplicate into a matching rig or skin joint hierarchy as needed. \nArguments:\n - end_joint (required, when no start joint is specified the first parent joint is used instead.)\n - start_joint (If provided, will be the joint above the twist controller.)\n - auto_weight (Should an autoweight be attempted if a skin cluster is found? Defaults to False.)\n - no_propogation (Defaults to False, when enabled will ignore generating a matching rig or skin skeleton."
    kay_help_sp = "Sets a default prefix KayKit uses to identify types of systems. \nArguments:\n - prefix (valid string inputs: skin, rig, fk, ik, ctrl, grp)\n - replace (new prefix string to use, including _)"
    kay_help_dss = "Defines a skeletal system from a joint named root with a matching prefix. This returns a list that can be used to make changes to the system. \nArguments:\n - type (valid string inputs: skin, rig)"

    # Defines dictionary of help hints
    kay_help_doc = {"return_selection": kay_help_rs, "bind_skin_to_rig": kay_help_bsr, "twist_joint": kay_help_tj,
                  "set_prefix": kay_help_sp,
                  "define_skeletal_system": kay_help_dss}  # Each valid command name should be assigned a hint text variable as its key pair
    kay_help_list = kay_help_doc.keys()
    kay_help_msg = kay_help_doc.get(command_name)
    kay_help_string = ""

    # Determines if hint text should be returned

    if kay_help_msg == None:
        kay_help_needed = True
    else:
        kay_help_needed = False

    # Valid command as input

    if kay_help_needed == False:
        # print(f"{CommandName}: \n {kayhelpmsg}")
        kay_help_info(f"{command_name}: \n {kay_help_msg}")

    else:  # Invalid command as input
        for entry in kay_help_list:
            entry = entry.replace(entry, f" - {entry}")
            kay_help_string = f"{kay_help_string}\n {entry}"

        if command_name == "":
            kay_help_info(kay_help_default + f"\nValid command names:{kay_help_string}")
        else:
            kay_help_info(kay_help_null + f"\nValid command names:{kay_help_string}", is_warning=True)

    return


# ________________________________________________________

def set_prefix(prefix="", replace=""):
    if prefix == "":
        kay_help("set_prefix")
    elif replace == "":
        kay_help("set_prefix")
    else:
        global rig_prefixes
        if rig_prefixes.get(prefix) != None:
            rig_prefixes[prefix] = replace
        else:
            om.MGlobal.displayError("Prefix reassignment failed, incorrect prefix type or replace data type?")

# ________________________________________________________

def return_selection(type="", all_descendents=False, hierarchy_depth=512, prefer_phrase="", print_return=False):
    
    # Add a flag to just return shape nodes so that locator command can set the scale of the entry by calling return_selection()

    def phrase_filter(list_to_filter, preferred_phrase):
        
        filtered_list = []
        found_match = False
                
        # Error handling
        if isinstance(list_to_filter, list) == False:
            om.MGlobal.displayError(f"phrase_filter - A non-list object was input for the phrase_filter() nested function of return_selection(), which now returns an empty list. Object name: {list_to_filter}")
            return []
        elif isinstance(preferred_phrase, str) == False:
            om.MGlobal.displayError("phrase_filter - List was returned with no modifications. Phrase filter only accepts string data type as input phrase.")
            return list_to_filter
        elif preferred_phrase == "":
            #om.MGlobal.displayWarning("phrase_filter - List was returned with no modifications. An empty string was specified as the preferred phrase.")
            return list_to_filter
        else:
            pass

        # Collects entries in the list with the specified filter phrase
        for entry in list_to_filter:
            if preferred_phrase in entry:
                pass
            else:
                filtered_list.append(entry)
                                
        return filtered_list # with keyword filtered entries removed
        
     
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
                try:
                    relatives = cmds.listRelatives(object, ad=True)[:hierarchy_depth] #+ cmds.listRelatives(object, s=True)
                except:
                    pass
                
                if relatives == []:    
                    return []
                    
                
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
        
        all_relatives = all_relatives[::-1]
        return all_relatives   
            
    
    # Main Body - Determine list of selected objects to return to user/function

    final_selection = []
    
    # Handles "type=" argument
    
    if type == "":
        selection = cmds.ls(sl=True)
    else:
        selection = cmds.ls(sl=True, type=type)    
    
    # Checks if selection is valid
     
    if selection:
        pass
    else: 
        return final_selection

    # Handles relative retrieval

    if all_descendents:
        
        relatives = get_relatives(selection)
               
        if relatives:
            final_selection = selection + relatives   
            
        else:
            final_selection = selection   
            
    else:
        final_selection = selection
        
    # Type filter
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
    

def control_colour_utility():
    pass
    

# ________________________________________________________

def weaver(*args, function="weave"):
    
    def weave():
        
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
            except:
                om.MGlobal.displayWarning("Unable to weave all selected objects into a hierarchy, aborting operation. This may be due to objects in a selection having relation to eachother.")
                
            last = entry
            
            cmds.parent(first, first_selection)
            cmds.select(first_selection, r=True)
             
    def unweave():
        
        selection = []
        selection = return_selection
        
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
                selection = return_selection(all_descendents=True)
        
        
        #selection = sorted(selection, reverse=True)
        
        print(selection)
        
        if isinstance(selection, list):
                           
            for entry in selection:
                print(entry)
                cmds.parent(entry, w=True)
            
        return

        
    if function == "weave":
        weave()
    elif function == "unweave":
        unweave()
    else:
        om.MGlobal.displayWarning(f"Weaver did not act as an invalid function, '{function}', was specified - Valid function name examples: 'weave', 'unweave'.")
        return
                
# ________________________________________________________
       
def locator(replace=False):
    selection = return_selection()
    
    if selection:
        for object in selection:
            
            new_locator = cmds.spaceLocator(name=f"loc_{object}")
            cmds.matchTransform(new_locator, object)
        
            if replace == True:
                cmds.delete(object)
    
# ________________________________________________________    

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


# ________________________________________________________

def bind_skin_to_rig(input_skin_system="None", skin_prefix = rig_prefixes.get("skin"), rig_prefix = rig_prefixes.get("rig")):

    def get_skin_system():

        joint_selection = return_selection(type="joint", all_descendents=True, print_return=True)

        if joint_selection == []:
            om.MGlobal.displayError("No joints selected")
            return

        # Searches the selected joints for a root joint, always preferring to make it the parent of all descendents
        #if joint_selection.get("root") != None:
            #joint_selection = joint_selection.get("root")
       # else:
           # joint_selection = [joint_selection[0]]

       # joint_selection = "a"

        #for jnt in selected_joints:
            #pass

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


# ________________________________________________________

#def twist_joint(end_joint="", start_joint="", auto_weight=True, no_propogation=False):
    if return_selection() == []:
        print("a")
        
    
    if end_joint == "":
        om.m
        return

    return_selection(type="joint")
    
    # cmds.ls(sl=True, type="joint")
    pass


# ________________________________________________________

# Development Only
if __name__ == "__main__":
    pass
