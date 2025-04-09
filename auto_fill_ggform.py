import requests
import random
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Lấy cấu hình từ biến môi trường
form_url = os.getenv("FORM_URL")
num_responses = int(os.getenv("NUM_RESPONSES", 20))
min_delay = float(os.getenv("MIN_DELAY", 1.5))
max_delay = float(os.getenv("MAX_DELAY", 4.0))
verbose_logging = os.getenv("VERBOSE_LOGGING", "true").lower() == "true"

# Cấu hình các entry ID tương ứng với từng câu hỏi từ biến môi trường
form_data_template = {
    os.getenv("FIELD_CLASS", "entry.1673755276"): "",         # Em là học sinh lớp
    os.getenv("FIELD_GENDER", "entry.803366471"): "",         # Giới tính
    os.getenv("FIELD_PREFERENCE", "entry.975913696"): "",     # Câu 1: Mức độ yêu thích
    os.getenv("FIELD_INTEREST", "entry.557521012"): "",       # Câu 2: Lý do hứng thú
    os.getenv("FIELD_EQ_KNOWLEDGE", "entry.1110732521"): "",  # Câu 3: Em có biết trí tuệ cảm xúc (EQ) là gì không?
    os.getenv("FIELD_RELATION", "entry.1059103494"): "",      # Câu 4: Nội dung bài học đạo đức có liên quan đến cảm xúc không?
    os.getenv("FIELD_EXPRESSION", "entry.2069632588"): "",    # Câu 5: Giáo viên có tạo điều kiện thể hiện cảm xúc không?
    os.getenv("FIELD_EMOTION", "entry.143017696"): "",        # Câu 6: Em có học được cách kiểm soát cảm xúc không?
    os.getenv("FIELD_DISCUSSION", "entry.1824094941"): "",    # Câu 7: Em có cơ hội thảo luận không?
    os.getenv("FIELD_IMPROVEMENT", "entry.1940461153"): "",   # Câu 8: Kỹ năng cảm xúc có cải thiện không?
    os.getenv("FIELD_IMPORTANCE", "entry.61104916"): "",      # Câu 9: Việc rèn luyện EQ có cần thiết không?
    os.getenv("FIELD_SUGGESTION", "entry.1675741628"): "",    # Câu 10: Đề xuất để giờ học hấp dẫn hơn
}

# Các lựa chọn cho từng câu hỏi theo form mới
classroom_options = ["9A5", "9A6", "9A3", "9A4"]
gender_options = ["NAM", "NỮ"]
preference_options = ["Rất yêu thích", "Yêu thích", "Bình thường", "Không yêu thích"]
interest_reasons = ["Nội dung kiến thức đa dạng", "Giáo viên áp dụng nhiều phương pháp thú vị", 
                     "Giáo viên tâm lý", "Môn học dễ đạt điểm cao", "Khác"]
eq_knowledge_options = ["Có", "Nghe rồi nhưng chưa hiểu rõ", "Chưa từng nghe"]
relation_options = ["Có", "Không", "Một phần"]
expression_options = ["Thỉnh thoảng", "Thường xuyên", "Không"]
emotion_control_options = ["Có", "Không rõ", "Không"]
discussion_options = ["Có", "Không"]
improvement_options = ["Có", "Chưa rõ", "Không"]
importance_options = ["Rất cần thiết", "Bình thường", "Không cần thiết"]

