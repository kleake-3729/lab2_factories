import json
import os
from pathlib import Path

email_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'emails.json')

def save_email(email_path, topic, subject, body):
    #Reading in existing json or creating a new object if unable to read file
    try:
        with open(email_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"saved_emails": []}
        
    except json.JSONDecodeError:
    # Handle case where file is empty or invalid JSON
        print(f"Error decoding JSON from file: {email_path}. Starting with empty object.")
        data = {"saved_emails": []}

    # Appending the saved emails list with new email
    data["saved_emails"].append({"topic":topic, "subject":subject, "body":body})
    
    with open(email_path, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"Your new email was appended to {email_path}")

#if __name__ == "__main__":
    #save_email(email_path, 'new', 'testing if this still works!', 'i really hope that this works!')