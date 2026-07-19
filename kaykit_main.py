# KayKit 26 - by Kieran Morley

KAYKIT_VERSION = "KayKit26.indev.1907-01"

import maya.cmds as cmds
import maya.OpenMaya as om

# Base Class Definition

# --------------------------------------------------------
class KayKitTool(object):
    
    HELPER_TEXT = {"helper":"Prints help text for the user. Call from a child class to view information about its uses and methods."}
    
    @classmethod
    def helper(self, method=""):
        # Has the user included a method to query instead of the class? And is that a valid method that belongs to the class?
        specific_method = False
        if method:
            method_text = self.HELPER_TEXT.get(method)
            if method_text:
                specific_method = True
        
        # If the user is querying a method to a class, print information about that method. Otherwise print all available methods to the class instead.        
        if specific_method == True:
            print(f"Class Name: {self.__name__}\nMethod Name: {method}\nDescription: {method_text}\n\nTo view all methods available to this class, call helper function with no arguments.")
            
        else:
            available_methods = "" 
            for entry in self.HELPER_TEXT:
                available_methods = available_methods + f"\n - {entry}"
            print(f"Class Name: {self.__name__}\nAvailable Methods:{available_methods}\n\nFor more details on an available method to this class, pass as a string to helper function.")
                 
# --------------------------------------------------------

# Available classes/methods

# --------------------------------------------------------
class Prefixes(KayKitTool):
    # Constants
    HELPER_TEXT = {"set_prefix_defaults":"Reset prefixes to their default values.", "set_prefix":"Replace a prefix name.\nArguments:\n - prefix (required, string to use as replacement.)\n - replace (required, " \
    "string of prefix type to replace.)"}
    
    RIG_PREFIX_DEFAULTS = {"skin":"skin_", "rig":"rig_", "fk":"fk_", "ik":"ik_", "ctrl":"ctrl_", "grp":"grp_", "locator":"loc_"}
    # Vars
    rig_prefixes = RIG_PREFIX_DEFAULTS

    @classmethod
    def set_prefix_defaults(*args):
        Prefixes.rig_prefixes = Prefixes.RIG_PREFIX_DEFAULTS
        
    @classmethod
    def set_prefix(self, prefix="", replace=""):
        print(f"{self}, {prefix}, {replace}")
        if prefix == "":
            print("Prefix replacement string is invalid.")
            Prefixes.helper("set_prefix")
        elif replace == "":
            print("Replace not recognised, valid types: skin, rig, fk, ik, ctrl, grp, locator")
            Prefixes.helper("set_prefix")
        else:
            if Prefixes.rig_prefixes.get(replace) != None:
                Prefixes.rig_prefixes[replace] = prefix
            else:
                om.MGlobal.displayError("Prefix reassignment failed, incorrect prefix type or replace data type?")
                
Prefixes.set_prefix_defaults()
                
# --------------------------------------------------------
class SelectUtility(KayKitTool):
    
    HELPER_TEXT = {"return_selection":"Returns a list containing the selection.\nArguments:\n - type (optional, expects string containing type to filter to)\n - all_descendents " \
    "(optional, expects True or False, ensures all descendents are returned)\n - hierarchy_depth (optional, integer value for how many relatives to return.\n - print_return (optional, " \
    "expects True or False, prints return of function to the script editor.\n - prefer_phrase (optional, will filter the initial selection to objects containing the phrase, not accounting " \
    "for objects collected as descendents.)", "phrase_filter":"Given a list, filters entries out that do not contain a given phrase.\nArguments:\n - list_to_filter (required, the list to filter for.)" \
    "\n - preferred_phrase (required, the phrase that entries must include.)", "get_relatives":"Get a list of relatives from a selection.\nArguments:\n - selection (required, list of selected objects " \
    "to search through."}
    
    @classmethod
    def phrase_filter(self, list_to_filter, preferred_phrase):
        
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
                filtered_list.append(entry)
            else:
                pass
        
        # Return the filtered list                        
        return filtered_list
    
    @classmethod
    def get_relatives(self, selection, hierarchy_depth):
        
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
                if direct_relatives:
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
        
    @classmethod
    def return_selection(self, type="", all_descendents=False, hierarchy_depth=512, preferred_phrase="", print_return=False):
        
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
            
            relatives = SelectUtility.get_relatives(selection, hierarchy_depth)
                   
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
        final_selection = SelectUtility.phrase_filter(final_selection, preferred_phrase)        
    
        # Returns the final selection 
        if print_return:
            print(final_selection)
        return final_selection

