
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from services.llm_service import LLMService
from services.postman_generator import generate_postman_collection
from services.jira_service import format_jira_payload

app = FastAPI(
    title="CaseForge AI API",
    description="AI QA Testing Assistant - Generates test cases, edge cases, bug reports, API tests",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm = LLMService()

class RequirementInput(BaseModel):
    requirement: str
    context: Optional[str] = None
    project_type: Optional[str] = "web"

class BugInput(BaseModel):
    bug_description: str
    environment: Optional[str] = "Chrome, Production"

class APIInput(BaseModel):
    spec: str
    base_url: Optional[str] = "https://api.example.com"

class RegressionInput(BaseModel):
    pr_url: Optional[str] = None
    diff: Optional[str] = None
    changed_files: Optional[List[str]] = None

@app.get("/")
def health():
    return {"status": "CaseForge AI API running", "name": "CaseForge", "version": "1.0.0", "mock_mode": llm.use_mock}

@app.post("/api/generate-test-cases")
async def generate_test_cases(data: RequirementInput):
    result = await llm.generate_test_cases(data.requirement, data.context)
    return result

@app.post("/api/detect-edge-cases")
async def detect_edge_cases(data: RequirementInput):
    result = await llm.detect_edge_cases(data.requirement, data.context)
    return result

@app.post("/api/user-story-to-scenarios")
async def user_story_to_scenarios(data: RequirementInput):
    result = await llm.story_to_gherkin(data.requirement)
    return result

@app.post("/api/generate-bug-report")
async def generate_bug_report(data: BugInput):
    result = await llm.generate_bug_report(data.bug_description, data.environment)
    jira_payload = format_jira_payload(result)
    return {"bug_report": result, "jira_payload": jira_payload}

@app.post("/api/suggest-api-tests")
async def suggest_api_tests(data: APIInput):
    tests = await llm.generate_api_tests(data.spec)
    postman_collection = generate_postman_collection(data.spec, tests, data.base_url)
    return {"api_tests": tests, "postman_collection": postman_collection}

@app.post("/api/build-regression-suite")
async def build_regression_suite(data: RegressionInput):
    result = await llm.build_regression_suite(data.diff, data.changed_files, data.pr_url)
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
