
# IK/FK Update

def update_ikfk_influence(armature, bone_name, influence):
    if not armature or armature.type != 'ARMATURE' or not bone_name:
        return

    try:
        bone = armature.pose.bones[bone_name]
        constraint = bone.constraints.get("IK")
        if constraint:
            constraint.influence = influence
    except KeyError:
        print(f"Bone '{bone_name}' or constraint 'IK' not found.")

def update_toes_toggle(self, context):
    armature = context.scene.armature_object
    if not armature or armature.type != 'ARMATURE':
        return

    left_foot_bone_name = context.scene.left_foot_bone
    right_foot_bone_name = context.scene.right_foot_bone

    left_influence = 0.0 if not context.scene.ikfk_toe_toggle else context.scene.ikfk_left_toe
    right_influence = 0.0 if not context.scene.ikfk_toe_toggle else context.scene.ikfk_right_toe

    update_ikfk_influence(armature, left_foot_bone_name, left_influence)
    update_ikfk_influence(armature, right_foot_bone_name, right_influence)


def update_ikfk_left_toe(self, context):
    if context.scene.ikfk_toe_toggle:
        armature = context.scene.armature_object
        left_foot_bone_name = context.scene.left_foot_bone
        left_influence = context.scene.ikfk_left_toe
        update_ikfk_influence(armature, left_foot_bone_name, left_influence)


def update_ikfk_right_toe(self, context):
    if context.scene.ikfk_toe_toggle:
        armature = context.scene.armature_object
        right_foot_bone_name = context.scene.right_foot_bone
        right_influence = context.scene.ikfk_right_toe
        update_ikfk_influence(armature, right_foot_bone_name, right_influence)

