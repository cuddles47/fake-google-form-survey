# file này để tự động điền vào Google Form
import requests
import random
import time
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Lấy cấu hình từ biến môi trường
form_url = os.getenv("FORM_URL")
num_responses = int(os.getenv("NUM_RESPONSES", 6))
min_delay = float(os.getenv("MIN_DELAY", 1.5))
max_delay = float(os.getenv("MAX_DELAY", 4.0))
verbose_logging = os.getenv("VERBOSE_LOGGING", "true").lower() == "true"

# Tạo template với tất cả các form fields từ biến môi trường
form_data_template = {
    os.getenv("FIELD_GENDER", "entry.1696897851"): [],                   # Câu 1: Giới tính của bạn là
    os.getenv("FIELD_JOB", "entry.647509306"): [],                       # Câu 2: Nghề nghiệp hiện tại của bạn
    os.getenv("FIELD_LOCATION", "entry.125157081"): "",                  # Câu 3: Bạn đang sống ở tỉnh thành nào?
    os.getenv("FIELD_AGE", "entry.1503145098"): [],                      # Câu 4: Độ tuổi của bạn
    os.getenv("FIELD_INTEREST", "entry.448714828"): [],                  # Câu 5: Bạn có quan tâm đến Kinh Dịch không?
    os.getenv("FIELD_SOURCE", "entry.1762183134"): [],                   # Câu 6: Bạn biết Kinh Dịch qua phương tiện nào?
    os.getenv("FIELD_EXPERIENCE", "entry.1690833340"): [],               # Câu 7: Bạn có từng xin quẻ, xem bói, hoặc rút bài chiêm nghiệm chưa?
    os.getenv("FIELD_AI_SUPPORT", "entry.2092013298"): [],               # Câu 8: Bạn có muốn có một ứng dụng AI để hỗ trợ giải nghĩa quẻ khi sử dụng bộ bài Kinh Dịch không?
    os.getenv("FIELD_DECK_INTEREST", "entry.2129006586"): [],            # Câu 9: Nếu sở hữu một bộ bài Kinh Dịch kèm theo app AI giải quẻ, bạn cảm thấy thế nào?
    os.getenv("FIELD_TOPICS", "entry.432475134"): [],                    # Câu 10: Những chủ đề bạn quan tâm?
    os.getenv("FIELD_PRICE", "entry.1343401821"): []                     # Câu 11: Với combo "bộ bài Kinh Dịch + app AI trọn đời", bạn thấy mức giá nào hợp lý?
}

# Các lựa chọn cho từng câu hỏi dựa theo khảo sát của bạn
# Câu 1: Giới tính của bạn là
gender_options = [
    "Nam",
    "Nữ",
]

# Câu 2: Nghề nghiệp hiện tại của bạn
job_options = [
    "Sinh viên",
    "Nhân viên văn phòng",
    "Kinh doanh tự do",
    "Khác"
]

# Câu 4: Độ tuổi của bạn
age_options = [
    "25 - 31",
    "32 - 38",
]

# Câu 5: Bạn có quan tâm đến Kinh Dịch không?
interest_options = [
    "Rất quan tâm",
    "Có nghe nhưng chưa tìm hiểu sâu",
]

# Câu 6: Bạn biết Kinh Dịch qua phương tiện nào?
source_options = [
    "Mạng Xã Hội (Facebook, Tiktok,...)",
    "Bạn bè, người thân",
]

# Câu 7: Bạn có từng xin quẻ, xem bói, hoặc rút bài chiêm nghiệm chưa?
experience_options = [
    "Có, thường xuyên",
    "Có, thỉnh thoảng", 
]

# Câu 8: Bạn có muốn có một ứng dụng AI để hỗ trợ giải nghĩa quẻ khi sử dụng bộ bài Kinh Dịch không?
ai_support_options = [
    "Rất muốn, vì tôi không rành cách xem",
]

# Câu 9: Nếu sở hữu một bộ bài Kinh Dịch kèm theo app AI giải quẻ, bạn cảm thấy thế nào?
deck_interest_options = [
    "Rất hứng thú",
]

# Câu 10: Những chủ đề bạn quan tâm?
topics_options = [
    "Tình Yêu",
    "Gia Đình",
    "Tài Chính",
    "Kinh Doanh",
    "Sức Khỏe",
]

