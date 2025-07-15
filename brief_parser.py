import os
import requests
import re
import json

def parse_brief(brief_text):
    url = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
    headers = {
        "Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}"
    }

    prompt = f"""
Extract the following from this creative brief and return in a clear structured format:

- Goals
- Deliverables
- Key Dates
- Responsibilities (Name – Role format)

Brief:
{brief_text}

Return the information clearly labeled like:

Goals:
- ...
- ...

Deliverables:
- ...
- ...

Key Dates:
- ...
- ...

Responsibilities:
- Name – Role
- Name – Role
"""

    response = requests.post(url, headers=headers, json={"inputs": prompt})
    raw_text = response.text

    print("DEBUG: Hugging Face response")
    print(raw_text)

    # Parse manually
    goals, deliverables, key_dates, responsibilities = [], [], [], []
    current = None

    for line in raw_text.splitlines():
        line = line.strip()

        if not line:
            continue

        lower = line.lower()
        if lower.startswith("goals"):
            current = goals
        elif lower.startswith("deliverables"):
            current = deliverables
        elif lower.startswith("key dates"):
            current = key_dates
        elif lower.startswith("responsibilities"):
            current = responsibilities
        elif current is not None and (line.startswith("-") or line.startswith("•")):
            item = line.strip("-• ").strip()
            current.append(item)

    # Convert responsibilities into dicts
    responsibility_list = []
    for entry in responsibilities:
        if "–" in entry:
            person, role = entry.split("–", 1)
            responsibility_list.append({"person": person.strip(), "role": role.strip()})
        elif "-" in entry:
            person, role = entry.split("-", 1)
            responsibility_list.append({"person": person.strip(), "role": role.strip()})
        else:
            responsibility_list.append({"person": entry.strip(), "role": "Unknown"})

    return {
        "goals": goals,
        "deliverables": deliverables,
        "key_dates": key_dates,
        "responsibilities": responsibility_list,
        "raw_response": raw_text  # Optional for debugging
    }
