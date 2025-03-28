from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager


def setup_driver():
    """Thiết lập WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver


def format_publish_time(publish_time):
    """Chuyển đổi thời gian về định dạng dd-MM-yyyy"""
    try:
        dt = datetime.strptime(publish_time[:10], "%Y-%m-%d")
        return dt.strftime("%d-%m-%Y")
    except Exception:
        return "Không tìm thấy"


def extract_news_info(file_path, output_file, start_line, end_line=None):
    """Trích xuất tiêu đề và thời gian đăng bài từ các link trong file .txt"""

    with open(file_path, 'r', encoding='utf-8') as file:
        all_lines = [line.strip() for line in file.readlines() if line.strip()]
        urls = all_lines[start_line - 1:end_line]  # Python index từ 0 nên trừ đi 1

    driver = setup_driver()
    news_data = []

    try:
        for index, url in enumerate(urls):
            print(f"Đang xử lý ({index + 1}/{len(urls)}): {url}")
            try:
                driver.get(url)
                time.sleep(3)  # Chờ trang load

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')

                # Lấy tiêu đề từ thẻ <title>
                title_element = soup.find("title")
                title = title_element.text.strip() if title_element else "Không tìm thấy"

                # Tìm thời gian đăng bài từ thẻ meta
                time_element = soup.find("meta", attrs={"property": "article:published_time"})
                publish_time_raw = time_element["content"] if time_element else "Không tìm thấy"
                publish_time = format_publish_time(publish_time_raw)

                news_data.append({
                    "url": url,
                    "title": title,
                    "publish_time": publish_time
                })

                print(f"✔ Lấy thành công: {title[:50]}...")

                # Lưu dữ liệu sau mỗi lần lấy được một bài báo
                df = pd.DataFrame(news_data)
                df.to_csv(output_file, index=False, encoding="utf-8-sig")

            except Exception as e:
                print(f"❌ Lỗi khi xử lý {url}: {str(e)}")
                continue

        print(f"✅ Đã lưu {len(news_data)} bài viết vào {output_file}")

        return df

    finally:
        print("Đóng WebDriver...")
        driver.quit()


file_path = 'vt_links1.txt'
output_file = f"vietstock_news_full111_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.csv"

# Process the entire file by starting from line 1
df_news = extract_news_info(file_path, output_file, start_line=1)
print("\nPreview dữ liệu:")
print(df_news.head())
