from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

import time

# Cấu hình trình duyệt Chrome
options = Options()
options.headless = False  
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = 'https://vietstock.vn/chung-khoan.htm'
driver.get(url)
links = []
time.sleep(3)

try:
    daterange_input = driver.find_element(By.NAME, "daterange")  
    daterange_input.clear() 
    daterange_input.send_keys("2024-9-29 - 2025-1-1")
    time.sleep(2)
    daterange_input.send_keys(Keys.ENTER)  
    time.sleep(10)

    while True:
        post_section = driver.find_elements(By.CLASS_NAME, "channelContent")
        for post in post_section:
            try:
                link = post.find_element(By.CLASS_NAME, 'fontbold')
                url = link.get_attribute('href')
                if url and url not in links:
                    links.append(url)
                    print("Link:", url)
            except Exception as e:
                print("Lỗi khi lấy link:", e)

        # Kiểm tra nếu có nút "Trang sau" hay không
        try:
            page_link = driver.find_element(By.XPATH, '//a[@title="Trang sau"]')
            page_link.click()
            time.sleep(20)
        except Exception:
            print("Không tìm thấy nút Trang sau, kết thúc vòng lặp.")
            break

except Exception as e:
    print("Lỗi:", e)

# Đóng trình duyệt sau khi hoàn thành
driver.quit()

# Lưu link vào file txt
with open('vt_links1.txt', 'w', encoding='utf-8') as f:
    for link in links:
        f.write(link + '\n')

print("Đã lưu tất cả các link vào vietstock_linksss.txt.")
