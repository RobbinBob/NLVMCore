import json
import os

import ClassDecorator

api_data = {'classes': []}

failed_files = []

def iterate_folder(folder_path: str):
    successful_entries = 0
    failed_entries = 0
    total_entries = 0

    for file in os.listdir(folder_path):
        os.chdir(folder_path)
        filename = os.fsdecode(file)
        filepath = os.getcwd() + '\\' + filename

        if os.path.isfile(filepath) and '.nlvm' in filename:
            total_entries += 1

            decorator = ClassDecorator.ClassDecorator(filepath)
            json = {}
            try:
                json = decorator.decorate()
                if json is None:
                    raise Exception("No json found")
                if "ignore_api" in json and json['ignore_api'] == 'true':
                    print(f"ignored {filename}")
                    continue

            except Exception as e:
                print(f"Failed to parse NLVM file {filename} : {e}")
                failed_entries += 1
                failed_files.append(filename)
                continue
            api_data['classes'].append(json)
            successful_entries += 1

        
        if os.path.isdir(filepath):
            print(f"folder found iterating over it {filepath}")
            iterate_folder(filepath)
    
    return successful_entries, failed_entries, total_entries

os.chdir(os.path.dirname(__file__))
os.chdir("..")
folder_path = os.getcwd() + "\\scripts"
successful_entries, failed_entries, total_entries = iterate_folder(folder_path)

print(f"Generated API entries: {len(api_data['classes'])}")
print(f"Success ratio {successful_entries}/{total_entries} : {successful_entries / total_entries}")
print(f"Failed files: {failed_files}")

with open(os.path.dirname(__file__) + "\\generated_api.json", "w") as file:
    json.dump(api_data, file, indent=4)
