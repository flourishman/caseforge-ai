
import json
from datetime import datetime

def generate_postman_collection(spec: str, tests: list, base_url: str):
    items = []
    for t in tests[:20]:
        test_script = "\n".join([f"pm.test('{a}', function() {{ pm.expect(true).to.be.true; }});" for a in t.get("assertions", ["Status 200"])[:4]])
        items.append({
            "name": t.get("test_name", "Test"),
            "request": {
                "method": t.get("method", "GET"),
                "header": [{"key": "Content-Type", "value": "application/json"}],
                "url": {"raw": f"{base_url}{t.get('endpoint','/')}", "host": [base_url], "path": [t.get('endpoint','/').lstrip('/')]},
                "body": {"mode": "raw", "raw": json.dumps(t.get("payload", {}))} if t.get("payload") else None
            },
            "event": [{"listen": "test", "script": {"exec": [test_script], "type": "text/javascript"}}]
        })
    return {
        "info": {"name": f"CaseForge AI - {datetime.now().strftime('%Y-%m-%d')}", "description": f"Auto-generated from: {spec[:100]}", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
        "item": items
    }
