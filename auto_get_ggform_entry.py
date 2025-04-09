import requests
import re
from bs4 import BeautifulSoup

# Link đến trang VIEWFORM (not formResponse)
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeWl9qBipUz4oJTRc3joixKfiz3gi00SBKeQcFEksNukn2fcg/viewform"

# Tải HTML trang form
res = requests.get(form_url)
soup = BeautifulSoup(res.text, 'html.parser')

# Tìm tất cả input fields có name="entry.xxxxx"
entries = {}
for input_tag in soup.find_all(['input', 'textarea', 'select']):
    name_attr = input_tag.get('name')
    if name_attr and name_attr.startswith('entry.'):
        # Tìm label gần nhất phía trên
        label = input_tag.find_previous('div', class_='M7eMe')  # class có thể thay đổi tùy form
        label_text = label.text.strip() if label else "Không rõ câu hỏi"
        entries[name_attr] = label_text

# In kết quả
for entry, label in entries.items():
    print(f"{entry} → {label}")
