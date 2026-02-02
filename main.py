import os
import smtplib
from email.mime.text import MIMEText

def send_test_email():
    # 수집 대신 강제로 테스트용 데이터를 만듭니다.
    test_content = (
        "주토피아 2|150000|25.5\n"
        "검은 수녀들|85000|18.2\n"
        "캡틴 아메리카|72000|15.1\n"
        "미키 17|54000|12.8\n"
        "알라딘 2|41000|10.5"
    )
    
    msg = MIMEText(test_content)
    msg['Subject'] = "[KOBIS_SEAT] 일일 리포트"
    msg['From'] = os.environ['GMAIL_USER']
    msg['To'] = os.environ['GMAIL_USER']
    
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.environ['GMAIL_USER'], os.environ['GMAIL_APP_PASSWORD'])
            smtp.send_message(msg)
        print("🚀 테스트 메일 발송 성공!")
    except Exception as e:
        print(f"❌ 발송 실패: {e}")

if __name__ == "__main__":
    send_test_email()
