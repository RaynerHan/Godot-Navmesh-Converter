import re
import sys
import os

def parse_vector3_array(data):
    match = re.search(r'vertices\s*=\s*PackedVector3Array\((.*?)\)', data, re.DOTALL)
    if not match:
        print("Error: Could not find PackedVector3Array in input file")
        return []
    
    try:
        vertices = [float(x) for x in match.group(1).replace('\n', '').split(',')]
        return [(vertices[i], vertices[i+1], vertices[i+2]) for i in range(0, len(vertices), 3)]
    except ValueError:
        print("Error: Failed to parse vertex data")
        return []

def parse_int_array_list(data):
    match = re.search(r'polygons\s*=\s*\[(.*?)\]', data, re.DOTALL)
    if not match:
        print("Error: Could not find polygons array in input file")
        return []
    
    arrays = re.findall(r'PackedInt32Array\((.*?)\)', match.group(1))
    try:
        return [[int(x) for x in arr.split(',')] for arr in arrays]
    except ValueError:
        print("Error: Failed to parse polygon data")
        return []

def parse_navigation_properties(data):
    properties = {}
    
    property_patterns = {
        'agent_height': r'agent_height\s*=\s*([\d.]+)',
        'agent_radius': r'agent_radius\s*=\s*([\d.]+)',
        'agent_max_climb': r'agent_max_climb\s*=\s*([\d.]+)',
        'agent_max_slope': r'agent_max_slope\s*=\s*([\d.]+)',
        'region_min_size': r'region_min_size\s*=\s*([\d.]+)',
        'region_merge_size': r'region_merge_size\s*=\s*([\d.]+)',
        'edge_max_length': r'edge_max_length\s*=\s*([\d.]+)',
        'edge_max_error': r'edge_max_error\s*=\s*([\d.]+)',
        'vertices_per_polygon': r'vertices_per_polygon\s*=\s*([\d.]+)',
        'detail_sample_distance': r'detail_sample_distance\s*=\s*([\d.]+)',
        'detail_sample_max_error': r'detail_sample_max_error\s*=\s*([\d.]+)',
    }
    
    bool_patterns = {
        'filter_low_hanging_obstacles': r'filter_low_hanging_obstacles\s*=\s*(true|false)',
        'filter_ledge_spans': r'filter_ledge_spans\s*=\s*(true|false)',
        'filter_walkable_low_height_spans': r'filter_walkable_low_height_spans\s*=\s*(true|false)',
    }
    
    for prop, pattern in property_patterns.items():
        match = re.search(pattern, data)
        if match:
            properties[prop] = float(match.group(1))
    
    for prop, pattern in bool_patterns.items():
        match = re.search(pattern, data)
        if match:
            properties[prop] = match.group(1) == 'true'
    
    return properties

def parse_obj_file(file_path):
    vertices, faces = [], []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            if parts and parts[0] == 'v':
                try:
                    vertices.append(tuple(map(float, parts[1:4])))
                except ValueError:
                    print(f"Warning: Invalid vertex data {parts}")
            elif parts and parts[0] == 'f':
                try:
                    face_indices = []
                    for p in parts[1:]:
                        if '/' in p:
                            face_indices.append(int(p.split('/')[0]) - 1)
                        else:
                            face_indices.append(int(p) - 1)
                    faces.append(face_indices)
                except ValueError:
                    print(f"Warning: Invalid face data {parts}")
    return vertices, faces

def write_obj_file(vertices, faces, output_file):
    with open(output_file, 'w') as f:
        f.write("# Converted from Godot NavigationMesh\n")
        f.write("mtllib navmesh.mtl\n")
        f.write("o navmesh\n")
        
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        
        f.write("vn -0.0000 -1.0000 -0.0000\n")
        f.write("s 0\n")
        
        for face in faces:
            f.write(f"f {' '.join(f'{idx+1}//1' for idx in face)}\n")

def write_godot_resource(vertices, faces, output_file, properties=None):
    with open(output_file, 'w') as f:
        f.write("[gd_resource type=\"NavigationMesh\" format=3]\n\n")
        f.write("[resource]\n")
        
        f.write("vertices = PackedVector3Array(" + ', '.join(f"{v[0]}, {v[1]}, {v[2]}" for v in vertices) + ")\n")
        f.write("polygons = [" + ', '.join(f"PackedInt32Array({', '.join(map(str, face))})" for face in faces) + "]\n")
        
        if properties:
            for prop, value in properties.items():
                if isinstance(value, bool):
                    f.write(f"{prop} = {'true' if value else 'false'}\n")
                else:
                    f.write(f"{prop} = {value}\n")
        else:
            f.write("agent_height = 0.5\n")
            f.write("vertices_per_polygon = 3.0\n")
            f.write("detail_sample_distance = 1.0\n")
            f.write("filter_low_hanging_obstacles = true\n")
            f.write("filter_ledge_spans = true\n")
            f.write("filter_walkable_low_height_spans = true\n")

def tres_to_obj(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            data = f.read()
        
        vertices = parse_vector3_array(data)
        faces = parse_int_array_list(data)
        
        if vertices and faces:
            write_obj_file(vertices, faces, output_file)
            print(f"Converted {len(vertices)} vertices and {len(faces)} faces to {output_file}")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def obj_to_tres(input_file, output_file, original_tres=None):
    try:
        properties = {}
        
        if original_tres and os.path.exists(original_tres):
            with open(original_tres, 'r') as f:
                properties = parse_navigation_properties(f.read())
        
        vertices, faces = parse_obj_file(input_file)
        if vertices and faces:
            write_godot_resource(vertices, faces, output_file, properties)
            print(f"Converted {len(vertices)} vertices and {len(faces)} faces to NavigationMesh resource")
            return True
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: script.py input_file [output_file] [original_tres_for_properties]")
        return
    
    input_file = sys.argv[1]
    ext = os.path.splitext(input_file)[1].lower()
    
    output_file = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(input_file)[0] + (".obj" if ext == ".tres" else ".tres")
    
    original_tres = None
    if len(sys.argv) > 3 and ext != ".tres":
        original_tres = sys.argv[3]
    
    if ext == ".tres":
        success = tres_to_obj(input_file, output_file)
    else:
        success = obj_to_tres(input_file, output_file, original_tres)
    
    print("Success!" if success else "Conversion failed.")

if __name__ == "__main__":
    main()