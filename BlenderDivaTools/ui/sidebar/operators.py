
import bpy
from .handler_elbow import register_frame_handler, unregister_frame_handler

class ELBOWS_OT_ActivateHandler(bpy.types.Operator):
    bl_idname = "elbows.activate_handler"
    bl_label = "Activate Elbow Handler"

    def execute(self, context):
        scene = context.scene

        if not scene.armature_object or scene.armature_object.type != 'ARMATURE':
            self.report({'ERROR'}, "No valid armature selected. Please select an armature.")
            return {'CANCELLED'}

        if not scene.pole_target_left or not scene.pole_target_right:
            self.report({'ERROR'}, "One or both pole targets are not set. Please select the targets.")
            return {'CANCELLED'}

        register_frame_handler()
        self.report({'INFO'}, "Elbow frame handler activated.")
        return {'FINISHED'}

class ELBOWS_OT_DeactivateHandler(bpy.types.Operator):
    bl_idname = "elbows.deactivate_handler"
    bl_label = "Deactivate Elbow Handler"

    def execute(self, context):
        unregister_frame_handler()
        self.report({'INFO'}, "Elbow frame handler deactivated.")
        return {'FINISHED'}

class ARMATURE_OT_DetectObjects(bpy.types.Operator):
    bl_idname = "armature.detect_objects"
    bl_label = "Auto-Detect Armature and Targets"

    def execute(self, context):
        scene = context.scene
        armature_found = False
        left_target_found = False
        right_target_found = False

        # Armature
        for obj in bpy.data.objects:
            if obj.type == 'ARMATURE' and obj.name == "Import Rig":
                scene.armature_object = obj
                self.report({'INFO'}, f"Armature '{obj.name}' detected and selected.")
                armature_found = True

        if not armature_found:
            self.report({'WARNING'}, "Armature 'Import Rig' not found. Please select manually.")

        # Pole targets
        for obj in bpy.data.objects:
            if obj.name == "ElbowPole_左":
                scene.pole_target_left = obj
                self.report({'INFO'}, f"Left pole target '{obj.name}' detected.")
                left_target_found = True
            elif obj.name == "ElbowPole_右":
                scene.pole_target_right = obj
                self.report({'INFO'}, f"Right pole target '{obj.name}' detected.")
                right_target_found = True

        if not left_target_found:
            self.report({'WARNING'}, "Left pole target 'ElbowPole_左' not found. Please select manually.")
        if not right_target_found:
            self.report({'WARNING'}, "Right pole target 'ElbowPole_右' not found. Please select manually.")

        return {'FINISHED'}

def register_operators():
    bpy.utils.register_class(ELBOWS_OT_ActivateHandler)
    bpy.utils.register_class(ELBOWS_OT_DeactivateHandler)
    bpy.utils.register_class(ARMATURE_OT_DetectObjects)

def unregister_operators():
    bpy.utils.unregister_class(ELBOWS_OT_ActivateHandler)
    bpy.utils.unregister_class(ELBOWS_OT_DeactivateHandler)
    bpy.utils.unregister_class(ARMATURE_OT_DetectObjects)
