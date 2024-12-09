
import bpy

class ImportMotionBinOperator(bpy.types.Operator):
    bl_idname = "import_motion.bin"
    bl_label = "Import Mot Set (.bin)"
    bl_description = "Import motion data from a Mot set file (.bin) / Not implemented yet!"

    def execute(self, context):
        self.report({'WARNING'}, "")
        return {'CANCELLED'}

def register():
    bpy.utils.register_class(ImportMotionBinOperator)

def unregister():
    bpy.utils.unregister_class(ImportMotionBinOperator)
