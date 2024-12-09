
import bpy
from mathutils import Vector

ADJUSTMENT_VECTORS = {
    "Left": Vector((-0.3, 0.0, 0.0)),
    "Right": Vector((0.3, 0.0, 0.0))
}

def frame_change_handler(scene):
    armature = scene.armature_object
    threshold = scene.pole_target_threshold

    for side, locator, arm_bone, elbow_bone, wrist_bone in [
        ("Left", scene.pole_target_left, scene.left_arm_bone, scene.left_elbow_bone, scene.left_wrist_bone),
        ("Right", scene.pole_target_right, scene.right_arm_bone, scene.right_elbow_bone, scene.right_wrist_bone)
    ]:
        try:
            pose_bones = armature.pose.bones
            bone1 = pose_bones.get(arm_bone)
            bone2 = pose_bones.get(elbow_bone)
            bone3 = pose_bones.get(wrist_bone)

            if not all([bone1, bone2, bone3]):
                print(f"One or more bones ({arm_bone}, {elbow_bone}, {wrist_bone}) not found for side '{side}'.")
                continue

            bone1_matrix = armature.matrix_world @ bone1.matrix
            bone2_matrix = armature.matrix_world @ bone2.matrix
            bone3_matrix = armature.matrix_world @ bone3.matrix

            pos1 = bone1_matrix.translation
            pos2 = bone2_matrix.translation
            pos3 = bone3_matrix.translation
            matrix = bone1_matrix

            midPoint = (pos1 + pos3) * 0.5
            direction = pos2 - midPoint
            length = direction.length

            blendFactor = max(0, min(1, length / threshold))

            if length > 0.0001:
                normalDirection = direction.normalized() * 0.3
            else:
                normalDirection = Vector((0, 0, 0))

            adjustment = ADJUSTMENT_VECTORS.get(side, Vector((0.0, 0.0, 0.0)))
            adjustedDirection = matrix.to_3x3() @ adjustment

            finalDirection = (normalDirection * blendFactor) + (adjustedDirection * (1 - blendFactor))

            newPos = finalDirection + pos2
            locator.location = newPos

        except Exception as e:
            print(f"Error processing side '{side}': {e}")

def is_handler_registered(handler_name):
    return any(h.__name__ == handler_name for h in bpy.app.handlers.frame_change_post)

def register_frame_handler():
    handler_name = frame_change_handler.__name__
    if not is_handler_registered(handler_name):
        bpy.app.handlers.frame_change_post.append(frame_change_handler)
        print("Frame change handler has been registered and is now active.")
    else:
        print("Frame change handler is already registered and active.")

def unregister_frame_handler():
    handler_name = frame_change_handler.__name__
    bpy.app.handlers.frame_change_post[:] = [h for h in bpy.app.handlers.frame_change_post if h.__name__ != handler_name]
    print("Frame change handler has been unregistered.")
