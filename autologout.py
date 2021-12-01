import time
import autologin
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def logout(headless):
    # 1~7. 로그인
    browser = autologin.login(headless=headless, only=False)

    # 8. 프로필 사진 마우스 오버
    actions = ActionChains(browser)
    actions.move_to_element(browser.find_element(By.CLASS_NAME, "icon__profile-avatar")).perform()

    # 9. 로그아웃 버튼 클릭
    browser.find_element(By.CLASS_NAME, "anticon-export").click()

    time.sleep(1)

    browser.close()
    browser.quit() 


if __name__ == "__main__":
    logout()