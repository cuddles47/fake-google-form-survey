# filepath: d:\project\fake-google-form-survey\auto_fill_ggform_new.py
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
num_responses = int(os.getenv("NUM_RESPONSES", 60))
min_delay = float(os.getenv("MIN_DELAY", 1.5))
max_delay = float(os.getenv("MAX_DELAY", 4.0))
verbose_logging = os.getenv("VERBOSE_LOGGING", "true").lower() == "true"

# Tạo template với tất cả các form fields từ biến môi trường
form_data_template = {
    os.getenv("FIELD_PHONE", "entry.723048589"): "",                     # Số điện thoại
    os.getenv("FIELD_GENDER", "entry.1284634938"): "",                   # Giới tính
    os.getenv("FIELD_AGE", "entry.714674737"): "",                       # Độ tuổi
    os.getenv("FIELD_JOB", "entry.1182528973"): "",                      # Nghề nghiệp
    os.getenv("FIELD_INCOME", "entry.396695018"): "",                    # Thu nhập
    os.getenv("FIELD_NEED", "entry.438110643"): [],                      # Nhu cầu làm nội thất
    os.getenv("FIELD_USED_SERVICE", "entry.1415315138"): "",             # Từng sử dụng dịch vụ
    os.getenv("FIELD_PLAN", "entry.1290045582"): "",                     # Có dự định làm nội thất
    os.getenv("FIELD_CHOICE", "entry.88438451"): "",                     # Hình thức làm nội thất
    os.getenv("FIELD_PRIORITY", "entry.235304159"): "",                  # Ưu tiên phòng
    os.getenv("FIELD_SERVICE", "entry.3180829"): "",                     # Lựa chọn dịch vụ
    os.getenv("FIELD_REASON", "entry.83483277"): [],                     # Lý do tách rời dự án
    os.getenv("FIELD_AI_EXP", "entry.2045442262"): [],                   # Kinh nghiệm với AI
    os.getenv("FIELD_INFO_SOURCE", "entry.1077655883"): [],              # Nguồn thông tin
    os.getenv("FIELD_FACTOR", "entry.1157663846"): "",                   # Yếu tố ảnh hưởng
    os.getenv("FIELD_FACTOR_F1", "entry.2132352851"): "",                # Nguời thân giới thiệu
    os.getenv("FIELD_FACTOR_F2", "entry.1829905709"): "",                # Đánh giá khách hàng
    os.getenv("FIELD_FACTOR_F3", "entry.121732886"): "",                 # Hình ảnh dự án
    os.getenv("FIELD_FACTOR_F4", "entry.56090466"): "",                  # Bài viết chia sẻ
    os.getenv("FIELD_FACTOR_F5", "entry.85970032"): "",                  # Quảng cáo mạng xã hội
    os.getenv("FIELD_FACTOR_F6", "entry.1270868494"): "",                # Nội dung từ KOLs
    os.getenv("FIELD_FACTOR_F7", "entry.571806922"): "",                 # Website chính thức
    os.getenv("FIELD_FACTOR_F8", "entry.1215248175"): "",                # Tư vấn trực tiếp
    os.getenv("FIELD_IMPACT", "entry.1421914297"): "",                   # Mức độ ảnh hưởng
    os.getenv("FIELD_IMPACT_I1", "entry.734035599"): "",                 # Giá cả
    os.getenv("FIELD_IMPACT_I2", "entry.760956149"): "",                 # Chất lượng
    os.getenv("FIELD_IMPACT_I3", "entry.1559038677"): "",                # Thái độ, chuyên môn
    os.getenv("FIELD_IMPACT_I4", "entry.192351050"): "",                 # Hình ảnh dự án
    os.getenv("FIELD_IMPACT_I5", "entry.792826521"): "",                 # Đánh giá từ khách
    os.getenv("FIELD_IMPACT_I6", "entry.62312338"): "",                  # Thời gian hoàn thiện
    os.getenv("FIELD_IMPACT_I7", "entry.129057080"): "",                 # Phong cách thiết kế
    os.getenv("FIELD_CONCERN", "entry.308821755"): [],                   # Điều lo lắng
    os.getenv("FIELD_PREV_COMPANY", "entry.1652272821"): "",             # Đơn vị làm nội thất trước đây
    os.getenv("FIELD_DISSATISFACTION", "entry.1706302253"): [],          # Điều không hài lòng
}