# 20 đề xuất chi tiết cho câu hỏi mở
suggestions = [
    "Tôi nghĩ nên tổ chức nhiều hoạt động trải nghiệm thực tế hơn trong các giờ học GDCD",
    "Giáo viên có thể sử dụng các video ngắn để minh họa các tình huống đạo đức thực tế",
    "Tạo không gian an toàn để học sinh có thể chia sẻ cảm xúc mà không sợ bị đánh giá",
    "Tổ chức các hoạt động nhóm nhỏ để thảo luận về các tình huống đạo đức khó xử",
    "Kết hợp nghệ thuật (vẽ, âm nhạc, kịch) vào các bài học về cảm xúc để tăng sự hấp dẫn",
    "Mời các chuyên gia tâm lý đến nói chuyện với học sinh về cách quản lý cảm xúc",
    "Dạy kỹ năng nhận biết và đặt tên cho các loại cảm xúc khác nhau",
    "Hướng dẫn các bài tập thực hành về kiểm soát cảm xúc tiêu cực như giận dữ, lo lắng",
    "Tích hợp các trò chơi và hoạt động vui nhộn vào bài học về quản lý cảm xúc",
    "Tổ chức các dự án cộng đồng để học sinh có thể áp dụng các bài học đạo đức vào thực tế",
    "Sử dụng các tình huống từ đời sống hàng ngày của học sinh làm ví dụ trong bài học",
    "Tạo sổ tay cảm xúc để học sinh ghi lại và theo dõi cảm xúc của mình hàng ngày",
    "Dạy các kỹ thuật thư giãn và chánh niệm để giúp học sinh kiểm soát căng thẳng",
    "Tổ chức các phiên chia sẻ cảm xúc định kỳ trong lớp học GDCD",
    "Khuyến khích học sinh đặt mục tiêu phát triển cảm xúc cá nhân và theo dõi tiến độ",
    "Sử dụng công nghệ và ứng dụng tương tác để tạo các bài học hấp dẫn về EQ",
    "Xây dựng thư viện sách về phát triển cảm xúc và khuyến khích học sinh đọc",
    "Tạo các tình huống mô phỏng để học sinh thực hành kỹ năng giải quyết xung đột",
    "Khuyến khích các hoạt động hợp tác thay vì cạnh tranh trong lớp học GDCD",
    "Đưa ra phản hồi tích cực và cụ thể khi học sinh thể hiện sự tiến bộ về kỹ năng cảm xúc"
]

print(f"Bắt đầu gửi {num_responses} phản hồi giả lập...")

# Gửi nhiều responses giả lập
for i in range(num_responses):
    form_data = form_data_template.copy()
    
    # Điền ngẫu nhiên vào các trường theo lựa chọn mới
    field_class = os.getenv("FIELD_CLASS", "entry.1673755276")
    field_gender = os.getenv("FIELD_GENDER", "entry.803366471")
    field_preference = os.getenv("FIELD_PREFERENCE", "entry.975913696")
    field_interest = os.getenv("FIELD_INTEREST", "entry.557521012")
    field_eq_knowledge = os.getenv("FIELD_EQ_KNOWLEDGE", "entry.1110732521")
    field_relation = os.getenv("FIELD_RELATION", "entry.1059103494")
    field_expression = os.getenv("FIELD_EXPRESSION", "entry.2069632588")
    field_emotion = os.getenv("FIELD_EMOTION", "entry.143017696")
    field_discussion = os.getenv("FIELD_DISCUSSION", "entry.1824094941")
    field_improvement = os.getenv("FIELD_IMPROVEMENT", "entry.1940461153")
    field_importance = os.getenv("FIELD_IMPORTANCE", "entry.61104916")
    field_suggestion = os.getenv("FIELD_SUGGESTION", "entry.1675741628")
    
    form_data[field_class] = random.choice(classroom_options)
    form_data[field_gender] = random.choice(gender_options)
    form_data[field_preference] = random.choice(preference_options)
    form_data[field_interest] = random.choice(interest_reasons)
    form_data[field_eq_knowledge] = random.choice(eq_knowledge_options)
    form_data[field_relation] = random.choice(relation_options)
    form_data[field_expression] = random.choice(expression_options)
    form_data[field_emotion] = random.choice(emotion_control_options)
    form_data[field_discussion] = random.choice(discussion_options)
    form_data[field_improvement] = random.choice(improvement_options)
    form_data[field_importance] = random.choice(importance_options)
    form_data[field_suggestion] = random.choice(suggestions)

    if verbose_logging:
        print(f"Sending form data: {form_data}")
        
    try:
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
