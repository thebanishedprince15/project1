import os
import requests
import json
import re

def parse_brief(brief_text):
    url = "https://api-inference.huggingface.co/models/bigscience/T0pp"
    headers = {
        "Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"
    }

    prompt = f"""
Extract the following information from the creative brief and return it in JSON:

1. goals (list)
2. deliverables (list)
3. key_dates (list of strings or deadline notes)
4. responsibilities (list of dicts with 'person' and 'role')

Brief:
{brief_text}

Return only valid JSON.
"""

    response = requests.post(url, headers=headers, json={"inputs": prompt})

    # Debug log
    print("DEBUG Hugging Face Status:", response.status_code)
    print("DEBUG Response Text:", response.text)

    # Try to extract the first JSON object from the response
    try:
        raw_text = response.text
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            return json.loads(match.group())
        else:
            return {"error": "No JSON found in response", "raw": raw_text}
    except Exception as e:
        return {"error": f"Failed to parse JSON: {str(e)}", "raw": response.text}
        
