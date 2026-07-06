# KayKit 26 - UI Module

import maya.cmds as cmds
import maya.OpenMaya as om
import kaykit26 as kaykit


# Function Definition    
        
def main_ui(window_name="Main Window"):
    
    # Duplicate Window Handling
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    # Window + Layouts
    m_ui_window = cmds.window(window_name, title="KayKit26 - Main Window", width=460)
    m_ui_main_layout = cmds.columnLayout(p=m_ui_window)
    m_ui_scroll_layout = cmds.scrollLayout(p=m_ui_main_layout, childResizable=True, margins4=(1, 2, 1, 2))
    m_ui_content_layout = cmds.columnLayout(adj=True, p=m_ui_scroll_layout)
    
    # Controls     
    
    #m_return_selection_button = cmds.button(label="Return Selection", p=m_ui_content_layout, command=return_selection_ui)
    #cmds.text("Returns a list of selected objects which can further be refined if desired.\n", p=m_ui_content_layout)
    
    m_colour_control_button = cmds.button(label="Colour Control", p=m_ui_content_layout)
    cmds.text("Modify controller drawing overrides.\n", p=m_ui_content_layout)  
    
    m_bind_skin_to_rig_button = cmds.button(label="Bind Skin to Rig Joints", p=m_ui_content_layout)
    cmds.text("Given a selection of skin joints, generate rig joints with constraints.\n", p=m_ui_content_layout)
    
    m_twist_joint_button = cmds.button(label="Twist Joints", p=m_ui_content_layout)
    cmds.text("Manage and generate various aspects of twist joint systems.\n", p=m_ui_content_layout)     
    
    m_manage_prefixes_button = cmds.button(label="Manage Prefixes", p=m_ui_content_layout) 
    cmds.text("View and modify prefixes in use.\n", p=m_ui_content_layout)
    
    m_kayhelp_button = cmds.button(label="Help Utility", p=m_ui_content_layout)
    cmds.text("Opens a help utility window for further documentation on KayKit commands.\n", p=m_ui_content_layout)     
    
    # Show Window
    cmds.showWindow(m_ui_window)
    
                           
def return_selection_ui(window_name="Return Selection Window"):
    
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
    
    # UI Window and Layout
    rs_ui_window = cmds.window(window_name, title="KayKit 26 - Return Selection", width=500)
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
    
    
# Development Only    
if __name__ == "__main__":
    #return_selection_ui()
    main_ui()
