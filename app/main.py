from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import time

app = FastAPI(title="Multi-LLM Orchestration API")

# Load two LLMs (both free and good for code tasks)
generator = pipeline("text-generation", model="microsoft/phi-2")
reviewer = pipeline("text-generation", model="Salesforce/codegen-350M-mono")

# Request model
class PromptRequest(BaseModel):
    prompt: str

@app.get("/")
def read_root():
    return {"message": "Free Multi-LLM Orchestration API running successfully!"}

@app.post("/generate_backend")
def generate_backend(request: PromptRequest):
    try:
        logs = []
        start_time = time.time()

        # Step 1: LLM 1 generates backend code
        logs.append("Microsoft Phi-2 generating initial backend code...")
        gen_result = generator(request.prompt, max_new_tokens=256, temperature=0.7, truncation=True)
        initial_code = gen_result[0]["generated_text"]

        # Step 2: LLM 2 reviews/improves the code
        logs.append("Salesforce CodeGen reviewing and improving the code...")
        review_prompt = f"Improve and clean up this backend code for production quality:\n\n{initial_code}"
        review_result = reviewer(review_prompt, max_new_tokens=256, temperature=0.6, truncation=True)
        improved_code = review_result[0]["generated_text"]

        # Step 3: Collect logs and return result
        end_time = time.time()
        logs.append(f"Total processing time: {end_time - start_time:.2f} seconds")

        return {
            "status": "success",
            "code_sample": improved_code,
            "logs": logs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
