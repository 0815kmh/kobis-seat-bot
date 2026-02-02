import os
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_kobis_seat_data():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    
    # [수정 완료] 날짜 고정을 제거한 기본 URL (자동으로 어제 확정 데이터를 보여줌)
    url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findDailySeatTicketList.do"
    
    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#tbody_0 tr"))
        )
        time.sleep(5)
        
        seat_data = []
        rows = driver.find_elements(By.CSS_SELECTOR, "#tbody_0 tr")
        
        if not rows or "데이터가 없습니다" in rows[0].text:
            return ""

        for row in rows[:5]:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 13:
                name = cols[1].text.strip()
                seat_cnt = cols[9].text.replace(',', '').strip()
                seat_rate = cols[13].text.replace('%', '').strip()
                if name:
                    seat_data.append(f"{name}|{seat_cnt}|{seat_rate}")
        
        return "\n".join(seat_data)

    except Exception as e:
        print(f"Error: {e}")
        return ""
    finally:
        driver.quit()

def send_email(content):
    if not content:
        return

    msg = MIMEText(content)
    msg['Subject'] = "[KOBIS_SEAT] 일일 리포트"
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['GMAIL_USER']
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['GMAIL_USER'], os.environ['GMAIL_APP_PASSWORD'])
            smtp.send_message(msg)
        print("Mail Sent")
    except Exception as e:
        print(f"Mail Error: {e}")

if __name__ == "__main__":
    data = get_kobis_seat_data()
    print(data)
    send_email(data)
