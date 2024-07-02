import sys
import os

def parse_arguments():
    if len(sys.argv) != 3:
        print("Usage: program.exe pathFile1.x pathFile2.y")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: {input_file} does not exist.")
        sys.exit(1)

    return input_file, output_file

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    print(f"Converting {input_file} to {output_file}")

import json

def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print("JSON data loaded successfully.")
            return data
    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        sys.exit(1)

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    data = load_json(input_file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f"Data successfully saved to {file_path}")

def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            print("YAML data loaded successfully.")
            return data
    except yaml.YAMLError:
        print("Error: Invalid YAML format.")
        sys.exit(1)

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file)
        print(f"Data successfully saved to {file_path}")

def load_xml(file_path):
    try:
        import xml.etree.ElementTree as ET
        tree = ET.parse(file_path)
        root = tree.getroot()
        print("XML data loaded successfully.")
        return ET.tostring(root, encoding='utf8').decode('utf8')
    except ET.ParseError:
        print("Error: Invalid XML format.")
        sys.exit(1)

def save_xml(data, file_path):
    try:
        import xml.dom.minidom as minidom
        dom = minidom.parseString(data)
        with open(file_path, 'w') as file:
            file.write(dom.toprettyxml())
        print(f"Data successfully saved to {file_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def convert_data(input_file, output_file):
    _, input_ext = os.path.splitext(input_file)
    _, output_ext = os.path.splitext(output_file)

    load_func = None
    save_func = None

    if input_ext == ".json":
        load_func = load_json
    elif input_ext == ".yml" or input_ext == ".yaml":
        load_func = load_yaml
    elif input_ext == ".xml":
        load_func = load_xml
    else:
        print("Unsupported input file format.")
        sys.exit(1)

    if output_ext == ".json":
        save_func = save_json
    elif output_ext == ".yml" or output_ext == ".yaml":
        save_func = save_yaml
    elif output_ext == ".xml":
        save_func = save_xml
    else:
        print("Unsupported output file format.")
        sys.exit(1)

    data = load_func(input_file)
    save_func(data, output_file)

if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    convert_data(input_file, output_file)