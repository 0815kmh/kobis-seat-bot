import os
import time
import smtplib
from email.mime.text import MIMEText
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def get_kobis_seat_data():
    """KOBIS에서 일별 좌석수와 좌석판매율 1~5위를 가져오는 함수"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=chrome_options)
    
    url = "https://www.kobis.or.kr/kobis/business/stat/boxs/findDailySeatTicketList.do"
    driver.get(url)
    time.sleep(5) # 테이블 로딩 대기
    
    seat_data = []
    try:
        # 데이터 행 추출 (1~5위)
        rows = driver.find_elements(By.CSS_SELECTOR, "#tbody_0 tr")[:5]
        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 13:
                name = cols[1].text.strip()
                seat_cnt = cols[9].text.replace(',', '') # 좌석수
                seat_rate = cols[13].text.replace('%', '') # 판매율
                seat_data.append(f"{name}|{seat_cnt}|{seat_rate}")
    except Exception as e:
        print(f"데이터 추출 중 오류 발생: {e}")
    
    driver.quit()
    return "\n".join(seat_data)

def send_email(content):
    """수집된 데이터를 파트너님 지메일로 발송하는 함수"""
    if not content:
        print("수집된 데이터가 없어 메일을 보내지 않습니다.")
        return

    msg = MIMEText(content)
    msg['Subject'] = "[KOBIS_SEAT] 일일 리포트"
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['GMAIL_USER']
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['GMAIL_USER'], os.environ['GMAIL_APP_PASSWORD'])
            smtp.send_message(msg)
        print("메일 발송 성공!")
    except Exception as e:
        print(f"메일 발송 실패: {e}")

if __name__ == "__main__":
    print("🚀 데이터 수집 시작...")
    data = get_kobis_seat_data()
    send_email(data)
    print("🎉 모든 작업 완료!")
