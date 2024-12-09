
import bpy

PANEL_NAME = "DIVA"

class SCENE_PT_Setup(bpy.types.Panel):
    bl_label = "Scene Setup"
    bl_idname = "SCENE_PT_setup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_NAME

    def draw(self, context):
        layout = self.layout
        layout.label(text="Motion Set:")

        # Import Button / Placeholder for now
        col = layout.column()
        col.enabled = False
        col.operator("import_motion.bin", text="Import", icon='IMPORT')

        # Export Button
        layout.operator("export_motion.bin", text="Export", icon='EXPORT')

class ARMATURE_PT_Panel(bpy.types.Panel):
    bl_label = "Armature Motion Setup"
    bl_idname = "ARMATURE_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_NAME

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.operator("armature.detect_objects", text="Auto-Detect Objects", icon='VIEWZOOM')
        layout.prop(scene, "armature_object", text="Armature")

        col = layout.column(align=True)
        split = col.split(factor=0.5)

        left_col = split.column(align=True)
        left_col.label(text="Left Side")
        left_col.prop(scene, "left_arm_bone", text="Arm")
        left_col.prop(scene, "left_elbow_bone", text="Elbow")
        left_col.prop(scene, "left_wrist_bone", text="Wrist")
        left_col.prop(scene, "left_foot_bone", text="Foot")

        right_col = split.column(align=True)
        right_col.label(text="Right Side")
        right_col.prop(scene, "right_arm_bone", text="Arm")
        right_col.prop(scene, "right_elbow_bone", text="Elbow")
        right_col.prop(scene, "right_wrist_bone", text="Wrist")
        right_col.prop(scene, "right_foot_bone", text="Foot")

class ARMATURE_PT_PoleTargets(bpy.types.Panel):
    bl_label = "Pole Targets"
    bl_idname = "ARMATURE_PT_pole_targets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_NAME
    bl_parent_id = "ARMATURE_PT_panel"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        col = layout.column(align=True)
        split = col.split(factor=0.5)

        left_col = split.column(align=True)
        left_col.label(text="Left Side")
        left_col.prop(scene, "pole_target_left", text="")

        right_col = split.column(align=True)
        right_col.label(text="Right Side")
        right_col.prop(scene, "pole_target_right", text="")

        layout.prop(scene, "pole_target_threshold", text="Threshold")

        # Activate/Deactivate
        row = layout.row(align=True)
        row.operator("elbows.activate_handler", text="Activate", icon='PLAY')
        row.operator("elbows.deactivate_handler", text="Deactivate", icon='PAUSE')

class ARMATURE_PT_IKFKSwitch(bpy.types.Panel):
    bl_label = "IK/FK Switch"
    bl_idname = "ARMATURE_PT_ikfk_switch"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = PANEL_NAME
    bl_parent_id = "ARMATURE_PT_panel"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.enabled = bool(scene.armature_object)

        row = layout.row(align=True)
        row.prop(scene, "ikfk_toe_toggle", text="")
        row.label(text="Toes:")

        col = layout.column(align=True)
        col.enabled = scene.ikfk_toe_toggle
        split = col.split(factor=0.5)

        left_col = split.column(align=True)
        left_col.prop(scene, "ikfk_left_toe", text="Left", slider=True)

        right_col = split.column(align=True)
        right_col.prop(scene, "ikfk_right_toe", text="Right", slider=True)

def register_panel():
    bpy.utils.register_class(SCENE_PT_Setup)
    bpy.utils.register_class(ARMATURE_PT_Panel)
    bpy.utils.register_class(ARMATURE_PT_PoleTargets)
    bpy.utils.register_class(ARMATURE_PT_IKFKSwitch)

def unregister_panel():
    bpy.utils.unregister_class(SCENE_PT_Setup)
    bpy.utils.unregister_class(ARMATURE_PT_Panel)
    bpy.utils.unregister_class(ARMATURE_PT_PoleTargets)
    bpy.utils.unregister_class(ARMATURE_PT_IKFKSwitch)
