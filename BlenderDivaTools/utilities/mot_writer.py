# Based on: https://github.com/korenkonder/PD_Tool/blob/master/KKdMainLib/Mot.cs

import struct

def align4(f):
    pos = f.tell()
    padding = (4 - (pos % 4)) % 4
    if padding:
        f.write(b'\x00' * padding)

def write_header(f, mot_headers):
    f.seek(0)
    for mot_header in mot_headers:
        f.write(struct.pack('<I', mot_header['KeySetOffset']))
        f.write(struct.pack('<I', mot_header['KeySetTypesOffset']))
        f.write(struct.pack('<I', mot_header['KeySetDataOffset']))
        f.write(struct.pack('<I', mot_header['BoneInfoOffset']))
    f.write(struct.pack('<I', 0))
    f.write(struct.pack('<I', 0))
    f.write(struct.pack('<I', 0))
    f.write(struct.pack('<I', 0))

def write_keyset_types(f, keyset_types):
    i = 0
    while i < len(keyset_types):
        word_value = 0
        for bit_index in range(8):
            if i + bit_index < len(keyset_types):
                keyset_type = keyset_types[i + bit_index]
                word_value |= (keyset_type & 0b11) << (bit_index * 2)
        f.write(struct.pack('<H', word_value))
        i += 8
    align4(f)

def write_keyset_data(f, export_data):
    for index, keyset in enumerate(export_data):
        if keyset is None:
            #print(f"Entry {index}: None keyset")
            continue  
        
        keyset_type = keyset.type
        keyset_values = keyset.values

        if keyset_type == 1:
            
            #print(f"Entry {index}: Writing a static keyset.")
            f.write(struct.pack('<f', keyset_values[0]))

        elif keyset_type == 2:
            
            key_count = len(keyset_values)
            #print(f"Entry {index}: Writing a linear keyset with {key_count} keys.")
            f.write(struct.pack('<H', key_count))
            for frame, value in keyset_values:
                f.write(struct.pack('<H', frame))
            align4(f)  
            for frame, value in keyset_values:
                f.write(struct.pack('<f', value))

        elif keyset_type == 3:
            key_count = len(keyset_values)
            #print(f"Entry {index}: Writing a tangent keyset with {key_count} keys.")
            f.write(struct.pack('<H', key_count))

            for frame, value, tangent in keyset_values:
                f.write(struct.pack('<H', frame))
            align4(f)

            for frame, value, tangent in keyset_values:
                f.write(struct.pack('<f', value))
                f.write(struct.pack('<f', tangent))
            #align4(f)

        else:
            pass

    align4(f)

def write_bone_info(f, bone_info):
    for bone_index in bone_info:
        f.write(struct.pack('<H', bone_index))
    f.write(struct.pack('<H', 0))
    align4(f)

def write_mot_bin(output_path, export_data, bone_info, frame_count):
    with open(output_path, 'wb') as f:
        mot_count = 1
        header_size = (mot_count + 1) * 16
        f.seek(header_size)

        mot_headers = []
        mot_header = {}
        mot_header['KeySetOffset'] = f.tell()
        high_bits = 1
        keyset_count = len(export_data)
        f.write(struct.pack('<H', (high_bits << 14) | (keyset_count & 0x3FFF)))
        f.write(struct.pack('<H', frame_count))

        mot_header['KeySetTypesOffset'] = f.tell()
        keyset_types = []
        for keyset in export_data:
            if keyset is None:
                keyset_types.append(0)
            else:
                keyset_type = keyset.type
                keyset_types.append(keyset_type)
        write_keyset_types(f, keyset_types)

        mot_header['KeySetDataOffset'] = f.tell()
        write_keyset_data(f, export_data)

        mot_header['BoneInfoOffset'] = f.tell()
        write_bone_info(f, bone_info)

        mot_headers.append(mot_header)
        write_header(f, mot_headers)
