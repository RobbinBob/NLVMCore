import os
import json
import xml
import requests

GITHUB_EVENT_PATH = os.getenv("GITHUB_EVENT_PATH")

# Load the event payload
with open(GITHUB_EVENT_PATH, "r") as event_file:
    event_data = json.load(event_file)

# Extract PR number and repo details
pr_number = event_data["pull_request"]["number"]
repo_full_name = event_data["repository"["full_name"]]

print(f"Processing PR #{pr_number} in repository {repo_full_name}")

# Fetch changed file from GitHub API
github_token = os.getenv("GITHUB_TOKEN")
headers = {"Autorization": f"token {github_token}"}
pr_files_url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}/files"

response = requests.get(pr_files_url, headers=headers)
pr_files = response.json()

print("Filed changed in this PR:")
for file in pr_files:
    print(f"- {file['filename']}")

# Load and update api.json
api_json_path = "build/api.json"
if os.path.exists(api_json_path):
    with open(api_json_path, "r") as json_file:
        api_data = json.load(json_file)
else:
    api_data = {}


### MODIFY JSON OBJECT HERE

### -----------------------

# Modify the set the new data
with open(api_json_path, "w") as json_file:
    json.dump(api_data, json_file, indent=4)

print("Updated api.json file successfully")