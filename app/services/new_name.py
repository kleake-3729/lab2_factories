import json
import os
from pathlib import Path
from sentence_transformers import SentenceTransformer

file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'emails.json')
model = SentenceTransformer('all-MiniLM-L6-v2')

def new_email_embeddings(file_path):
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
        
    
    emails = []
    embedding_list = []
    topic_embeddings = {}
    for item in data['saved_emails']:
            body = item['body']
            subject = item['subject']
            topic = item['topic']
            email_text = f"{subject} {body}"
            emails.append(email_text)
            embedding = model.encode(email_text, convert_to_numpy=True)
            embedding_list.append(embedding)
            topic_embeddings[topic] = embedding
    print(topic_embeddings)   
    return topic_embeddings

if __name__ == "__main__":
    new_email_embeddings(file_path)
