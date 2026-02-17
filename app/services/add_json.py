import json
from pathlib import Path

file_path = '/home/ec2-user/environment/kl_lab2/lab2_factories/data/test_topic.json'

def new_topic_to_json(file_path, new_topic, desc):
    #Reading in existing json or creating a new object if unable to read file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}
        
    except json.JSONDecodeError:
    # Handle case where file is empty or invalid JSON
        print(f"Error decoding JSON from file: {file_path}. Starting with empty object.")
        data = {}

    # Adding in new topic if it doesn't exist
    if new_topic not in data:
        data[new_topic] = {"description": desc}
    
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        print(f"Key '{new_topic}' with value '{desc}' appended to {file_path}")
        
    # Prevents topic already in file from being readded
    else:
        print(f"Key '{new_topic}' already exists. No changes made.")

if __name__ == "__main__":
    new_topic_to_json(file_path, 'test', 'testing if this still works')


    