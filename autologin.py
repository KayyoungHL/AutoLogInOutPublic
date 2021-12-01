import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from imap_tools import MailBox
import json
import os
import webbrowser
import sys

#####################################################
##     크롬 버전에 맞는 크롬드라이버 반드시 구비      ##
#####################################################

def login(headless=False, only=False):
    # json data 입력
    if getattr(sys, 'frozen', False):
        #test.exe로 실행한 경우,test.exe를 보관한 디렉토리의 full path를 취득
        curr_path = os.path.dirname(os.path.abspath(sys.executable))
    else:
        #python test.py로 실행한 경우,test.py를 보관한 디렉토리의 full path를 취득
        curr_path = os.path.dirname(os.path.abspath(__file__))
    with open(curr_path+"/.id.json", encoding="UTF-8") as f:
        info = json.loads(f.read())

    # 0. 크롬 실행 아래 주석은 headless. 
    # 실제로 켜지는 것을 볼 순 없지만 background에서 동작한다.
    options = webdriver.ChromeOptions()
    options.headless = headless
    browser = webdriver.Chrome(curr_path+"/chromedriver.exe", options=options)
    # browser = webdriver.Chrome(curr_path+"/chromedriver.exe") 

    # 1. 코드스테이츠 이동
    browser.get("https://urclass.codestates.com/")

    # 2. 로그인 버튼 클릭
    browser.find_element(By.CLASS_NAME, "css-1i5o0f9").click()
    browser.find_element(By.CLASS_NAME, "login-form__button--kakao").click() # 카카오 로그인 버튼

    # 3. ID, PW 입력
    browser.find_element(By.ID, "id_email_2").send_keys(info["kakao"]["email"])
    browser.find_element(By.ID, "id_password_3").send_keys(info["kakao"]["password"])

    # 4. 로그인 버튼 클릭
    browser.find_element(By.CLASS_NAME, "btn_confirm").click()

    time.sleep(3)

    # 5. Gmail 로그인
    mailbox = MailBox('imap.gmail.com', 993)
    mailbox.login(info["gmail"]["email"],info["gmail"]["password"],initial_folder="INBOX")

    # 6. 첫 번째 메일 불러오기(로그인인증메일)
    for msg in mailbox.fetch(limit=1, reverse=True):
        source = msg.html

    # 7. bs4로 html 문서 파싱해서 로그인 인증 링크 구하기
    soup = BeautifulSoup(source, "html.parser")
    x = soup.find("a", class_="mcnButton")["href"] # 인증 링크
    
    if only:
        browser.close()
        browser.quit()
        chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(chrome_path).open(x)
        
    else:
        browser.get(x)
        return browser


if __name__ == "__main__":
    browser = login(headless=True, only=True)
    browser.close()
    browser.quit() 