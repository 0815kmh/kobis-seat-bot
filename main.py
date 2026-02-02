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
    
    # [중요] 어제 날짜(2026-02-01) 데이터를 강제로 가져오도록 설정된 URL입니다.
    test_url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findDailySeatTicketList.do?sSearchFrom=2026-02-01&curPage=1"
    
    try:
        print(f"🌐 사이트 접속 중: {test_url}")
        driver.get(test_url)
        
        # 테이블이 나타날 때까지 최대 15초 대기
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#tbody_0 tr"))
        )
        time.sleep(5) 
        
        seat_data = []
        rows = driver.find_elements(By.CSS_SELECTOR, "#tbody_0 tr")
        
        if not rows or "데이터가 없습니다" in rows[0].text:
            print("⚠️ 수집 가능한 데이터가 없습니다.")
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
        print(f"❌ 오류 발생: {e}")
        return ""
    finally:
        driver.quit()

def send_email(content):
    if not content or len(content.strip()) < 5:
        print("ℹ️ 데이터가 유효하지 않아 메일을 보내지 않습니다.")
        return

    msg = MIMEText(content)
    msg['Subject'] = "[KOBIS_SEAT] 일일 리포트"
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['GMAIL_USER']
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['GMAIL_USER'], os.environ['GMAIL_APP_PASSWORD'])
            smtp.send_message(msg)
        print("🚀 메일 발송 성공!")
    except Exception as e:
        print(f"❌ 메일 발송 실패: {e}")

if __name__ == "__main__":
    print("🎬 테스트 수집 시작 (타겟: 2026-02-01)...")
    data = get_kobis_seat_data()
    print(f"📊 수집 결과:\n{data}")
    send_email(data)
    print("🏁 테스트 종료!")
