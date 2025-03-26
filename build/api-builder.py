import os
import json
import requests

import ClassDecorator

GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

# Load the event payload
with open(GITHUB_EVENT_PATH, "r") as event_file:
    event_data = json.load(event_file)

# Extract PR number and repo details
pr_number = event_data["pull_request"]["number"]
repo_full_name = event_data["repository"]["full_name"]

print(f"Processing PR #{pr_number} in repository {repo_full_name}")

# Fetch changed file from GitHub API
github_token = os.getenv("GITHUB_TOKEN")
headers = {"Autorization": f"token {github_token}"}
pr_files_url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files"

response = requests.get(pr_files_url, headers=headers)
pr_files = response.json()

# Load and update api.json
api_json_path = "build/api.json"
if os.path.exists(api_json_path):
    print(f"{api_json_path} is valid!")
    with open(api_json_path, "r") as json_file:
        api_data = json.load(json_file)
else:
    print(f"{api_json_path} is invalid!")
    api_data = {}


print("Files changed in this PR:")
for file in pr_files:
    print(f"- {file['filename']}")
    if '.nlvm' in file['filename']:
        print("NLVM file found")

        def findIndexOfType(haystack: list[any], type: any) -> int:
            index = 0
            for item in haystack:
                if item[ClassDecorator.JSON_TAG_TYPENAME] == type:
                    return index
                index += 1
            return -1

        status = file['status']
        if status == 'added' or status == 'modified':
            class_json = ClassDecorator.ClassDecorator(file['filename']).decorate()
            #print(f"Generated data {json.dumps(class_json, indent=2)}")

            type_index = findIndexOfType(api_data['classes'], class_json[ClassDecorator.JSON_TAG_TYPENAME])
            if type_index < 0: # Not found
                print(f"{class_json[ClassDecorator.JSON_TAG_TYPENAME]} not found in api, creating new index!")
                api_data['classes'].append(class_json)
            else: # Found
                print(f"{class_json[ClassDecorator.JSON_TAG_TYPENAME]} found in api, updating entry!")
                api_data['classes'][type_index] = class_json

        elif status == 'removed':
            class_json = ClassDecorator.ClassDecorator(file['filename']).decorate()
            #print(f"Generated data {json.dumps(class_json, indent=2)}")

            type_index = findIndexOfType(api_data['classes'], class_json[ClassDecorator.JSON_TAG_TYPENAME])
            if type_index < 0:
                print(f"{class_json[ClassDecorator.JSON_TAG_TYPENAME]} not found in api, unable to remove!")
            else:
                print(f"{class_json[ClassDecorator.JSON_TAG_TYPENAME]} found in api, removing!")
                api_data['classes'].pop(type_index, None)



# Modify the set the new data
with open(api_json_path, "w") as json_file:
    json.dump(api_data, json_file, indent=4)

print("Updated api.json file successfully")