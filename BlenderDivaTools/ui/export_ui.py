
import bpy
from bpy.props import FloatProperty, StringProperty, BoolProperty, IntProperty
from bpy_extras.io_utils import ExportHelper
from ..operators import motion_export

class ExportMotionBinOperator(bpy.types.Operator, ExportHelper):
    bl_idname = "export_motion.bin"
    bl_label = "Export Mot Set (.bin)"
    bl_description = "Export motion data of selected Armature object to Mot set file (.bin)"
    bl_options = {'PRESET'}
    filename_ext = ".bin"

    filter_glob: StringProperty(default="*.bin", options={'HIDDEN'})

    decimals: IntProperty(
        name="Static Precision",
        description="Number of decimal places for rounding static values",
        default=4,
        min=0,
        max=8
    )
    scale_keys: FloatProperty(
        name="Scale Keys",
        description="Scale factor for keyframes (e.g., 2.0 for doubling frame rate if 30FPS)",
        default=1.0,
        min=1.0,
        max=100.0
    )
    enable_animation: BoolProperty(
        name="Simplify Animation Curves",
        description="(WARNING!: Using this option may impact Blender's performance. Enable only if needed for your workflow)",
        default=False
    )
    decimate_margin: FloatProperty(
        name="Curve Margin",
        description="Error margin for decimating animation curves.",
        default=0.005225,
        min=0.0,
        max=10.0
    )

    def invoke(self, context, event):
        self.filepath = "PV0000_DMY_P1_00.bin"
        return super().invoke(context, event)

    @classmethod
    def poll(cls, context):
        return context.object and context.object.type == 'ARMATURE'

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False
        draw_general_panel(layout, self)
        draw_animation_panel(layout, self)

    def execute(self, context):
        return execute_motion_export(self, context)

def draw_general_panel(layout, operator):
    general_panel, general_body = layout.panel("MOT_Export_General", default_closed=False)
    general_panel.label(text="General")
    if general_body:
        general_body.prop(operator, "decimals")
        general_body.prop(operator, "scale_keys")

def draw_animation_panel(layout, operator):
    header, body = layout.panel("MOT_Export_AnimationCurves", default_closed=False)
    header.use_property_split = False
    header.prop(operator, "enable_animation", text="")
    header.label(text="Optimize Animation Curves")
    row_header = header.row()
    row_header.label(text="", icon='ERROR')
    
    if body:
        body.enabled = operator.enable_animation
        body.prop(operator, "decimate_margin")

def execute_motion_export(operator, context):
    armature = context.object

    if not armature or armature.type != 'ARMATURE':
        operator.report({'ERROR'}, "No armature selected.")
        return {'CANCELLED'}

    decimals = operator.decimals
    scale_keys = operator.scale_keys
    enable_animation = operator.enable_animation
    decimate_margin = operator.decimate_margin if enable_animation else None

    result = motion_export.export_motion(
        armature=armature,
        filepath=operator.filepath,
        decimals=decimals,
        scale_keys=scale_keys,
        enable_animation=enable_animation,
        decimate_margin=decimate_margin
    )

    if result:
        operator.report({'INFO'}, f"Export completed: {operator.filepath}")
        return {'FINISHED'}
    else:
        operator.report({'ERROR'}, "Export failed.")
        return {'CANCELLED'}

def menu_func_export(self, context):
    self.layout.operator(ExportMotionBinOperator.bl_idname, text="DIVA Motion Set (.bin)")

def register():
    bpy.utils.register_class(ExportMotionBinOperator)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    bpy.utils.unregister_class(ExportMotionBinOperator)
