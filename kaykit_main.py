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
        return ()

        # Defines a list of variables storing hint text

    kay_help_null = f"'{command_name}' not recognised, did you forget to wrap in quotations or remove the module name?"
    kay_help_default = "To get help on a KayKit command, format = kay_help('commandname')"
    kay_help_rs = "Returns a list containing the selection.\nArguments:\n - specific_type (optional, expects string containing type to filter to)\n - complex_hierarchy (optional, expects True or False, ensures all descendents are returned)\n - hierarchy_depth (optional, integer value for how many relatives to return.\n - print_return (optional, expects True or False, prints return of function to the script editor.\n - prefer_phrase (optional, will filter the initial selection to objects containing the phrase, not accounting for objects collected as descendents.)"
    kay_help_brs = "Given a selected joint, builds a list of all descendents then constructs a set of rig joints that constrain the joint hierarchy\nArguments:\n - skin_system (optional, a specified list of skin joints, default behaviour uses selected top level joint)"
    kay_help_tj = "Given a target joint, generates a twist joint in the parent skeletal system that is autoweighted if a valid skincluster is attached to the joint system, before inserting a duplicate into a matching rig or skin joint hierarchy as needed. \nArguments:\n - end_joint (required, when no start joint is specified the first parent joint is used instead.)\n - start_joint (If provided, will be the joint above the twist controller.)\n - auto_weight (Should an autoweight be attempted if a skin cluster is found? Defaults to False.)\n - no_propogation (Defaults to False, when enabled will ignore generating a matching rig or skin skeleton."
    kay_help_sp = "Sets a default prefix KayKit uses to identify types of systems. \nArguments:\n - prefix (valid string inputs: skin, rig, fk, ik, ctrl, grp)\n - replace (new prefix string to use, including _)"
    kay_help_dss = "Defines a skeletal system from a joint named root with a matching prefix. This returns a list that can be used to make changes to the system. \nArguments:\n - type (valid string inputs: skin, rig)"

    # Defines dictionary of help hints
    kay_help_doc = {"return_selection": kay_help_rs, "bind_rig_to_skin": kay_help_brs, "twist_joint": kay_help_tj,
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

    return ()


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


def return_selection(specific_type="None", complex_hierarchy=False, hierarchy_depth=512, print_return=False, prefer_phrase=""):
    
    # Removes non-transforms from an input list of relatives
    def ignore_shape_relatives(relatives):

        found_shapes = []

        if relatives:
            for item in relatives:
                if cmds.nodeType(item) != "transform":
                    found_shapes = found_shapes + [item]

            for item in found_shapes:
                relatives.remove(item)

        return (found_shapes)

        # Adds any objects listed in selection to the filtered selection list

    def phrase_filter(list_to_filter, preferred_phrase="phrase"):
        if preferred_phrase == "":
            return (list_to_filter)
        elif type(list_to_filter) != "list":
            raise Exception(f"A non-list object was input for the phrase_filter() nested function of Returnselection(). Object name: {list_to_filter}")

        filtered_list = []
        found_match = False

        for entry in list_to_filter:
            if preferred_phrase in entry:
                filtered_list.append(entry)
                found_match = True
            else:
                # Entry being tested does not match
                pass

        # If no names matched the filter keyword, returns the list without modification.
        if found_match == False:
            filtered_list = list_to_filter

        return (filtered_list)

        # Main Body

    final_selection = []

    if specific_type == "None":
        selection = cmds.ls(sl=True)

        if selection:
            relatives = cmds.listrelatives(selection[0], ad=True)
            relatives.reverse()
        else:
            return (final_selection)

    else:
        selection = cmds.ls(sl=True, type=specific_type)

        if selection:
            relatives = cmds.listrelatives(selection[0], ad=True)
        else:
            return (final_selection)

        for elem in relatives:
            elemtype = cmds.objectType(elem)
            if elemtype != specific_type:
                relatives.remove(elem)

    ignore_shape_relatives(relatives)

    # Returns list based on complex hierarchy argument
    if complex_hierarchy == True:
        if len(selection) > 1:
            om.MGlobal.displayWarning(
                f"Discarded multiple selections, '{selection[0]}' is now the parent of returned hierarchy.")
        selection = selection[:1]  # Currently will only get the first selection's hierarchy in complex hierarchy mode
        relatives = relatives[:hierarchy_depth]
        final_selection = selection + relatives

    else:
        final_selection = selection

    if print_return:
        print(final_selection)
    return (final_selection)


# ________________________________________________________

def define_skeletal_system(type="None"):
    # No User Input

    if type == "None":
        kay_help("define_skeletal_system")
        return()

    # User Selected Type To Define

    sk_skinsystem = []
    sk_rigsystem = []

    if type == "skin":
        root = cmds.ls(n=f"{skin_prefix}_root")[0]
        sk_skinsystem = [root] + cmds.listrelatives(type="joint", ad=True)

    elif Type == "rig":
        root = cmds.ls(n=f"{rig_prefix}_root")[0]
        sk_rigsystem = [root] + cmds.listrelatives(type="joint", ad=True)

    else:
        om.MGlobalDisplayError("Invalid type of skeletal system specified for definition. Valid types: 'skin', 'rig'")

    return ()


# ________________________________________________________

def bind_rig_to_skin(input_skin_system="None", skin_prefix="skin_", rig_prefix="rig_"):
    def get_skin_system():

        joint_selection = return_selection(specific_type="joint")

        # Returnselection could include handling for no output? Including a name filter is a good idea

        # Are any joints in the selection?
        if joint_selection:
            pass
        else:
            return ()

        # Searches the selected joints for a root joint, always preferring to make it the parent of all descendents
        if joint_selection.get("root") != None:
            joint_selection = joint_selection.get("root")
        else:
            joint_selection = [joint_selection[0]]

        joint_selection = "a"

        for jnt in selected_joints:
            pass

        return()

    if selected_joints.get(prefix) != None:
        rig_prefixes[prefix] = replace

        #
        # SelectedJoints = cmds.ls(sl=True, type="joint")
        # if SelectedJoints:
        #    relatives = cmds.listrelatives(SelectedJoints[0], ad=True)
        #    return(relatives + SelectedJoints)
        # else:
        #    return([])

    def create_rig_system(skin_system):
        if skin_system != True:
            om.MGlobal.displayError("No valid skin system selected, select a root joint for a skin system.")
            return ()
        else:
            duplicate_skin_system = cmds.duplicate(skin_system, st=True, rc=True)
            rig_system = []

        # Generates a list of names for the rig system
        for name in (skin_system):
            rig_name = name.replace(skin_prefix, rig_prefix)
            rig_system.append(rig_name)

            # Renames the duplicated joints to the list of new desired names
        for name in (duplicate_skin_system):
            rig_name = rig_system[duplicate_skin_system.index(name)]
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

def twist_joint(end_joint, start_joint="", auto_weight=True, no_propogation=False):
    # cmds.ls(sl=True, type="joint")
    pass


# ________________________________________________________

# Development Only
if __name__ == "__main__":
    pass
