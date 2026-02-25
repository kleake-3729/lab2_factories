from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.email_topic_inference import EmailTopicInferenceService
from app.services.new_email_topics import NewEmailTopicInferenceService
from app.dataclasses import Email
from app.services import add_json
from app.services import save_emails
import os

router = APIRouter()


email_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'emails.json')

file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'topic_keywords.json')

class EmailRequest(BaseModel):
    subject: str
    body: str
    
class NewTopic(BaseModel):
    topic: str
    description: str

class EmailWithTopicRequest(BaseModel):
    subject: str
    body: str
    topic: str

class EmailClassificationResponse(BaseModel):
    predicted_topic: str
    topic_scores: Dict[str, float]
    features: Dict[str, Any]
    available_topics: List[str]

class EmailAddResponse(BaseModel):
    message: str
    email_id: int

@router.post("/emails/classify", response_model=EmailClassificationResponse)
async def new_classify_email(request: EmailRequest):
    try:
        new_inference_service = NewEmailTopicInferenceService()
        inference_service = EmailTopicInferenceService()
        email = Email(subject=request.subject, body=request.body)
        new_result = new_inference_service.classify_email(email)
        old_result = inference_service.classify_email(email)
        max_new = max(new_result["topic_scores"].items(), key=lambda item: item[1])
        max_old = max(old_result["topic_scores"].items(), key=lambda item: item[1])
        
        if max_new[1] > max_old[1]: 
        
        
            return EmailClassificationResponse(
                predicted_topic=new_result["predicted_topic"],
                topic_scores=new_result["topic_scores"],
                features=new_result["features"],
                available_topics=new_result["available_topics"]
                
                )
        else: 
            return EmailClassificationResponse(
                predicted_topic=old_result["predicted_topic"],
                topic_scores=old_result["topic_scores"],
                features=old_result["features"],
                available_topics=old_result["available_topics"]
                
                )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.post("/emails")

async def save_email(request: EmailWithTopicRequest):
    try:
        save_emails.save_email(email_path, request.topic, request.subject, request.body)
        
        return "Success! You have saved your new email!"
        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        
@router.post("/topics")

async def new_topic_to_json(request: NewTopic):
    try:
        inference_service = EmailTopicInferenceService()
        info = inference_service.get_pipeline_info()
        add_json.new_topic_to_json(file_path, request.topic, request.description)
        
        return "Success! Please check the GET topics endpoint to see your new topic!"
        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/topics")
async def topics():
    """Get available email topics"""
    inference_service = EmailTopicInferenceService()
    info = inference_service.get_pipeline_info()
    return {"topics": info["available_topics"]}

@router.get("/pipeline/info") 
async def pipeline_info():
    inference_service = EmailTopicInferenceService()
    return inference_service.get_pipeline_info()

# TODO: LAB ASSIGNMENT - Part 2 of 2  
# Create a GET endpoint at "/features" that returns information about all feature generators
# available in the system.
#
# Requirements:
# 1. Create a GET endpoint at "/features"
# 2. Import FeatureGeneratorFactory from app.features.factory
# 3. Use FeatureGeneratorFactory.get_available_generators() to get generator info
# 4. Return a JSON response with the available generators and their feature names
# 5. Handle any exceptions with appropriate HTTP error responses
#
# Expected response format:
# {
#   "available_generators": [
#     {
#       "name": "spam",
#       "features": ["has_spam_words"]
#     },
#     ...
#   ]
# }
#
# Hint: Look at the existing endpoints above for patterns on error handling
# Hint: You may need to instantiate generators to get their feature names

