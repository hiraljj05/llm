from typing import Dict, Any, List
from pathlib import Path
import textwrap

from .llm_clients import chatgpt_generate, gemini_review
from .utils import safe_parse_python, write_project_files, new_project_folder, make_zip

def build_prompts(user_prompt: str) -> Dict[str, str]:
    """
    Create specialized prompts for generator and reviewer.
    """
    generator_prompt = textwrap.dedent(f"""
    You are an expert backend engineer. Generate a complete FastAPI-based backend project for the following request.
    Please include:
    - project structure
    - models (Pydantic models / SQLAlchemy models)
    - routes (CRUD endpoints)
    - authentication (JWT or simple token)
    - main application file with dependency wiring
    - requirements.txt content
    Return only the code blocks and filenames in a JSON object of the form:
    {{
      "files": {{
        "path/to/file.py": "file contents",
        ...
      }},
      "notes": "short explanation"
    }}
    Request: {user_prompt}
    """).strip()

    reviewer_prompt = textwrap.dedent(f"""
    You are a senior backend engineer / code reviewer. The following is the generated project (JSON with files).
    Please:
    - point out obvious issues
    - propose fixes (provide replacement files or modifications)
    - add error handling and input validation improvements
    - ensure syntax correctness
    - return a merged JSON with 'files' updated where you propose changes and a 'review_notes' field.
    Input: {{generated_json}}
    """).strip()

    return {"generator": generator_prompt, "reviewer": reviewer_prompt}

def orchestrate_generation(user_prompt: str, max_gen_tokens: int = 1200) -> Dict[str, Any]:
    logs: List[str] = []
    cost_log: List[Dict[str, Any]] = []
    files: Dict[str, str] = {}

    # 1) Build prompts
    prompts = build_prompts(user_prompt)

    # 2) Ask ChatGPT (generator)
    gen_resp = chatgpt_generate(prompts["generator"], max_tokens=max_gen_tokens)
    logs.append("ChatGPT generated initial project JSON")
    cost_log.append({"provider": "openai", "usage": gen_resp.get("usage")})

    # parse ChatGPT response: expect JSON with files
    import json
    try:
        generated_json = json.loads(gen_resp["text"])
        gen_files = generated_json.get("files", {})
        files.update(gen_files)
    except Exception:
        # fallback: try to extract JSON object anywhere in the text
        import re
        m = re.search(r"\{.*\}", gen_resp["text"], flags=re.DOTALL)
        if m:
            try:
                generated_json = json.loads(m.group(0))
                files.update(generated_json.get("files", {}))
            except Exception:
                # if can't parse, put entire response into a single file
                files["GENERATED_BY_CHATGPT.txt"] = gen_resp["text"]
        else:
            files["GENERATED_BY_CHATGPT.txt"] = gen_resp["text"]

    # 3) Ask Gemini to review and improve
    # Provide the generated JSON to the reviewer prompt by replacing placeholder
    reviewer_prompt = prompts["reviewer"].replace("{generated_json}", json.dumps({"files": files}, indent=2))
    review_resp = gemini_review(reviewer_prompt)
    logs.append("Gemini reviewed and proposed improvements")
    cost_log.append({"provider": "gemini", "usage": review_resp.get("usage")})

    # Attempt to parse Gemini response as JSON with 'files' and 'review_notes'
    try:
        review_json = json.loads(review_resp["text"])
        reviewed_files = review_json.get("files", {})
        # Merge: reviewed files replace or augment original
        files.update(reviewed_files)
        review_notes = review_json.get("review_notes", "")
    except Exception:
        # If parsing fails, create a review note file
        files["REVIEW_BY_GEMINI.txt"] = review_resp["text"]
        review_notes = "Gemini response could not be parsed as JSON. See REVIEW_BY_GEMINI.txt."

    # 4) Validate Python files for syntax and keep a validation report
    validation = {}
    for path, content in list(files.items()):
        if path.endswith(".py"):
            valid, err = safe_parse_python(content)
            validation[path] = {"valid": valid, "error": err}
            if not valid:
                logs.append(f"Syntax error detected in {path}: {err}")

    # 5) Create project folder and write files
    folder = new_project_folder("generated_backend")
    write_project_files(folder, files)
    logs.append(f"Project files written to {str(folder)}")

    # 6) Make zip
    zip_path = folder.with_suffix(".zip")
    make_zip(folder, zip_path)
    logs.append(f"Project zipped at {str(zip_path)}")

    # 7) Prepare code sample to return (e.g., main.py or README excerpt)
    code_sample = files.get("app/main.py") or files.get("main.py") or next(iter(files.values()), "")[:2000]

    # 8) Return assembled response
    return {
        "status": "success",
        "code_sample": code_sample,
        "generated_folder": str(folder),
        "zip_path": str(zip_path),
        "logs": logs,
        "validation": validation,
        "costs": cost_log,
        "review_notes": review_notes if 'review_notes' in locals() else ""
    }
