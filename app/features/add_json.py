import json
import os

def add_new_topic(filename='test_topic.json'):
    """
    Prompts the user for a new topic and description, then adds it to a JSON file.
    """
    # 1. Get user input
    new_topic_name = input("Enter the new topic name: ")
    new_description = input("Enter the topic description: ")

    new_entry = {
        "topic": new_topic_name,
        "description": new_description
    }

    data = []
    # 2. Read existing data
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode existing data from {filename}. Starting with fresh list.")

    # 3. Append the new entry
    if isinstance(data, list):
        data.append(new_entry)
    else:
        print(f"Error: JSON file does not contain a list. Cannot append.")
        return

    # 4. Write the updated data back to the file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Successfully added '{new_topic_name}' to {filename}.")

if __name__ == "__main__":
    add_new_topic()

    