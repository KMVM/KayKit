# KayKit 26 - UI Module

import maya.cmds as cmds
import maya.OpenMaya as om
import kaykit26 as kaykit


# Function Definition    
        
def colour_control_ui(cc_window_name="Colour Control Window", *args):
    
    # Duplicate Window Handling
    if cmds.window(cc_window_name, exists=True):
        cmds.deleteUI(cc_window_name)
        
    # Window + Layouts
    cc_ui_window = cmds.window(cc_window_name, title="KayKit26 - Colour Control", width=460)
    cc_ui_main_layout = cmds.columnLayout(p=cc_ui_window) 
    
    # Show Window
    cmds.showWindow(cc_ui_window)

    
def bind_skin_to_rig_ui(bsr_window_name="Bind Skin Joints to Rig Joints Window"):
    
    # Duplicate Window Handling
    if cmds.window(bsr_window_name, exists=True):
        cmds.deleteUI(bsr_window_name)
        
    # Window + Layouts
    bsr_ui_window = cmds.window(bsr_window_name, title="KayKit26 - Bind Skin To Rig", width=360)
    bsr_ui_main_layout = cmds.columnLayout(adj=True, p=bsr_ui_window)
    
    # Controls
    
    bsr_ui_cusom_prefix = cmds.checkBoxGrp(l="Customise Prefixes", p=bsr_ui_main_layout)
    cmds.text("\nSkin Prefix to Search for / Rig Prefix To Create Joints With", p=bsr_ui_main_layout)  
    bsr_ui_prefix_skin = cmds.textFieldGrp(label="Skin Prefix", p=bsr_ui_main_layout)
    bsr_ui_prefix_rig = cmds.textFieldGrp(label="Rig Prefix", p=bsr_ui_main_layout)  
    
    # Show Window
    cmds.showWindow(bsr_ui_window)  
    
                     
def return_selection_ui(window_name="Return Selection Window", *args):
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    # UI Window and Layout
    rs_ui_window = cmds.window(window_name, title="KayKit26 - Return Selection", width=500)
    rs_ui_layout = cmds.columnLayout(adj=True, p=rs_ui_window)
    
    
    # UI Hierarchy Options
    cmds.text("\nHierarchy Options", p=rs_ui_layout)    
    rs_ui_descendents = cmds.checkBoxGrp(label="All Descendents", p=rs_ui_layout)
    rs_ui_hierarchy_depth = cmds.intFieldGrp(label="Hierarchy Max Depth", p=rs_ui_layout, sbm="Limits the depth searched to when returning relatives from selected objects.")
    
    # UI Filter Options
    cmds.text("\nFilter Options", p=rs_ui_layout)
    rs_ui_type = cmds.textFieldGrp(label="Specific Type Filter", p=rs_ui_layout)
    rs_ui_phrase = cmds.textFieldGrp(label="Includes Phrase Only Filter", p=rs_ui_layout)
        
    # UI Debug Options
    cmds.text("\nMisc Options", p=rs_ui_layout)
    rs_ui_print = cmds.checkBoxGrp(label="Print Return List to Console", p=rs_ui_layout)
    cmds.text("\n", p=rs_ui_layout)
    
    # UI Confirm Button
    rs_ui_confirm = cmds.button(label="Return Selection")
    
    cmds.showWindow(rs_ui_window)


def weaver_ui(window_name="Weaver Window", *args):
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)   

    # UI Window and Layout
    wvr_ui_window = cmds.window(window_name, title="KayKit26 - Weaver", width=500)
    wvr_ui_main_layout = cmds.columnLayout(adj=True, p=wvr_ui_window)   
    wvr_ui_scroll_layout = cmds.scrollLayout(p=wvr_ui_main_layout, childResizable=True, margins4=(1, 2, 1, 2))
    wvr_ui_content_layout = cmds.columnLayout(adj=True, p=wvr_ui_scroll_layout)  
    
    # Controls
    #wvr_ui_inverse = cmds.checkBoxGrp(label="Weave Inverted.", p=wvr_ui_content_layout)
    #cmds.text("Will weave or unweave in an inverted fashion.\n")
    wvr_ui_builder_button = cmds.button(label="Weave Hierarchy", p=wvr_ui_content_layout, command=kaykit.weaver)
    cmds.text("Given a selection of unrelated objects, will arrange them in a standard hierarchy.\n")
    wvr_ui_demolition_button = cmds.button(label="Unweave Hierarchy", p=wvr_ui_content_layout)
    cmds.text("Remove all selected objects from a hierarchy.\n")

    
    # Show Window
    
    cmds.showWindow(wvr_ui_window)
    

def main_ui(window_name="Main Window"):
    
    # Duplicate Window Handling
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
        
    def placeholder_msg(*kwargs):
        om.MGlobal.displayInfo("KayKit26 Control Panel - Button does not function, work in progress.")  
    
    # Window + Layouts
    m_ui_window = cmds.window(window_name, title="KayKit26 - Control Panel", width=460)
    m_ui_main_layout = cmds.columnLayout(p=m_ui_window)
    m_ui_scroll_layout = cmds.scrollLayout(p=m_ui_main_layout, childResizable=True, margins4=(1, 2, 1, 2))
    m_ui_content_layout = cmds.columnLayout(adj=True, p=m_ui_scroll_layout)
    
    # Controls     
    
    #m_return_selection_button = cmds.button(label="Return Selection", p=m_ui_content_layout, command=return_selection_ui)
    #cmds.text("Returns a list of selected objects which can further be refined if desired.\n", p=m_ui_content_layout)
    
    m_colour_control_button = cmds.button(label="Colour Control", p=m_ui_content_layout, command=colour_control_ui)
    cmds.text("Modify controller drawing overrides.\n", p=m_ui_content_layout)  
    
    m_bind_skin_to_rig_button = cmds.button(label="Bind Skin to Rig Joints", p=m_ui_content_layout, command=bind_skin_to_rig_ui)
    cmds.text("Given a selection of skin joints, generate rig joints with constraints.\n", p=m_ui_content_layout)
    
    m_twist_joint_button = cmds.button(label="Twist Joints", p=m_ui_content_layout, command=placeholder_msg)
    cmds.text("Manage and generate various aspects of twist joint systems.\n", p=m_ui_content_layout)     
    
    m_weaver_button = cmds.button(label="Weaver", p=m_ui_content_layout, command=weaver_ui)
    cmds.text("Manipulate hierarchies in a range of ways.\n")
    
    m_manage_prefixes_button = cmds.button(label="Manage Prefixes", p=m_ui_content_layout, command=placeholder_msg) 
    cmds.text("View and modify prefixes in use.\n", p=m_ui_content_layout)
    
    m_kayhelp_button = cmds.button(label="Help Utility", p=m_ui_content_layout, command=placeholder_msg)
    cmds.text("Opens a help utility window for further documentation on KayKit commands.\n", p=m_ui_content_layout)     
    
    # Show Window
    cmds.showWindow(m_ui_window)
       
    
# Development Only    
if __name__ == "__main__":
    #return_selection_ui()
    main_ui()
