import os
import json
import numpy as np
from typing import Dict, Any, List
from sentence_transformers import SentenceTransformer
from app.features.generators import EmailEmbeddingsFeatureGenerator
from app.dataclasses import Email

def similar_email(message): 
    
    email = Email(subject=message.subject, body=message.body)
    
    EmailEmbeddingsFeatureGenerator.generate_features(email)

if __name__ == "__main__":
    similar_email({"subject": "curling is cool",
            "body": "the us womens team is doing awesome at curling right now"})