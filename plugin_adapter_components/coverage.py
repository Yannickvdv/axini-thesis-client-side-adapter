import os
import json
import time

def write_coverage(self, coverage_data):
    coverage_data = self.browser.execute_script('return window.__coverage__;')
    if coverage_data:
        json_data = json.dumps(coverage_data)
        timestamp = int(time.time())
        coverage_folder = get_coverage_folder()
        file_name = f"{coverage_folder}/coverage_{timestamp}.json"
        file = open(file_name, "w")
        file.write(json_data)


def get_coverage_folder(self):
    base_path = 'plugin_adapter_components/coverage_reports'
    # List all subdirectories in the base path
    subdirectories = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

    if not subdirectories:
        # If there are no existing folders, create the first one
        new_folder_name = "1"
    else:
        # Find the highest folder number and increment it
        number_directories = [int(d) for d in subdirectories if d.isdigit()]
        max_folder_number = max(number_directories) if len(number_directories) > 0 else 0 
        # max_folder_number = max([int(d) for d in subdirectories if d.isdigit()])
        new_folder_name = str(max_folder_number + 1)

    new_folder_path = os.path.join(base_path, new_folder_name)

    # Create the new folder
    os.mkdir(new_folder_path)

    return new_folder_path
