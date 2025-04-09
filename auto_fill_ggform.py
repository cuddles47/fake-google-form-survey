import requests
import random
import time

# Link gửi dữ liệu (POST) của Google Form
form_url = "https://docs.google.com/forms/d/e/1FAIpQLSeWl9qBipUz4oJTRc3joixKfiz3gi00SBKeQcFEksNukn2fcg/formResponse"

# Cấu hình các entry ID tương ứng với từng câu hỏi
form_data_template = {
    "entry.1715539090": "",  # Họ và tên
    "entry.1820486686": "",  # Giới tính
    "entry.1847694190": "",  # Ngành học
    "entry.368858845": "",   # Bạn đã có kiến thức về DevOps chưa?
}

# Một số lựa chọn giả
names = ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Minh D"]
genders = ["Nam", "Nữ", "Khác"]
majors = ["CNTT", "Kỹ thuật phần mềm", "Hệ thống thông tin", "Khoa học máy tính"]
devops_knowledge = ["Chưa", "Một ít", "Cơ bản", "Tốt"]

# Gửi nhiều responses giả lập
for i in range(50):  # Gửi 50 phản hồi
    form_data = form_data_template.copy()
    form_data["entry.1715539090"] = random.choice(names)
    form_data["entry.1820486686"] = random.choice(genders)
    form_data["entry.1847694190"] = random.choice(majors)
    form_data["entry.368858845"] = random.choice(devops_knowledge)

    response = requests.post(form_url, data=form_data)
    print(f"Sent response {i+1}, status code: {response.status_code}")
    
    time.sleep(random.uniform(0.5, 1.5))  # Delay giữa các lần gửi