# Các lựa chọn cho từng câu hỏi dựa theo khảo sát của bạn
# Giới tính - trắc nghiệm (câu 1)
gender_options = [
    "Nam",
    "Nữ",
    "Khác"
]

# Độ tuổi - trắc nghiệm (câu 2)
age_options = [
    "25 - 32 tuổi",
    "33 - 40 tuổi",
    "41 - 52 tuổi",
    "53 tuổi trở lên"
]

# Nghề nghiệp - trắc nghiệm (câu 3)
job_options = [
    "Nhân viên văn phòng",
    "Chủ doanh nghiệp",
    "Lao động tự do",
    "Nội trợ",
    "Nghề khác: _____________"
]

# Thu nhập - trắc nghiệm (câu 4)
income_options = [
    "10 - 20 triệu",
    "21 - 30 triệu",
    "31 - 40 triệu",
    "41 - 50 triệu"
]

# Nhu cầu làm nội thất - hộp kiểm (câu 5)
need_options = [
    "Mới mua căn hộ",
    "Xây nhà mới",
    "Cải tạo/chỉnh sửa nhà cũ",
    "Cho thuê/bán lại",
    "Khác: _____________"
]

# Từng sử dụng dịch vụ - trắc nghiệm (câu 6)
used_service_options = [
    "Đã từng",
    "Chưa từng (đang cân nhắc)"
]

# Dự định làm nội thất - trắc nghiệm (câu 7)
plan_options = [
    "Có",
    "Không",
    "Đang cân nhắc"
]

# Hình thức làm nội thất - trắc nghiệm (câu 8)
choice_options = [
    "Làm full căn",
    "Làm theo phòng (phòng khách, bếp, phòng ngủ…)"
]

# Ưu tiên phòng - trắc nghiệm (câu 9)
priority_options = [
    "Phòng khách",
    "Phòng ngủ",
    "Bếp + ăn",
    "Phòng làm việc",
    "Phòng trẻ em"
]

# Lựa chọn dịch vụ - trắc nghiệm (câu 10)
service_options = [
    "Chỉ Thiết kế ( không thi công )",
    "Chỉ thi công ( không thiết kế )",
    "Trọn gói ( cả thiết kế và thi công )"
]

# Lý do tách rời dự án - hộp kiểm (câu 11)
reason_options = [
    "Muốn tự chọn đơn vị thi công rẻ hơn",
    "Muốn kiểm soát chất lượng kỹ hơn",
    "Có người quen làm phần thi công",
    "Đơn vị thiết kế không nhận thi công",
    "Khác: _____________"
]

# Kinh nghiệm với AI - hộp kiểm (câu 12)
ai_exp_options = [
    "1. Nhập thử lên AI để dựng hình ảnh phác họa theo idea của bạn?",
    "2. Dùng hình ảnh thiết kế của AI để gop ý cho đơn vị thiết kế?",
    "3. Dùng hình ảnh thiết kế của AI để gửi đơn vị thi công?"
]

# Nguồn thông tin - hộp kiểm (câu 13)
info_source_options = [
    "Facebook/TikTok/Zalo",
    "Google/Website",
    "Người quen giới thiệu",
    "Tham quan căn hộ mẫu",
    "Hội nhóm/diễn đàn (ví dụ: hiệp hội, group nội thất, chung cư…)",
    "Khác: _____________"
]

# Điều lo lắng - hộp kiểm (câu 16)
concern_options = [
    "Chi phí vượt ngân sách",
    "Không giống như bản thiết kế",
    "Không đảm bảo tiến độ",
    "Sử dụng vật liệu không đúng cam kết",
    "Khó làm việc, khó trao đổi với đội ngũ thi công",
    "Thiếu tin tưởng vào uy tín đơn vị",
    "Không rõ quy trình, giấy tờ",
    "Khác: _____________"
]

# Điều không hài lòng - hộp kiểm (câu 18)
dissatisfaction_options = [
    "Thiết kế không đúng ý tưởng ban đầu",
    "Chất lượng vật liệu không đúng như báo giá",
    "Trễ tiến độ thi công",
    "Nhân viên và thợ thiếu chuyên nghiệp",
    "Thi công không giống thiết kế",
    "Chi phí phát sinh ngoài dự toán ban đầu",
    "Giao tiếp và xử lý vấn đề chậm",
    "Không thực hiện chính sách bảo hành",
    "Khác: _______________"
]

