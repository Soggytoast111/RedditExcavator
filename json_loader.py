import json

def load_json(file_name):
    try:
        with open(file_name, 'r') as file:
            loaded_data = json.load(file)
        
        return loaded_data

    except FileNotFoundError:
        print("Error: The file 'data.json' was not found.")
    except json.JSONDecodeError:
        print("Error: Could not decode JSON from the file.")