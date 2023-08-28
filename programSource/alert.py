# 이메일로 이벤트 발생을 알려줌
import smtplib
from email.mime.text import MIMEText

def alertMail(label, file_name):
    # label 별로 이벤트 설정
    # label = int(label)
    # if label == 0:
    #     event = 'awake'
    # if label == 1:
    #     event = 'drowsy'
    
    # (*)보낼 메일의 내용과 제목
    #content = "%s 이벤트가 발생했습니다.\n파일 %s 로 저장되었습니다." % (event, file_name)
    content = "%s 이벤트가 발생했습니다.\n파일 %s 로 저장되었습니다." % (label, file_name)
    title = '이벤트가 발생'

    msg = MIMEText(content)
    msg['Subject'] = title

    # (*)메일의 발신자 메일 주소, 수신자 메일 주소, 앱비밀번호(발신자) 
    sender = 'boocam500@gmail.com'
    receiver = 'k4n9jun3@gmail.com'
    # app_password = 'cjuxmynyckbztsvz' # Windows
    app_password = 'fnkfvzeoccxhtumh' # Mac

    # 세션 생성
    with smtplib.SMTP('smtp.gmail.com', 587) as s:
        # TLS 암호화
        s.starttls()

        # 로그인 인증과 메일 보내기
        s.login(sender, app_password)
        s.sendmail(sender, receiver, msg.as_string())
