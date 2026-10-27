
def format_jira_payload(bug_report: dict):
    return {
        "fields": {
            "summary": bug_report.get("title", "Bug from CaseForge AI"),
            "description": {"type": "doc","version":1,"content":[
                {"type":"paragraph","content":[{"type":"text","text":f"Environment: {bug_report.get('environment','')}"}]},
                {"type":"bulletList","content":[{"type":"listItem","content":[{"type":"paragraph","content":[{"type":"text","text":s}]}]} for s in bug_report.get("steps_to_reproduce", [])]},
                {"type":"paragraph","content":[{"type":"text","text":f"Expected: {bug_report.get('expected_vs_actual',{}).get('expected','')}"}]},
                {"type":"paragraph","content":[{"type":"text","text":f"Actual: {bug_report.get('expected_vs_actual',{}).get('actual','')}"}]},
            ]},
            "issuetype": {"name": "Bug"},
            "priority": {"name": "Medium"}
        }
    }
