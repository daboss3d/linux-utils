# general purpose tools for save , load, update file settings.json

'''
directories {
   "ai": "",
   "utils":""
}
'''



import os
import json


def save_settings(settings_dict, filepath):
    """
    Saves a dictionary of settings to a JSON file.

    Args:
        settings_dict (dict): The dictionary of settings to save.
        filepath (str): The path to the JSON file.
    """
    try:
        with open(filepath, 'w') as f:
            json.dump(settings_dict, f, indent=4)
        print(f"Settings saved successfully to {filepath}")
    except IOError as e:
        print(f"Error saving settings to {filepath}: {e}")


def load_settings(filepath):
    """
    Loads a dictionary from a JSON file.

    Args:
        filepath (str): The path to the JSON file containing the settings.

    Returns:
        dict: A dictionary containing the settings loaded
              from the file or None if file not found.
              Returns an empty dict if fails to parse JSON.
    """
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)  # loading and parsing into a dict here!
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        # Returning None if file not found or cannot decode JSON.
        return {}

def _recursive_update(target_dict, source_dict):
    """
    Recursively updates a dictionary with values from another dictionary.

    Args:
        target_dict (dict): The dictionary to be updated.
        source_dict (dict): The dictionary containing the new values.
    """
    for key, value in source_dict.items():
        if isinstance(value, dict) and key in target_dict and isinstance(target_dict[key], dict):
            # If both values are dictionaries, recurse
            _recursive_update(target_dict[key], value)
        else:
            # Otherwise, update or add the key-value pair
            target_dict[key] = value

def update_settings2(settings_dict, new_settings, filepath):
    """
    
 Updates a dictionary of settings with new values and saves it back to the JSON file.
    
    Args:
        settings_dict (dict): The current dictionary of settings.
        new_settings (dict): A dictionary containing the new settings to apply.
        filepath (str): The path where the updated JSON file will be saved.
        
    Returns:
        None
    """
    for key, value in new_settings.items():
        if key in settings_dict:
            settings_dict[key] = value

    save_settings(settings_dict, filepath)

def update_settings(settings_dict, new_settings, filepath):
    """
    Updates a dictionary of settings with new values (including nested keys)
    and saves it back to the JSON file.

    Args:
        settings_dict (dict): The current dictionary of settings.
        new_settings (dict): A dictionary containing the new settings to apply.
        filepath (str): The path where the updated JSON file will be saved.

    Returns:
        None
    """
    _recursive_update(settings_dict, new_settings)
    save_settings(settings_dict, filepath)


def get_cwd():
    return os.path.dirname(os.path.realpath(__file__))


def get_parent_directory(path, target_dir_name):
    """
    Gets the parent directory of a given path that matches a specific directory name.

    Args:
        path (str): The input path.
        target_dir_name (str): The name of the target directory to find.

    Returns:
        str or None: The path to the target parent directory, or None if not found.
    """
    current_path = path
    while current_path and current_path != os.path.dirname(current_path):
        # Get the last component of the path
        head, tail = os.path.split(current_path)
        if tail == target_dir_name:
            return current_path  # We found the target directory itself
        
        # If the head is empty and tail is not the target, then it's a file in the root
        if not head and tail != target_dir_name:
            return None # Reached the root without finding the target

        # Move up to the parent directory
        current_path = head
        
        # Check if the current_path (which is now a parent directory) is the target_dir_name
        # This handles cases like 'c:/temp/files' where 'files' is the target
        if os.path.basename(current_path) == target_dir_name:
            return current_path

    return None

def create_new_settings():
    print("Creating new settings ...")
    # create a new setting
    cwd = get_cwd()

    ai_path =get_parent_directory(cwd, 'ai')
    # Default values can be initialized here to avoid issues with empty dictionary
    default_values = {'directories': {"cwd": cwd, "utils": "", "ai": ai_path, "models":""}}
    current_settings.update(default_values)  # Update with defaults

# usage
settings_path = 'path/to/settings.json'
current_settings = {}

def test_update_settings():
    print("[test] Settings ---------------------------------------------------")
    print( json.dumps(load_settings(settings_path), indent=4))
    # Updating the settings. Please ensure 'new_values' contains valid keys.
    new_values = {"directories": { "models": 350 } }
    print(f"New values to be updated: {new_values}")
    update_settings(current_settings, new_values, settings_path)   # Update function call
    print("[test] Updating Settings ---------------------------------------------------")
    print(json.dumps(current_settings, indent=4))

if __name__ == "__main__":

    # Load current settings
    cwd = get_cwd()
    settings_path = os.path.join(cwd, 'settings.json')

    print(f"Loaded Settings Path: {settings_path}")
    current_settings = load_settings(settings_path) or {}

    if not current_settings:
        create_new_settings()
    else :
        print("Found settings ...")

    test_update_settings()



        


 