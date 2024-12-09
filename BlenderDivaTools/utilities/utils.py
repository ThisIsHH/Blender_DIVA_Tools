
import bpy
import math

LOCATOR_PREFIX = "TempMotExport_"

class KeySet:
    def __init__(self, keyset_type, values):
        self.type = keyset_type
        self.values = values

def fix_rotation(res):
    half_pi = math.pi / 2.0
    two_pi = math.pi * 2.0

    curr_rot = 0
    rot_fix = 0.0
    _, rot_prev = res[0]

    for i in range(1, len(res)):
        frame, rot = res[i]
        if rot < -half_pi and rot_prev > half_pi and abs(rot - rot_prev) > half_pi:
            curr_rot += 1
            rot_fix = two_pi * float(curr_rot)
        elif rot > half_pi and rot_prev < -half_pi and abs(rot - rot_prev) > half_pi:
            curr_rot -= 1
            rot_fix = two_pi * float(curr_rot)

        if curr_rot != 0:
            res[i] = (frame, rot + rot_fix)
        rot_prev = rot

    return res

def is_static(values, decimals):
    if not values:
        return True
    rounded_values = [round(value, decimals) for value in values]
    first_value = rounded_values[0]
    return all(value == first_value for value in rounded_values)

def simplify_fcurves(remove_error_margin):
    # https://blender.stackexchange.com/questions/160728/decimate-f-curves-using-python

    C = bpy.context
    area_preferences = ['VIEW_3D', 'DOPESHEET_EDITOR', 'PROPERTIES', 'OUTLINER', 'TEXT_EDITOR']

    target_area = None
    for area_type in area_preferences:
        for area in C.screen.areas:
            if area.type == area_type:
                target_area = area
                break
        if target_area is not None:
            break

    if target_area is not None:
        old_area_type = target_area.type
        target_area.type = 'GRAPH_EDITOR'

        override_context = C.copy()
        override_context['area'] = target_area
        override_context['region'] = target_area.regions[0]

        with bpy.context.temp_override(**override_context):
            bpy.ops.graph.decimate(mode='ERROR', remove_error_margin=remove_error_margin)

        target_area.type = old_area_type
    else:
        print("Theres no area")

def calculate_hermite_tangents(keyframes):
    length = len(keyframes)
    result = []

    for i in range(length):
        frame, value, leftp, rightp = keyframes[i]

        if i == 0:
            in_t = 0.0
        else:
            t = frame - keyframes[i-1][0]
            in_t = 3 * (value - leftp) / t

        if i == length - 1:
            out_t = 0.0
        else:
            t = keyframes[i+1][0] - frame
            out_t = 3 * (rightp - value) / t

        result.append((frame, value, in_t, out_t))

    return result