# Chỉ số đánh giá mức độ ảnh hưởng (1-5)
rating_options = ["1", "2", "3", "4", "5"]

# List mẫu số điện thoại
phone_numbers = [""]

# Mẫu tên công ty nội thất
company_names = [
    "AIA Decor", "Nội Thất Hoàng Gia", "EuroStyle", "Nhà Xinh",
    "Luxury Home", "AA Corporation", "Savimex", "Thế Giới Nội Thất",
    "Decox Design", "IKEA", "Nội Thất An Cường", "Nội Thất Hòa Phát",
    "Nội Thất Phố", "SimpleLiving", "HomeDesign", "", "Không nhớ rõ",
    "AConcept", "Casa Nhà Xinh", "Một công ty nhỏ ở gần nhà"
]

print(f"Bắt đầu gửi {num_responses} phản hồi giả lập...")

# Gửi nhiều responses giả lập
for i in range(num_responses):
    form_data = form_data_template.copy()
    
    # Các ID cơ bản
    field_phone = os.getenv("FIELD_PHONE", "entry.723048589")
    field_gender = os.getenv("FIELD_GENDER", "entry.1284634938")
    field_age = os.getenv("FIELD_AGE", "entry.714674737")
    field_job = os.getenv("FIELD_JOB", "entry.1182528973")
    field_income = os.getenv("FIELD_INCOME", "entry.396695018")
    field_need = os.getenv("FIELD_NEED", "entry.438110643")
    field_used_service = os.getenv("FIELD_USED_SERVICE", "entry.1415315138")
    field_plan = os.getenv("FIELD_PLAN", "entry.1290045582")
    field_choice = os.getenv("FIELD_CHOICE", "entry.88438451")
    field_priority = os.getenv("FIELD_PRIORITY", "entry.235304159")
    field_service = os.getenv("FIELD_SERVICE", "entry.3180829")
    field_reason = os.getenv("FIELD_REASON", "entry.83483277")
    field_ai_exp = os.getenv("FIELD_AI_EXP", "entry.2045442262")
    field_info_source = os.getenv("FIELD_INFO_SOURCE", "entry.1077655883")
    
    # Các ID cho câu hỏi đánh giá (1-5)
    field_factor_f1 = os.getenv("FIELD_FACTOR_F1", "entry.2132352851")
    field_factor_f2 = os.getenv("FIELD_FACTOR_F2", "entry.1829905709")
    field_factor_f3 = os.getenv("FIELD_FACTOR_F3", "entry.121732886")
    field_factor_f4 = os.getenv("FIELD_FACTOR_F4", "entry.56090466")
    field_factor_f5 = os.getenv("FIELD_FACTOR_F5", "entry.85970032")
    field_factor_f6 = os.getenv("FIELD_FACTOR_F6", "entry.1270868494")
    field_factor_f7 = os.getenv("FIELD_FACTOR_F7", "entry.571806922")
    field_factor_f8 = os.getenv("FIELD_FACTOR_F8", "entry.1215248175")
    
    field_impact_i1 = os.getenv("FIELD_IMPACT_I1", "entry.734035599")
    field_impact_i2 = os.getenv("FIELD_IMPACT_I2", "entry.760956149")
    field_impact_i3 = os.getenv("FIELD_IMPACT_I3", "entry.1559038677")
    field_impact_i4 = os.getenv("FIELD_IMPACT_I4", "entry.192351050")
    field_impact_i5 = os.getenv("FIELD_IMPACT_I5", "entry.792826521")
    field_impact_i6 = os.getenv("FIELD_IMPACT_I6", "entry.62312338")
    field_impact_i7 = os.getenv("FIELD_IMPACT_I7", "entry.129057080")
    
    field_concern = os.getenv("FIELD_CONCERN", "entry.308821755")
    field_prev_company = os.getenv("FIELD_PREV_COMPANY", "entry.1652272821")
    field_dissatisfaction = os.getenv("FIELD_DISSATISFACTION", "entry.1706302253")

    # Điền dữ liệu vào form
    # Câu 0: Số điện thoại - trả lời ngắn
    form_data[field_phone] = random.choice(phone_numbers)
    
    # Câu 1-4, 6-10: Câu hỏi trắc nghiệm (chọn một đáp án)
    form_data[field_gender] = random.choice(gender_options)
    form_data[field_age] = random.choice(age_options)
    form_data[field_job] = random.choice(job_options)
    form_data[field_income] = random.choice(income_options)
    form_data[field_used_service] = random.choice(used_service_options)
    form_data[field_plan] = random.choice(plan_options)
    form_data[field_choice] = random.choice(choice_options)
    form_data[field_priority] = random.choice(priority_options)
    form_data[field_service] = random.choice(service_options)
    
    # Câu 5, 11-13, 16, 18: Câu hỏi hộp kiểm (chọn nhiều đáp án)
    # Câu 5: Nhu cầu làm nội thất (chọn 1-3 lựa chọn)
    selected_needs = random.sample(need_options, min(len(need_options), random.randint(1, 3)))
    for need in selected_needs:
        form_data[field_need].append(need)
    
    # Câu 11: Lý do tách rời dự án (chọn tối đa 2)
    selected_reasons = random.sample(reason_options, min(len(reason_options), random.randint(1, 2)))
    for reason in selected_reasons:
        form_data[field_reason].append(reason)
    
    # Câu 12: Kinh nghiệm với AI (chọn 1-2)
    selected_ai_exp = random.sample(ai_exp_options, min(len(ai_exp_options), random.randint(1, 2)))
    for ai_exp in selected_ai_exp:
        form_data[field_ai_exp].append(ai_exp)
    
    # Câu 13: Nguồn thông tin (chọn 1-3)
    selected_info_sources = random.sample(info_source_options, min(len(info_source_options), random.randint(1, 3)))
    for info_source in selected_info_sources:
        form_data[field_info_source].append(info_source)
    
    # Câu 14 & 15: Xếp hạng (1-5)
    # Câu 14: Đánh giá mức độ ảnh hưởng cho các yếu tố (1-5)
    form_data[field_factor_f1] = random.choice(rating_options)
    form_data[field_factor_f2] = random.choice(rating_options)
    form_data[field_factor_f3] = random.choice(rating_options)
    form_data[field_factor_f4] = random.choice(rating_options)
    form_data[field_factor_f5] = random.choice(rating_options)
    form_data[field_factor_f6] = random.choice(rating_options)
    form_data[field_factor_f7] = random.choice(rating_options)
    form_data[field_factor_f8] = random.choice(rating_options)
    
    # Câu 15: Mức độ ảnh hưởng của các yếu tố
    form_data[field_impact_i1] = random.choice(rating_options)
    form_data[field_impact_i2] = random.choice(rating_options)
    form_data[field_impact_i3] = random.choice(rating_options)
    form_data[field_impact_i4] = random.choice(rating_options)
    form_data[field_impact_i5] = random.choice(rating_options)
    form_data[field_impact_i6] = random.choice(rating_options)
    form_data[field_impact_i7] = random.choice(rating_options)
    
    # Câu 16: Điều lo lắng (chọn 1-2)
    selected_concerns = random.sample(concern_options, min(len(concern_options), random.randint(1, 2)))
    for concern in selected_concerns:
        form_data[field_concern].append(concern)
    
    # Câu 17: Thông tin công ty cũ - trả lời ngắn
    form_data[field_prev_company] = random.choice(company_names)
    
    # Câu 18: Điều không hài lòng (chọn 1-3)
    selected_dissatisfactions = random.sample(dissatisfaction_options, min(len(dissatisfaction_options), random.randint(1, 3)))
    for dissatisfaction in selected_dissatisfactions:
        form_data[field_dissatisfaction].append(dissatisfaction)

    if verbose_logging:
        print(f"Đang gửi form data #{i+1}...")
        print(json.dumps(form_data, ensure_ascii=False, indent=2))
        
    try:
        # Hiển thị một phần dữ liệu quan trọng để tracking
        print(f"Submitting response #{i+1}: Phone={form_data[field_phone]}, Gender={form_data[field_gender]}, Age={form_data[field_age]}")
        
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