# Câu 11: Với combo "bộ bài Kinh Dịch + app AI trọn đời", bạn thấy mức giá nào hợp lý?
price_options = [
    "200.000-300.000",
    "300.000-400.000",
]

# List các tỉnh thành phổ biến ở Việt Nam để điền vào câu 3
locations = [
    "Hà Nội", "TP. Hồ Chí Minh",
]

print(f"Bắt đầu gửi {num_responses} phản hồi giả lập...")

# Gửi nhiều responses giả lập
for i in range(num_responses):
    form_data = form_data_template.copy()
    
    # Lấy các field ID từ biến môi trường
    field_gender = os.getenv("FIELD_GENDER", "entry.1696897851")         # Câu 1: Giới tính
    field_job = os.getenv("FIELD_JOB", "entry.647509306")                # Câu 2: Nghề nghiệp
    field_location = os.getenv("FIELD_LOCATION", "entry.125157081")      # Câu 3: Tỉnh thành
    field_age = os.getenv("FIELD_AGE", "entry.1503145098")               # Câu 4: Độ tuổi
    field_interest = os.getenv("FIELD_INTEREST", "entry.448714828")      # Câu 5: Quan tâm Kinh Dịch
    field_source = os.getenv("FIELD_SOURCE", "entry.1762183134")         # Câu 6: Phương tiện biết Kinh Dịch
    field_experience = os.getenv("FIELD_EXPERIENCE", "entry.1690833340") # Câu 7: Kinh nghiệm xem bói
    field_ai_support = os.getenv("FIELD_AI_SUPPORT", "entry.2092013298") # Câu 8: Ứng dụng AI hỗ trợ
    field_deck_interest = os.getenv("FIELD_DECK_INTEREST", "entry.2129006586") # Câu 9: Mức độ quan tâm
    field_topics = os.getenv("FIELD_TOPICS", "entry.432475134")          # Câu 10: Chủ đề quan tâm
    field_price = os.getenv("FIELD_PRICE", "entry.1343401821")           # Câu 11: Mức giá hợp lý
   
    # Điền dữ liệu vào form
    # Đối với câu hỏi trắc nghiệm (chỉ chọn 1 đáp án) - cần đưa vào mảng
    form_data[field_gender] = [random.choice(gender_options)]
    form_data[field_job] = [random.choice(job_options)]
    form_data[field_age] = [random.choice(age_options)]
    form_data[field_interest] = [random.choice(interest_options)]
    form_data[field_source] = [random.choice(source_options)]
    form_data[field_experience] = [random.choice(experience_options)]
    form_data[field_ai_support] = [random.choice(ai_support_options)]
    form_data[field_deck_interest] = [random.choice(deck_interest_options)]
    
    # Câu 10: Những chủ đề bạn quan tâm? (chọn 1 chủ đề)
    form_data[field_topics] = [random.choice(topics_options)]
    
    # Câu 11: Mức giá hợp lý
    form_data[field_price] = [random.choice(price_options)]
    
    # Câu 3: Bạn đang sống ở tỉnh thành nào? - câu hỏi điền text
    form_data[field_location] = random.choice(locations)
    if verbose_logging:
        print(f"Đang gửi form data #{i+1}...")
        print(json.dumps(form_data, ensure_ascii=False, indent=2))
        
    try:        # Hiển thị một phần dữ liệu quan trọng để tracking
        gender_info = form_data[field_gender][0] if isinstance(form_data[field_gender], list) and len(form_data[field_gender]) > 0 else form_data[field_gender]
        age_info = form_data[field_age][0] if isinstance(form_data[field_age], list) and len(form_data[field_age]) > 0 else form_data[field_age]
        
        print(f"Submitting response #{i+1}: Gender={gender_info}, Location={form_data[field_location]}, Age={age_info}")
        
        response = requests.post(form_url, data=form_data)
        status = "Thành công" if response.status_code == 200 else f"Lỗi: {response.status_code}"
        print(f"Đã gửi phản hồi {i+1}/{num_responses}: {status}")
    except Exception as e:
        print(f"Lỗi khi gửi phản hồi {i+1}: {str(e)}")
    
    # Delay ngẫu nhiên giữa các lần gửi để tránh bị phát hiện là bot
    delay = random.uniform(min_delay, max_delay)
    if verbose_logging:
        print(f"Chờ {delay:.2f} giây trước khi gửi phản hồi tiếp theo...")
    time.sleep(delay)

print("Hoàn thành!")
