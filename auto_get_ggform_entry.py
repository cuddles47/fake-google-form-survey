# file này để lấy entry ID của các trường trong Google Form
import requests
import re
import json
from bs4 import BeautifulSoup

# Link đến trang VIEWFORM (not formResponse)
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeWl9qBipUz4oJTRc3joixKfiz3gi00SBKeQcFEksNukn2fcg/viewform"

# Tải HTML trang form
res = requests.get(form_url)
soup = BeautifulSoup(res.text, 'html.parser')

# Tìm dữ liệu form trong script JSON
form_data = None
for script in soup.find_all('script'):
    if script.string and 'FB_PUBLIC_LOAD_DATA_' in script.string:
        json_text = script.string.replace('var FB_PUBLIC_LOAD_DATA_ =', '').strip()[:-1]
        try:
            form_data = json.loads(json_text)
            break
        except:
            continue

if not form_data:
    print("Không thể tìm thấy dữ liệu form!")
    exit(1)

# Extract form structure - questions and answers
questions = {}

# Parse form structure from JSON data
try:
    form_items = form_data[1][1]
    for item in form_items:
        if isinstance(item, list) and len(item) > 4:
            question_id = item[4][0][0]
            question_text = item[1]
            
            # Initialize question data
            questions[f"entry.{question_id}"] = {
                "text": question_text,
                "type": "",
                "options": []
            }
            
            # Check if it has options (multiple choice, dropdown, etc.)
            if len(item) > 4 and isinstance(item[4], list):
                question_type = item[3]
                questions[f"entry.{question_id}"]["type"] = question_type
                
                # Extract options if present
                if question_type in [0, 1, 2, 3, 4]:  # Multiple choice, checkbox, dropdown
                    if len(item[4]) > 0 and isinstance(item[4][0], list):
                        for option in item[4][0]:
                            if isinstance(option, list) and len(option) > 0:
                                option_text = option[0]
                                option_value = option[2] if len(option) > 2 else option[0]
                                questions[f"entry.{question_id}"]["options"].append({
                                    "text": option_text,
                                    "value": option_value
                                })
except Exception as e:
    print(f"Error parsing form structure: {e}")

# In kết quả
print("\n=== GOOGLE FORM QUESTIONS AND ANSWERS ===\n")
for entry_id, question_data in questions.items():
    print(f"{entry_id} → {question_data['text']}")
    
    if question_data["options"]:
        print("  Options:")
        for i, option in enumerate(question_data["options"], 1):
            print(f"    {i}. {option['text']}")
    
    print()

# Output payload example for form submission
print("=== EXAMPLE PAYLOAD FOR FORM SUBMISSION ===")
payload = {}
for entry_id, question_data in questions.items():
    if question_data["options"] and len(question_data["options"]) > 0:
        payload[entry_id] = question_data["options"][0]["value"]
    else:
        payload[entry_id] = "Sample answer"

print(json.dumps(payload, indent=2, ensure_ascii=False))


