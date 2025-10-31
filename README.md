# 🚀 Multi-LLM Orchestration API  
### *AI Engineer Backend Task – OriMind Assignment*  

This project implements a **Multi-LLM Orchestration System** using **FastAPI** that automatically generates backend code from natural language prompts.  
It leverages **two language models** — one for code generation and another for refinement — to deliver clean, production-ready backend code in JSON format.  

---

## 🧠 Features  

✅ **Dual LLM Orchestration** — Uses GPT-2 for backend code generation and DistilGPT-2 for code refinement.  
⚙️ **FastAPI-based REST API** — Lightweight and high-performance Python web framework.  
🧩 **Structured JSON Responses** — Includes the final code output and process logs.  
🚀 **Deploy Anywhere** — Easily deploy on Render or Hugging Face Spaces (free tiers supported).  
🧠 **Extendable Design** — Can be integrated with OpenAI, Gemini, or Claude APIs for improved performance.  

---

## 🧰 Tech Stack  

| Component | Description |
|------------|-------------|
| **Language** | Python 3.10+ |
| **Framework** | FastAPI |
| **LLM 1** | GPT-2 (Code Generation) |
| **LLM 2** | DistilGPT-2 (Code Review & Refinement) |
| **Deployment** | Render / Hugging Face Spaces |
| **Libraries** | `transformers`, `torch`, `pydantic`, `uvicorn` |

---

## ⚙️ Setup Instructions  

Follow these steps to set up and run the project locally.  

---

### 🪜 Step 1: Clone the Repository  
```bash
git clone https://github.com/<your-username>/multi-llm-api.git
cd multi-llm-api
🪜 Step 2: Create a Virtual Environment
Create and activate a virtual environment for dependency management.


# Create environment
python -m venv venv
Activate the environment:


# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
🪜 Step 3: Install Dependencies
Install all the required libraries listed in requirements.txt.

pip install -r requirements.txt
If you don’t have requirements.txt yet, you can create one with:


pip install fastapi uvicorn transformers torch pydantic
pip freeze > requirements.txt
🪜 Step 4: Run the Application Locally
Start the FastAPI server using Uvicorn.


uvicorn main:app --reload

The server will start locally at:
👉 http://127.0.0.1:8000

You can explore and test all endpoints using the interactive documentation:
👉 http://127.0.0.1:8000/docs

🧩 API Endpoints
🔹 GET /
Description: Health check endpoint.

Example Request:


curl http://127.0.0.1:8000/


#Example Response:

json
{
  "message": "Free Multi-LLM API running successfully!"
}

🔹 POST /generate_backend

Description: Generates and refines backend code using two LLMs (GPT-2 & DistilGPT-2).
Request Example:
json
{
  "prompt": "Build a REST API for a blog app with users, posts, and comments."
}

Example using curl:

curl -X POST "http://127.0.0.1:8000/generate_backend" \
-H "Content-Type: application/json" \
-d "{\"prompt\": \"Build a REST API for a blog app with users, posts, and comments.\"}"

#Response Example:

json
{
  "status": "success",
  "code_sample": "from fastapi import FastAPI\napp = FastAPI()\n@app.get('/posts')...",
  "logs": [
    "GPT-2 generated initial backend code",
    "DistilGPT-2 reviewed and improved the code"
  ]
}

#🧠 Architecture Overview

┌─────────────────────────────┐
│  User Prompt (Natural Text) │
└───────────────┬─────────────┘
                │
                ▼
         ┌────────────┐
         │ GPT-2 (Generator) │
         └────────────┘
                │
                ▼
        ┌────────────────┐
        │ DistilGPT-2 (Reviewer) │
        └────────────────┘
                │
                ▼
        ┌─────────────────────────────┐
        │  Refined Code + Logs (JSON) │
        └─────────────────────────────┘


🚀 Deployment
You can deploy this API easily on:

🟢 Render
Create a free Render account → https://render.com

Click “New Web Service”

Connect your GitHub repo

Set the Start Command as:


uvicorn main:app --host 0.0.0.0 --port 10000

