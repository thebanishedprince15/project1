import os
import requests
import json

def parse_brief(brief_text):
    url = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"}
    prompt = f"""Extract project goals, deliverables, key dates, and team responsibilities from the following creative brief. Return JSON.

Creative Brief:
{brief_text}

Expected format:
{{
  "goals": ["goal1", "goal2"],
  "deliverables": ["item1", "item2"],
  "key_dates": ["YYYY-MM-DD"],
  "responsibilities": [{{"person": "Name", "role": "Designer"}}]
}}
"""
    payload = {
        "inputs": prompt
    }
    response = requests.post(url, headers=headers, json=payload)
    try:
        output = response.json()
        text = output[0]['generated_text'] if isinstance(output, list) else output.get("generated_text", "")
        match = json.loads(text[text.index("{"):text.rindex("}")+1])
        return match
    except Exception as e:
        return {"error": str(e)}
