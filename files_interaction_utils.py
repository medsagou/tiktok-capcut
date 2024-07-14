import os
import random

def remove_file(file_path):
    os.remove(file_path)
    print(f"Removed {file_path}")


def get_first_element_path(directory):
    # List all items in the specified directory
    items = os.listdir(directory)
    
    # Iterate through the items
    for item in items:
        # Construct the full path
        item_path = os.path.join(directory, item)
        # Check if it's a file and doesn't contain a bracket
        if os.path.isfile(item_path) and 'THIsMineDontTakeitPLease' not in item:
            return item_path
    
    # If no suitable item is found, return None
    return None
    

def get_random_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    if lines:
        random_line = random.choice(lines).strip()
        return random_line
    else:
        return None
    

def get_file_content(file_path):
    with open(file_path, 'r') as file:
        return file.read().replace('\n', '').replace('\r', '')
    

def add_bracket_to_filename(file_path):
    # Get the directory and the base name of the file
    directory, original_name = os.path.split(file_path)
    
    # Add the closing bracket to the base name before the file extension
    name, extension = os.path.splitext(original_name)
    new_name = f"{name}THIsMineDontTakeitPLease{extension}"
    
    # Construct the new file path
    new_file_path = os.path.join(directory, new_name)
    
    # Rename the file
    os.rename(file_path, new_file_path)
    return new_file_path
    

# add_bracket_to_filename(get_first_element_path(os.getcwd() + "\\videos\\"))
# print(get_first_element_path(os.getcwd() + "\\videos\\"))

def add_text_to_file(file_path, text):
    with open(file_path, 'a') as file:
        # Append text to the file
        file.write(text + '\n')