# --------------------------------------------------------
class ColourControl(KayKitTool):
    
    HELPER_TEXT = {"paint_joints":"Can recolour joints given an index and a specific selection.", "paint_controls":"Can recolour controls given an index and a specific " \
    "selection.", "auto_paint_joints":"Automatically recolour joints by sidedness.\nArguments:\n - skip_phrase_list (optional, a list object containing all phrases that qualify a joint for skipping the auto paint process"}
    
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
    
    HELPER_TEXT = {"weave":"Weaves the selected objects into a standard hierarchy.", "unweave":"All selected objects are reparented to the scene world, removing them from any hierarchy."}
    
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
class Locator(KayKitTool):
    
    HELPER_TEXT = {"place_locator":"Given a selection, places a locator at each selection.\nArguments:\n - replace (optional, default=False, a boolean that determines if " \
                  "the selected objects are deleted when a locator is placed."}

    def place_locator(replace=False):
        selection = SelectUtility.return_selection()
        
        if selection:
            for object in selection:
                
                new_locator = cmds.spaceLocator(name=f"{Prefixes.rig_prefixes.get('locator')}{object}")
                cmds.matchTransform(new_locator, object)
            
                if replace == True:
                    cmds.delete(object)
                
# --------------------------------------------------------
class Bind(KayKitTool):
    
    HELPER_TEXT = {"get_skin_system":"Return a list of all joints that have the skin prefix and are joint type, including all descendents.", "build_rig_system":"Given a list " \
                  "of skin joints, constructs and binds a rig system to match.", "skin_to_rig":"Combines two methods to act as a convenient way to build a rig system layer."}

    @classmethod    
    def get_skin_system(self):
        joint_selection = SelectUtility.return_selection(type="joint", all_descendents=True, preferred_phrase=rig_prefixes.get("skin"))
        
        if joint_selection == []:
            om.MGlobal.displayError("No joints selected")
            return []
            
        return joint_selection
        
    @classmethod    
    def build_rig_system(self, skin_system):
        rig_system = []
        
        if skin_system == "None":
            om.MGlobal.displayError("No valid skin system selected, select a root joint for a skin system.")
            return()
        else:
            duplicate_skin_system = cmds.duplicate(skin_system, st=True, rc=True)
            rig_system = []

        # Generates a list of names for the rig system
        for name in (skin_system):
            rig_name = name.replace(Prefixes.rig_prefixes["skin"], Prefixes.rig_prefixes["rig"])
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
        pass
        
    @classmethod
    def skin_to_rig(self, input_skin_system="None", skin_prefix=Prefixes.rig_prefixes.get("skin"), rig_prefix=rig_prefixes.get("rig")):
        if input_skin_system == "None":
            skin_system = Bind.get_skin_system()
        else:
            skin_system = input_skin_system
    
        if skin_system == False:
            print("No valid input")
        else:
            Bind.build_rig_system(skin_system)
        
# --------------------------------------------------------
class Twister(KayKitTool):
    
    HELPER_TEXT = {"insert_joint":"Work in progress."}
    
    def insert_joint(end_joint="", start_joint="", auto_weight=True, no_propogation=False):
        if SelectUtility.return_selection() == ():
            pass
        if end_joint == "":
            pass
            
        SelectUtility.return_selection(type="joint")
        pass
    
# --------------------------------------------------------  

# Development Only
if __name__ == "__main__":
    pass
    
