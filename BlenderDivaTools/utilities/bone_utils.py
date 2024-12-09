
import bpy
from .utils import *

def collect_bone_transformations(armature_name, frame_start, frame_end):
    bone_transformations = {}
    for frame in range(frame_start, frame_end + 1):
        bpy.context.scene.frame_set(frame)
        for obj in bpy.context.scene.objects:
            if obj.type == 'ARMATURE' and obj.name == armature_name:
                for pbone in obj.pose.bones:
                    bone_key = (obj.name, pbone.name)
                    if bone_key not in bone_transformations:
                        bone_transformations[bone_key] = []
                    parent_bone = pbone.parent
                    if parent_bone is not None:
                        bone_transform = parent_bone.matrix.inverted() @ pbone.matrix
                    else:
                        bone_transform = pbone.matrix.copy()
                    bone_transformations[bone_key].append((frame, bone_transform))
    return bone_transformations

def get_bone_position(bone_transformations, armature_name, bone_name):
    res_x, res_y, res_z = [], [], []

    if (armature_name, bone_name) not in bone_transformations:
        return res_x, res_y, res_z

    for frame, bone_matrix in bone_transformations[(armature_name, bone_name)]:
        value = bone_matrix.to_translation()
        res_x.append((frame, value[0]))
        res_y.append((frame, value[1]))
        res_z.append((frame, value[2]))

    return res_x, res_y, res_z

def get_bone_rotation(bone_transformations, armature_name, bone_name):
    res_x, res_y, res_z = [], [], []

    if (armature_name, bone_name) not in bone_transformations:
        return res_x, res_y, res_z

    for frame, bone_matrix in bone_transformations[(armature_name, bone_name)]:
        value = bone_matrix.to_euler('XYZ')
        res_x.append((frame, value[0]))
        res_y.append((frame, value[1]))
        res_z.append((frame, value[2]))

    res_x = fix_rotation(res_x)
    res_y = fix_rotation(res_y)
    res_z = fix_rotation(res_z)

    return res_x, res_y, res_z

def bone_structure(obj_v, decimals, scale_keys, frame_start):
    if not obj_v:
        return None
    values = [i[1] for i in obj_v]

    if is_static(values, decimals):
        static_value = round(values[0], decimals)
        if static_value == 0:
            return None
        else:
            return KeySet(1, [static_value])
    else:
        scaled_keys = [[int((frame - frame_start) * scale_keys), value] for frame, value in obj_v]
        return KeySet(2, scaled_keys)

def handle_bone(bone_data, bone_transformations, armature_name, decimals, scale_keys, frame_start):
    def structure_bone_components(components):
        return [bone_structure(component, decimals, scale_keys, frame_start) for component in components]

    def get_position_components(bone_name):
        return get_bone_position(bone_transformations, armature_name, bone_name)

    def get_rotation_components(bone_name):
        return get_bone_rotation(bone_transformations, armature_name, bone_name)

    bone_name = bone_data["Name"]
    bone_type = bone_data["Type"]
    ik_bone_name = bone_data["IKTarget"]

    if bone_type == "Position":
        return structure_bone_components(get_position_components(bone_name))

    elif bone_type == "Rotation":
        return structure_bone_components(get_rotation_components(bone_name))

    elif bone_type == "PositionRotation":
        pos_components = get_position_components(bone_name)
        rot_components = get_rotation_components(bone_name)
        return structure_bone_components(pos_components + rot_components)

    elif bone_type in ["HeadIKTargetRotation", "ArmIKTargetRotation", "LegIKTargetRotation"]:
        pos_components = get_position_components(ik_bone_name)
        rot_components = get_rotation_components(bone_name)
        return structure_bone_components(pos_components + rot_components)

    elif bone_type == "GlobalPosition":
        return structure_bone_components(get_position_components(bone_name))

    elif bone_type == "GlobalRotation":
        return structure_bone_components(get_rotation_components(bone_name))

    else:
        return []

def create_locator_for_bone(bone_name, keysets, bone_type, decimate_margin):
    locator_name = f"{LOCATOR_PREFIX}{bone_name}"
    if locator_name in bpy.data.objects:
        locator = bpy.data.objects[locator_name]
    else:
        bpy.ops.object.empty_add(type='PLAIN_AXES')
        locator = bpy.context.active_object
        locator.name = locator_name
        locator.empty_display_type = 'ARROWS'

    if bone_type in ["Position", "GlobalPosition"]:
        position_keysets = keysets[:3]
        for axis, keyset, index in zip(['x', 'y', 'z'], position_keysets, [0, 1, 2]):
            if keyset and keyset.type == 1:
                setattr(locator.location, axis, keyset.values[0])
            elif keyset and keyset.type == 2:
                for frame, value in keyset.values:
                    setattr(locator.location, axis, value)
                    locator.keyframe_insert(data_path='location', frame=frame, index=index)
                simplify_fcurves(decimate_margin)

    elif bone_type in ["Rotation", "GlobalRotation"]:
        rotation_keysets = keysets[:3]
        for axis, keyset, index in zip(['x', 'y', 'z'], rotation_keysets, [0, 1, 2]):
            if keyset and keyset.type == 1:
                setattr(locator.rotation_euler, axis, keyset.values[0])
            elif keyset and keyset.type == 2:
                for frame, value in keyset.values:
                    setattr(locator.rotation_euler, axis, value)
                    locator.keyframe_insert(data_path='rotation_euler', frame=frame, index=index)
                simplify_fcurves(decimate_margin)

    elif bone_type in ["PositionRotation", "HeadIKTargetRotation", "ArmIKTargetRotation", "LegIKTargetRotation"]:
        position_keysets = keysets[:3]
        rotation_keysets = keysets[3:6]

        for axis, keyset, index in zip(['x', 'y', 'z'], position_keysets, [0, 1, 2]):
            if keyset and keyset.type == 1:
                setattr(locator.location, axis, keyset.values[0])
            elif keyset and keyset.type == 2:
                for frame, value in keyset.values:
                    setattr(locator.location, axis, value)
                    locator.keyframe_insert(data_path='location', frame=frame, index=index)
                simplify_fcurves(decimate_margin)

        for axis, keyset, index in zip(['x', 'y', 'z'], rotation_keysets, [0, 1, 2]):
            if keyset and keyset.type == 1:
                setattr(locator.rotation_euler, axis, keyset.values[0])
            elif keyset and keyset.type == 2:
                for frame, value in keyset.values:
                    setattr(locator.rotation_euler, axis, value)
                    locator.keyframe_insert(data_path='rotation_euler', frame=frame, index=index)
                simplify_fcurves(decimate_margin)

    #print(f"Locator created: {bone_name}")


