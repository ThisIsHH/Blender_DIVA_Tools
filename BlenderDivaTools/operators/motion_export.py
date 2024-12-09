
import os
import xml.etree.ElementTree as ET
import bpy
from ..utilities import bone_utils, locators_utils, mot_writer

def read_data():
    addon_dir = os.path.dirname(os.path.dirname(__file__))
    xml_file = os.path.join(addon_dir, "data", "BoneDataTypes.xml")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    # Bones
    bones_data = []
    for elem in root.findall("Bones/Bone"):
        item_data = {
            "Name": elem.find("Name").text,
            "Type": elem.find("Type").text,
            "IKTarget": elem.find("IKTarget").text if elem.find("IKTarget") is not None else None
        }
        bones_data.append(item_data)
    
    # BoneInfo
    bone_info = []
    for elem in root.findall("BoneInfo/id"):
        bone_info.append(int(elem.text))
    
    return bones_data, bone_info

def collect_transformations(object_name, frame_start, frame_end):
    return bone_utils.collect_bone_transformations(object_name, frame_start, frame_end)

def process_bones(bones_data, armature_name, bone_transformations, decimals, scale_keys, enable_animation, decimate_margin, frame_start):
    export_data = []
    
    for bone in bones_data:
        keysets = bone_utils.handle_bone(
            bone,
            bone_transformations,
            armature_name,
            decimals,
            scale_keys,
            frame_start
        )
        export_data.extend(keysets)

        if enable_animation:
            bone_utils.create_locator_for_bone(
                bone["Name"], keysets, bone["Type"], decimate_margin=decimate_margin
            )

    export_data.append(None)
    return export_data

def process_locators(locator_data, filepath, frame_count, bone_info):
    locator_export_data = []

    for locator in locator_data:
        keysets = locators_utils.handle_locator(locator["Type"], locator["Name"])
        locator_export_data.extend(keysets)

    locator_export_data.append(None)
    mot_writer.write_mot_bin(filepath, locator_export_data, bone_info, frame_count)

def export_motion(armature, filepath, decimals, scale_keys, enable_animation, decimate_margin):
    try:
        bones_data, bone_info = read_data()

        frame_start = bpy.context.scene.frame_start
        frame_end = bpy.context.scene.frame_end
        frame_count = int(((frame_end - frame_start) * scale_keys) + 1) 

        bone_transformations = collect_transformations(armature.name, frame_start, frame_end)

        export_data = process_bones(
            bones_data, armature.name, bone_transformations, decimals, scale_keys, enable_animation, decimate_margin, frame_start
        )

        if enable_animation:
            locator_data = bones_data
            process_locators(locator_data, filepath, frame_count, bone_info)
            locators_utils.cleanup_locators()
        else:
            mot_writer.write_mot_bin(filepath, export_data, bone_info, frame_count)

        print("Export completed successfully.")
        return True

    except Exception as e:
        print(f"Error: {e}")
        return False