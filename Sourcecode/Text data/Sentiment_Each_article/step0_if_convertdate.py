import pandas as pd
from datetime import datetime

# Đọc file CSV
df = pd.read_csv('stock_VCB_filled.csv')

# Giả sử cột chứa ngày có tên là 'date'
# Chuyển đổi định dạng từ MM/DD/YYYY sang DD-MM-YYYY
df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d')

# Lưu lại file CSV
df.to_csv('vcb.csv', index=False)

print("Đã chuyển đổi định dạng ngày thành công!")