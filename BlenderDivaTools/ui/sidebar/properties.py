
import bpy
from .handler_ikfk import update_toes_toggle, update_ikfk_right_toe, update_ikfk_left_toe

def register_properties():
    # General Armature
    bpy.types.Scene.armature_object = bpy.props.PointerProperty(
        name="Armature",
        type=bpy.types.Object,
        description="Select the armature to use"
    )

    # Left Side Bones
    bpy.types.Scene.left_arm_bone = bpy.props.StringProperty(
        name="Left Arm Bone",
        description="Name for the left arm bone",
        default="左腕"
    )
    bpy.types.Scene.left_elbow_bone = bpy.props.StringProperty(
        name="Left Elbow Bone",
        description="Name for the left elbow bone",
        default="左ひじ"
    )
    bpy.types.Scene.left_wrist_bone = bpy.props.StringProperty(
        name="Left Wrist Bone",
        description="Name for the left wrist bone",
        default="左手首"
    )
    bpy.types.Scene.left_foot_bone = bpy.props.StringProperty(
        name="Left Foot Bone",
        description="Name of the left foot bone",
        default="左足首"
    )

    # Right Side Bones
    bpy.types.Scene.right_arm_bone = bpy.props.StringProperty(
        name="Right Arm Bone",
        description="Name for the right arm bone",
        default="右腕"
    )
    bpy.types.Scene.right_elbow_bone = bpy.props.StringProperty(
        name="Right Elbow Bone",
        description="Name for the right elbow bone",
        default="右ひじ"
    )
    bpy.types.Scene.right_wrist_bone = bpy.props.StringProperty(
        name="Right Wrist Bone",
        description="Name for the right wrist bone",
        default="右手首"
    )
    bpy.types.Scene.right_foot_bone = bpy.props.StringProperty(
        name="Right Foot Bone",
        description="Name of the right foot bone",
        default="右足首"
    )

    # Pole Targets
    bpy.types.Scene.pole_target_threshold = bpy.props.FloatProperty(
        name="Threshold",
        description="Threshold for pole target calculation",
        default=0.15,
        min=0.01,
        max=10.0
    )
    bpy.types.Scene.pole_target_left = bpy.props.PointerProperty(
        name="Left Pole Target",
        type=bpy.types.Object,
        description="Select the left pole target"
    )
    bpy.types.Scene.pole_target_right = bpy.props.PointerProperty(
        name="Right Pole Target",
        type=bpy.types.Object,
        description="Select the right pole target"
    )

    # Toes IK/FK Toggle
    bpy.types.Scene.ikfk_toe_toggle = bpy.props.BoolProperty(
        name="Toe IK/FK Toggle",
        description="Toggle IK/FK for both toes",
        default=True,
        update=update_toes_toggle
    )
    bpy.types.Scene.ikfk_left_toe = bpy.props.FloatProperty(
        name="Left Toe IK/FK",
        description="Control the IK influence for the left toe",
        default=1.0,
        min=0.0,
        max=1.0,
        update=update_ikfk_left_toe
    )
    bpy.types.Scene.ikfk_right_toe = bpy.props.FloatProperty(
        name="Right Toe IK/FK",
        description="Control the IK influence for the right toe",
        default=1.0,
        min=0.0,
        max=1.0,
        update=update_ikfk_right_toe
    )

def unregister_properties():
    del bpy.types.Scene.armature_object
    del bpy.types.Scene.left_arm_bone
    del bpy.types.Scene.left_elbow_bone
    del bpy.types.Scene.left_wrist_bone
    del bpy.types.Scene.right_arm_bone
    del bpy.types.Scene.right_elbow_bone
    del bpy.types.Scene.right_wrist_bone
    del bpy.types.Scene.left_foot_bone
    del bpy.types.Scene.right_foot_bone
    del bpy.types.Scene.pole_target_threshold
    del bpy.types.Scene.pole_target_left
    del bpy.types.Scene.pole_target_right
    del bpy.types.Scene.ikfk_toe_toggle
    del bpy.types.Scene.ikfk_left_toe
    del bpy.types.Scene.ikfk_right_toe
