
import os, json
from typing import List

SYSTEM = """You are CaseForge AI, a Senior QA Engineer with 10+ years in manual, automation, and security testing.
You think like a breaker - boundaries, nulls, race conditions, auth bypass, production edge cases."""

PROMPTS = {
"test_cases": """Requirement: {requirement}
Context: {context}
Generate 10-12 test cases as JSON array. Each: {{"id":"TC_001","title":"","type":"functional|boundary|negative|security|usability","priority":"P0|P1|P2","precondition":"","steps":["step"],"expected_result":"","edge_case_rationale":""}}
Include at least 3 edge cases juniors miss. Return ONLY valid JSON array.""",
"edge_cases": """Analyze requirement and list non-obvious edge cases.
Requirement: {requirement}
Return JSON: {{"categories": [{{"category":"Boundary","cases":[{{"case":"", "risk":"High|Medium|Low","why_it_matters":""}}]}}]}}
Categories: Boundary, Null/Empty, Security, Concurrency, Time/Timezone, i18n/Unicode, Performance, Integration
Return ONLY JSON.""",
"gherkin": """Convert user story to BDD Gherkin.
Story: {requirement}
Return JSON: {{"feature":"","background":"","scenarios":[{{"name":"","type":"happy|alternate|negative","gherkin":"Given...\nWhen...\nThen..."}}]}}
Return ONLY JSON.""",
"bug_report": """Create professional bug report.
Bug: {bug}
Env: {env}
Return JSON: {{"title":"","severity":"Critical|Major|Minor","priority":"P0|P1|P2","environment":"","steps_to_reproduce":[""],"expected_vs_actual":{{"expected":"","actual":""}},"logs_hint":"","suggested_labels":[],"suggested_assignee_role":""}}
Return ONLY JSON.""",
"api_tests": """Generate API test cases for Spec: {spec}
Return JSON array: [{{"test_name":"","method":"GET|POST","endpoint":"","payload":{{}},"assertions":["status == 200"],"type":"happy|negative|security|boundary"}}]
Include: happy, 401, 403, 404, 422, schema, SQLi, XSS. Return ONLY JSON.""",
"regression": """Given code changes, suggest regression suite.
Diff: {diff}
Files: {files}
PR: {pr}
Return JSON: {{"risk_score":85,"risk_reason":"","must_test":[{{"test_case":"","reason":"","module":""}}],"can_skip":[{{"test_case":"","reason":""}}],"coverage_suggestion":""}}
Return ONLY JSON."""
}

