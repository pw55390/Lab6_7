import sys
import os
import json
import yaml
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# Funkcja do parsowania argumentów wiersza poleceń
def parse_arguments():
    if len(sys.argv) != 3:
        print("Argumenty konieczne: program.exe pathFile1 pathFile2")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Błąd: {input_file} nie istnieje.")
        sys.exit(1)

    return input_file, output_file

# Funkcja do ładowania danych z pliku JSON
def load_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print("Dane JSON załadowane prawidłowo")
            return data
    except json.JSONDecodeError:
        print("Błąd: Nieprawidłowy plik JSON.")
        sys.exit(1)

# Funkcja do zapisywania danych do pliku JSON
def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)
        print(f"Dane zapisane do {file_path}")

# Funkcja do ładowania danych z pliku YAML
def load_yaml(file_path):
    try:
        with open(file_path, 'r') as file:
            data = yaml.safe_load(file)
            print("Plik YAML wczytany prawidłowo.")
            return data
    except yaml.YAMLError:
        print("Błąd: Nieprawidłowy plik YAML.")
        sys.exit(1)

# Funkcja do zapisywania danych do pliku YAML
def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.safe_dump(data, file)
        print(f"Dane zapisane do {file_path}")

# Funkcja do ładowania danych z pliku XML
def load_xml(file_path):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        print("XML został wczytany.")
        return ET.tostring(root, encoding='utf8').decode('utf8')
    except ET.ParseError:
        print("Błąd: Nieprawidłowy plik XML.")
        sys.exit(1)

# Funkcja do konwersji słownika na XML
def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, war in d.items():
        if isinstance(war, list):
            for sub_dict in war:
                child = dict_to_xml("FirmaElement", sub_dict) if key == "Firma" else dict_to_xml(key[:-1] + "y", sub_dict)
                elem.append(child)
        elif isinstance(war, dict):
            child = dict_to_xml(key, war)
            elem.append(child)
        else:
            child = ET.SubElement(elem, key)
            child.text = str(war)
    return elem

# Funkcja do zapisywania danych do pliku XML
def save_xml(data, file_path):
    try:
        if isinstance(data, dict):
            root_name = 'root'  
            root = dict_to_xml(root_name, data)
            data = ET.tostring(root, encoding='utf8').decode('utf8')
        
        dom = minidom.parseString(data)
        with open(file_path, 'w') as file:
            file.write(dom.toprettyxml())
        print(f"Dane zapisane do: {file_path}")
    except Exception as e:
        print(f"Błąd: {e}")
        sys.exit(1)

# Funkcja do konwersji danych pomiędzy formatami
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
        print("Format pliku -input- nieprawidłowy.")
        sys.exit(1)

    if output_ext == ".json":
        save_func = save_json
    elif output_ext == ".yml" or output_ext == ".yaml":
        save_func = save_yaml
    elif output_ext == ".xml":
        save_func = save_xml
    else:
        print("Format pliku -output- nieprawidłowy")
        sys.exit(1)

    data = load_func(input_file)
    save_func(data, output_file)

# Główna funkcja programu
if __name__ == "__main__":
    input_file, output_file = parse_arguments()
    convert_data(input_file, output_file)
