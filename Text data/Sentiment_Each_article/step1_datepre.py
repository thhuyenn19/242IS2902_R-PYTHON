import pandas as pd
import numpy as np

# Đọc file bài báo và file stock
df_news = pd.read_csv("file_updated.csv")  # Cột 'publish_time' chứa ngày xuất bản
df_stock = pd.read_csv("vcb.csv")  # Cột 'Date' chứa ngày giao dịch

# Chuyển cột 'publish_time' và 'Date' thành datetime (Sửa lỗi định dạng ngày)
df_news['publish_time'] = pd.to_datetime(df_news['publish_time'], dayfirst=True, errors='coerce')
df_stock['Date'] = pd.to_datetime(df_stock['Date'], dayfirst=True, errors='coerce')

df_stock = df_stock.dropna(subset=['Date'])

# Lấy danh sách các ngày giao dịch hợp lệ và sắp xếp tăng dần
valid_dates = np.sort(df_stock['Date'].dropna().unique())

# Đảm bảo tất cả các giá trị trong valid_dates đều là Timestamp
valid_dates = pd.DatetimeIndex(valid_dates)


# Hàm tìm ngày giao dịch gần nhất trước đó
def get_nearest_previous_trading_day(date, valid_dates):
    if pd.isna(date):
        return pd.NaT

    # Nếu ngày đã nằm trong các ngày giao dịch, giữ nguyên ngày đó
    if date in valid_dates:
        return date

    # Nếu không phải ngày giao dịch, tìm ngày giao dịch gần nhất trước đó
    mask = valid_dates < date
    if not any(mask):  # Không có ngày giao dịch nào trước date
        return pd.NaT

    return valid_dates[mask][-1]  # Lấy ngày giao dịch gần nhất trước date


# Áp dụng hàm cho từng ngày xuất bản
df_news['publish_time'] = df_news['publish_time'].apply(
    lambda x: get_nearest_previous_trading_day(x, valid_dates)
)

# Lưu kết quả
df_news.to_csv("data1.csv", index=False)
print("✅ Hoàn thành xử lý ngày! File đã được lưu.")