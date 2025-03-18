import os
import json
import xml.etree.ElementTree as ET

extracted_xml = ""
script_package = ""
included_libraries = []

store_next_line = False

temp_path = os.path.join(os.path.dirname(__file__), "../scripts/core/Behaviour.nlvm")
if os.path.exists(temp_path):
    with open(temp_path, "r") as my_file:
        for line in my_file:
            if "///" in line: # Find all xml tags
                extracted_xml += line.replace('///', '')
                store_next_line = True
                continue
            elif "package" in line: # Find package line
                script_package = line.replace("package", '').strip()
            elif "import" in line: # Find libraries
                included_libraries.append(line.replace("import", '').strip())

            if store_next_line: # Store the code line in the xml for use later
                extracted_xml += f"<data>{line}</data>"
                store_next_line = False

        # Create json information
    root = ET.fromstring(extracted_xml)
    print(extracted_xml)
else:
    print(f"Not a valid path {temp_path}")