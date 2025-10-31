import os
import json
import time
from typing import Dict, Any
import openai
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# For Vertex AI (Google Gemini), we will use google.cloud.aiplatform.gapic
# This example uses a simplified call pattern — adapt if using a different client library.
from google.cloud import aiplatform
from google.oauth2 import service_account

from .config import OPENAI_API_KEY, GOOGLE_CREDENTIALS, MAX_RETRIES

openai.api_key = OPENAI_API_KEY

# -------- OpenAI ChatGPT wrapper --------
@retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=1, min=1, max=10))
def chatgpt_generate(prompt: str, system: str = "You are a helpful assistant", max_tokens: int = 1200) -> Dict[str, Any]:
    """
    Use OpenAI ChatCompletion (chat GPT) to generate code or suggestions.
    Returns dict with keys: text, usage (tokens), raw
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",  # change to an available model or user choice
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.2,
        )
        text = ""
        if "choices" in response and len(response.choices) > 0:
            text = response.choices[0].message.content
        usage = response.get("usage", {})
        return {"text": text, "usage": usage, "raw": response}
    except Exception as e:
        # tenacity will retry
        raise

# -------- Gemini (Vertex AI) wrapper --------
@retry(stop=stop_after_attempt(MAX_RETRIES), wait=wait_exponential(multiplier=1, min=1, max=10), retry=retry_if_exception_type(Exception))
def gemini_review(prompt: str, model: str = "projects/your-project/locations/us-central1/publishers/google/models/text-bison@001", max_output_tokens: int = 1024) -> Dict[str, Any]:
    """
    An example review call to Google Vertex AI (Gemini-like). 
    Replace model with appropriate model resource name if needed.
    This code assumes GOOGLE_APPLICATION_CREDENTIALS is set.
    """
    try:
        # initialize if not already configured
        if GOOGLE_CREDENTIALS:
            creds = service_account.Credentials.from_service_account_file(GOOGLE_CREDENTIALS)
            client_options = {}
        else:
            creds = None
            client_options = {}

        aiplatform.init()

        # Use Vertex AI text generation for review — pseudo-call here; adjust per SDK
        client = aiplatform.gapic.PredictionServiceClient()
        # Resource name for endpoint/model (user must replace below with correct endpoint or model path)
        # This is an illustrative payload. Replace with valid endpoint and request for your setup.
        endpoint = model
        instance = {"content": prompt}
        instances = [instance]

        # If you have an endpoint: call client.predict(endpoint=endpoint,...)
        # Here: attempt to call a general predict method. Adjust in your environment.
        response = client.predict(endpoint=endpoint, instances=instances)
        # response predictions might be a list
        text = ""
        if response.predictions:
            # Convert first prediction to str
            text = json.dumps(response.predictions[0])
        # We cannot get token usage easily from Vertex in the same field; record placeholder.
        usage = {"tokens": None}
        return {"text": text, "usage": usage, "raw": response}
    except Exception as e:
        raise
