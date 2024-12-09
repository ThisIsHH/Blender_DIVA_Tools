
import bpy
from .utils import *

def obj_structure(obj_v):
    tolerance = 1e-6
    if obj_v == 0:
        return None
    elif isinstance(obj_v, float):
        return KeySet(1, [obj_v])
    else:
        obj_v = calculate_hermite_tangents(obj_v)
        values = []
        for frame, value, in_t, out_t in obj_v:
            if abs(in_t - out_t) < tolerance:
                avg_t = (in_t + out_t) * 0.5
                values.append((frame, value, avg_t))
            else:
                values.append((frame, value, in_t))
                values.append((frame, value, out_t))
        return KeySet(3, values)

def handle_locator(locator_type, locator_name):
    def get_position_keysets(obj):
        return [obj_structure(anim_loc(obj, axis=i)) for i in range(3)]

    def get_rotation_keysets(obj):
        return [obj_structure(anim_rot(obj, axis=i)) for i in range(3)]

    keysets = []
    locator_full_name = f"{LOCATOR_PREFIX}{locator_name}"
    obj = bpy.data.objects.get(locator_full_name)

    if locator_type == "Position":
        keysets = get_position_keysets(obj)
    
    elif locator_type == "Rotation":
        keysets = get_rotation_keysets(obj)

    elif locator_type in ["PositionRotation", "HeadIKTargetRotation", "ArmIKTargetRotation", "LegIKTargetRotation"]:
        keysets = get_position_keysets(obj) + get_rotation_keysets(obj)

    elif locator_type == "GlobalPosition":
        keysets = get_position_keysets(obj)

    elif locator_type == "GlobalRotation":
        keysets = get_rotation_keysets(obj)

    return keysets

def cleanup_locators():
    for obj in bpy.data.objects:
        if obj.name.startswith(LOCATOR_PREFIX):
            bpy.data.objects.remove(obj, do_unlink=True)

def anim_loc(obj, axis):
    if obj.animation_data is None or obj.animation_data.action is None:
        return obj.location[axis]

    anim = obj.animation_data.action.fcurves.find('location', index=axis)
    if anim is None:
        return obj.location[axis]

    keyframes = []
    for point in anim.keyframe_points:
        frame = int(point.co[0])
        value = point.co[1]
        leftp = point.handle_left[1]
        rightp = point.handle_right[1]
        keyframes.append((frame, value, leftp, rightp))

    return keyframes

def anim_rot(obj, axis):
    if obj.animation_data is None or obj.animation_data.action is None:
        return obj.rotation_euler[axis]

    anim = obj.animation_data.action.fcurves.find('rotation_euler', index=axis)
    if anim is None:
        return obj.rotation_euler[axis]

    keyframes = []
    for point in anim.keyframe_points:
        frame = int(point.co[0])
        value = point.co[1]
        leftp = point.handle_left[1]
        rightp = point.handle_right[1]
        keyframes.append((frame, value, leftp, rightp))

    return keyframes
