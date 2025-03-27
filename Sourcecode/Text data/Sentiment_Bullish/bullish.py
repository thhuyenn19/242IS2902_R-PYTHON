import pandas as pd

# Định nghĩa đường dẫn tới các tệp dữ liệu
file_paths = {
    "CafeF_sentiment": "cafef_sen.csv",
    "Thanhnien_sentiment": "Thanhnien_sentiment.csv",
    "Vietstock_sentiment": "vietstock_sen.csv"
}

# Đọc dữ liệu từ các tệp và thêm cột nguồn
dfs = []
for name, path in file_paths.items():
    df = pd.read_csv(path)
    df['source'] = name  # Thêm cột nguồn tin
    dfs.append(df)

# Gộp tất cả dữ liệu lại thành một DataFrame
df_combined = pd.concat(dfs, ignore_index=True)

# Chuyển đổi cột publish_time về kiểu datetime
df_combined['date'] = pd.to_datetime(df_combined['date'], errors='coerce')

# Loại bỏ các dòng không có giá trị ngày hợp lệ
df_combined = df_combined.dropna(subset=['date'])

# Trích xuất ngày từ cột publish_time
df_combined['date'] = df_combined['date'].dt.date

# Chuẩn hóa cột sentiment
df_combined['sentiment'] = df_combined['sentiment'].str.lower()

# Hàm tính chỉ số Bullish Index
def compute_bullish_index(group):
    positive = (group['sentiment'] == 'positive').sum()
    neutral = (group['sentiment'] == 'neutral').sum()
    negative = (group['sentiment'] == 'negative').sum()
    total = positive + neutral + negative
    if total == 0:
        bullish_index = None  # Tránh chia cho 0
        dominant_sentiment = None
    else:
        bullish_index = (positive + 0.5 * neutral) / total
        # Xác định sentiment chiếm ưu thế
        dominant_sentiment = max(
            [('positive', positive), ('neutral', neutral), ('negative', negative)],
            key=lambda x: x[1]
        )[0]
    return pd.Series([total, bullish_index, dominant_sentiment], index=['total_articles', 'bullish_index', 'dominant_sentiment'])

# Áp dụng tính toán theo từng ngày
df_summary = df_combined.groupby('date').apply(compute_bullish_index).reset_index()

# Xuất kết quả ra file CSV
df_summary.to_csv("bullish_index_summary.csv", index=False)

# Hiển thị kết quả
print(df_summary)