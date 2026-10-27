# CaseForge AI — AI QA Testing Assistant
> Built by a QA Engineer, for QA Engineers. Turn any requirement into test cases, edge cases, and Postman collections in 10 seconds.

[CaseForge](https://img.shields.io/badge/Status-Live-brightgreen) [FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688) [Next.js](https://img.shields.io/badge/Frontend-Next.js-black) [OpenAI](https://img.shields.io/badge/AI-GPT--4o-8A2BE2)

**Live Demo:** [caseforge-ai.vercel.app](https://caseforge-ai.vercel.app)  
**App Prototype:** Real backend-connected version  
**Tech Stack:** Next.js 14, FastAPI, OpenAI GPT-4o-mini, Jira REST API, Postman Collection v2.1, GitHub Apps

---

### 🚀 Why This Project Stands Out

Most junior portfolios have todo-apps. **Very few build developer tools.**

CaseForge proves 4 rare skills in one project:
1. **QA Depth** — Boundary, security, concurrency, i18n edge cases juniors miss
2. **AI Engineering** — Structured JSON output, prompt orchestration, mock fallback
3. **API Integration** — Jira, Postman, GitHub real-world workflows
4. **Product Thinking** — Built for actual dev workflow, not just a demo

### ✨ 6 Core Modules

| Module | Input | Output | Why It's Special |
|--------|-------|--------|------------------|
| **Requirement → Test Cases** | PRD / Jira ticket | 12 test cases (ID, Title, Steps, Expected, Priority, Type) | Includes 3+ edge cases |
| **Edge Case Detector** | Requirement | Categorized risks: Boundary, Null, Security, Concurrency, Time, i18n | The module that impresses seniors |
| **User Story → Scenarios** | As a... I want... | BDD Gherkin Given/When/Then | Happy + Alternate + Negative paths |
| **Bug Report Builder** | Plain English bug | Professional Jira-ready report + Jira API payload | Title, Severity, Steps, Expected vs Actual |
| **API Test Suggester** | OpenAPI / cURL | Postman Collection with pm.test() assertions + security tests | Happy, 401, 403, 422, SQLi, XSS |
| **Regression Suite Builder** | Git diff / PR link | Must Test vs Can Skip + Risk Score | Uses changed files to prioritize |

### 🏗️ Architecture

```
User Input (Jira / Requirement / OpenAPI / GitHub PR)
        ↓
FastAPI (main.py) — 6 endpoints
        ↓
LLM Service (llm_service.py) — 6 specialized prompts with SYSTEM QA persona
        ↓
Formatters: Postman Generator, Jira Payload Builder
        ↓
Frontend: Next.js + Integrated App (calls /api/*)
        ↓
Exports: CSV, Postman JSON, Jira Issue, GitHub PR Comment
```

See `architecture.png` for visual diagram.

### 🔌 Integrations

**Jira:** OAuth + REST API — Pull issue → Generate tests → Create sub-tasks
```python
POST /api/jira/push?issue_key=PROJ-123
```

**Postman:** Generates valid Collection v2.1 JSON — 1-click Import
```json
{
  "info": { "name": "CaseForge AI - 2024-10-27", "schema": "..." },
  "item": [{ "name": "Happy - Send OTP", "request": {...}, "event": [...] }]
}
```

**GitHub:** Paste PR URL → Analyzes diff → Suggests regression suite → Comment on PR (via GitHub Apps)

### 🛠️ Quick Start

**Backend (2 min):**
```bash
cd caseforge-backend
pip install -r requirements.txt
cp .env.example .env
# Add OPENAI_API_KEY (optional - mock mode works without it)
uvicorn main:app --reload --port 8000
# Docs: http://localhost:8000/docs
```

**Frontend (Vercel):**
```bash
# Landing page + App are in /frontend
# Deploy to Vercel, set env:
NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

**Deploy:**
- Backend: Render.com → Build: pip install -r requirements.txt, Start: uvicorn main:app --host 0.0.0.0 --port $PORT
- Frontend: Vercel → Import GitHub repo

### 🧠 Prompt Engineering Highlight

Each module uses a senior QA system persona + forced JSON output:

```python
SYSTEM = "You are CaseForge AI, Senior QA with 10+ years..."
PROMPT = "Generate 10-12 test cases as JSON array... Include at least 3 edge cases juniors miss..."
response_format={"type":"json_object"}
```

Mock fallback ensures demo works without API key — critical for portfolio.

### 📸 Demo Flow (For README GIF)

1. Paste Jira ticket: "Users reset password via email OTP valid 10 mins"
2. Click Generate → Get 6 test cases including "OTP at 9:59 vs 10:01 boundary" and "+ alias email"
3. Click Export Postman → Import into Postman → Run
4. Click Push to Jira → Test cases appear as sub-tasks

### 📝 LinkedIn Launch Post

```
🚀 I built CaseForge AI — An AI QA Assistant that turns requirements into test cases in 10 seconds.

As a QA Engineer, I was tired of:
- Writing the same test cases manually
- Edge cases slipping to production
- Jira bugs with "it doesn't work" and no repro steps

So I built the tool I wished I had:

✅ Paste any requirement → Get 12 test cases (functional + boundary + security)
✅ Edge Case Detector — Finds the +alias emails, 9:59 vs 10:01 OTP expiry, race conditions juniors miss
✅ User Story → BDD Gherkin scenarios
✅ Bug description → Professional Jira-ready report
✅ Swagger / cURL → Full Postman collection with pm.test() + security tests
✅ GitHub PR → Smart regression suite (Must Test vs Can Skip)

Tech: Next.js, FastAPI, OpenAI, Jira API, Postman Collection v2.1, GitHub Apps

🔗 Live Demo: [your link]
💻 GitHub: [your repo]
🎨 Why dev tools? Very few juniors build tools FOR developers — this is how you stand out.

Open to feedback from Senior QAs — what edge case would you add?

#QA #QualityAssurance #AI #OpenAI #Testing #DeveloperTools #FastAPI #NextJS
```

### 🤝 Future Roadmap

- [ ] Chrome Extension — Generate tests on any Jira page
- [ ] TestRail / Zephyr direct push
- [ ] Fine-tuned model on 10k real bug reports
- [ ] Slack bot: @caseforge generate tests for this ticket

### 👨‍💻 Author

Built by Sulyman Hammed — QA Engineer turning manual expertise into AI tooling.

**License:** MIT — Use it, break it, improve it.
