import pandas as pd
from vncorenlp import VnCoreNLP

# ✅ Đường dẫn đến file VnCoreNLP-1.2.jar
vncorenlp_path = r"D:\Code\CK\VnCoreNLP-master\VnCoreNLP-1.2.jar"

# ✅ Khởi tạo VnCoreNLP
annotator = VnCoreNLP(vncorenlp_path, annotators="wseg", max_heap_size='-Xmx500m')

# ✅ Đọc dữ liệu từ file CSV
df_news = pd.read_csv("data1.csv")

# ✅ Danh sách stopwords trong bối cảnh tài chính (có thể mở rộng)
stopwords = set([
    "là", "của", "và", "có", "cho", "các", "một", "được", "đến", "với", "từ", "sẽ", 
    "trong", "khi", "này", "sau", "cùng", "về", "đã", "nhiều", "lại", "thì", "ra", 
    "hơn", "năm", "ngày", "vừa", "sáng", "chiều", "nay", "lúc", "tại", "vào", "cũng"
])

# ✅ Hàm tách từ và loại bỏ stopwords
def preprocess_text(text):
    if pd.isna(text):  # Nếu dữ liệu bị thiếu, trả về chuỗi rỗng
        return ""
    words = annotator.tokenize(text)  # Tách từ
    words = [w for sentence in words for w in sentence if w.lower() not in stopwords]  # Loại stopwords
    return " ".join(words)

# ✅ Áp dụng tiền xử lý lên cột 'title'
df_news['processed_title'] = df_news['title'].apply(preprocess_text)

# ✅ Xuất file kết quả
df_news.to_csv("data2.csv", index=False)

print("✅ Hoàn thành xử lý văn bản! File đã được lưu vào 'data2.csv'.")