class LLMService:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.use_mock = not self.api_key
        if not self.use_mock:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=self.api_key)
            except:
                self.use_mock = True

    async def _call(self, prompt: str) -> str:
        if self.use_mock:
            return self._mock(prompt)
        try:
            r = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"system","content": SYSTEM},{"role":"user","content": prompt}],
                response_format={"type":"json_object"},
                temperature=0.3
            )
            return r.choices[0].message.content
        except Exception as e:
            return self._mock(prompt)

    def _mock(self, prompt: str) -> str:
        if "test cases as JSON array" in prompt:
            return json.dumps([
                {"id":"CF_001","title":"Verify password reset with valid email","type":"functional","priority":"P0","precondition":"User exists","steps":["Go to forgot password","Enter valid email","Click reset"],"expected_result":"OTP email sent","edge_case_rationale":"Core happy path"},
                {"id":"CF_002","title":"Verify OTP expiry after 10 minutes - boundary","type":"boundary","priority":"P0","precondition":"OTP sent","steps":["Wait 9:59 - enter OTP","Wait 10:01 and retry"],"expected_result":"First succeeds, second fails expired","edge_case_rationale":"Boundary time logic often fails"},
                {"id":"CF_003","title":"Reset with email containing + alias","type":"boundary","priority":"P1","precondition":"Email with +","steps":["Enter test+alias@gmail.com"],"expected_result":"System handles plus addressing","edge_case_rationale":"Regex fail on +"},
                {"id":"CF_004","title":"Rapid double-click reset button - race","type":"security","priority":"P1","precondition":"","steps":["Double click reset rapidly"],"expected_result":"Only one OTP, second blocked","edge_case_rationale":"Race condition"},
                {"id":"CF_005","title":"SQL injection in email field","type":"security","priority":"P0","precondition":"","steps":["Enter ' OR 1=1-- as email"],"expected_result":"Input sanitized","edge_case_rationale":"Security baseline"},
                {"id":"CF_006","title":"Unicode in email - i18n","type":"negative","priority":"P2","precondition":"","steps":["Enter test@exämple.com"],"expected_result":"Handled per RFC or clear error","edge_case_rationale":"i18n often missed"}
            ])
        if "non-obvious edge cases" in prompt:
            return json.dumps({"categories":[
                {"category":"Boundary","cases":[{"case":"OTP at exactly 10:00.000","risk":"High","why_it_matters":"Off-by-one ms error"},{"case":"Email length 254 vs 255 chars","risk":"Medium","why_it_matters":"RFC limit"}]},
                {"category":"Security","cases":[{"case":"Rate limit bypass with X-Forwarded-For rotation","risk":"High","why_it_matters":"Abuse vector"}]},
                {"category":"Concurrency","cases":[{"case":"Two simultaneous reset requests","risk":"High","why_it_matters":"Token invalidation race"}]}
            ]})
        if "BDD Gherkin" in prompt:
            return json.dumps({"feature":"Password Reset","background":"Given user exists","scenarios":[
                {"name":"Successful reset","type":"happy","gherkin":"Given user is on forgot password page\nWhen user enters valid email\nThen OTP email is sent"},
                {"name":"Expired OTP","type":"negative","gherkin":"Given OTP was sent 11 minutes ago\nWhen user enters OTP\nThen error 'OTP expired' is shown"}
            ]})
        if "bug report" in prompt:
            return json.dumps({"title":"Password reset fails for + alias emails","severity":"Major","priority":"P1","environment":"Prod Chrome","steps_to_reproduce":["Use email with +","Request reset","No email received"],"expected_vs_actual":{"expected":"Email with + should receive OTP","actual":"No email"},"logs_hint":"Check email regex validation","suggested_labels":["backend","email"],"suggested_assignee_role":"Backend"})
        if "API test cases" in prompt:
            return json.dumps([
                {"test_name":"Happy - Send reset OTP","method":"POST","endpoint":"/auth/forgot-password","payload":{"email":"user@test.com"},"assertions":["status == 200","has otp_id"],"type":"happy"},
                {"test_name":"Negative - Invalid email format","method":"POST","endpoint":"/auth/forgot-password","payload":{"email":"invalid"},"assertions":["status == 422"],"type":"negative"},
                {"test_name":"Security - SQLi attempt","method":"POST","endpoint":"/auth/forgot-password","payload":{"email":"' OR 1=1--"},"assertions":["status == 400"],"type":"security"}
            ])
        if "regression suite" in prompt:
            return json.dumps({"risk_score":88,"risk_reason":"Auth module changed - high impact","must_test":[
                {"test_case":"Login with valid credentials","reason":"Auth core changed","module":"auth"},
                {"test_case":"Password reset flow","reason":"Directly affected file","module":"auth"},
                {"test_case":"OTP expiry boundary","reason":"Time logic in diff","module":"auth"}
            ],"can_skip":[{"test_case":"Change profile picture","reason":"Unrelated module"}],"coverage_suggestion":"Run auth e2e + security suite"})
        return json.dumps({"mock": True})

    async def generate_test_cases(self, req, ctx=""):
        raw = await self._call(PROMPTS["test_cases"].format(requirement=req, context=ctx or "web"))
        try:
            data = json.loads(raw)
            return {"test_cases": data if isinstance(data, list) else data.get("test_cases", []), "count": len(data) if isinstance(data, list) else 0}
        except: return {"test_cases": [], "raw": raw}

    async def detect_edge_cases(self, req, ctx=""):
        raw = await self._call(PROMPTS["edge_cases"].format(requirement=req))
        try: return json.loads(raw)
        except: return {"categories": [], "raw": raw}

    async def story_to_gherkin(self, story):
        raw = await self._call(PROMPTS["gherkin"].format(requirement=story))
        try: return json.loads(raw)
        except: return {"feature": story, "scenarios": [], "raw": raw}

    async def generate_bug_report(self, bug, env):
        raw = await self._call(PROMPTS["bug_report"].format(bug=bug, env=env))
        try: return json.loads(raw)
        except: return {"title": bug[:60], "raw": raw}

    async def generate_api_tests(self, spec):
        raw = await self._call(PROMPTS["api_tests"].format(spec=spec))
        try:
            data = json.loads(raw)
            return data if isinstance(data, list) else data.get("tests", [])
        except: return []

    async def build_regression_suite(self, diff, files, pr):
        raw = await self._call(PROMPTS["regression"].format(diff=diff or "No diff", files=str(files), pr=pr or "N/A"))
        try: return json.loads(raw)
        except: return {"risk_score": 75, "must_test": [], "raw": raw}
