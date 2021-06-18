from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pyperclip

# 크롬 웹 드라이버의 경로를 설정합니다.
driver = webdriver.Chrome('/usr/local/bin/chromedriver')
driver.implicitly_wait(3)

url = "https://nid.naver.com/nidlogin.login"
# phantomjs 드라이버 실행
browser = webdriver.PhantomJS()
browser.implicitly_wait(3)

# url 읽어들이고 로그인
browser.get(url)
element_id = browser.find_element_by_id("id")  # id 텍스트 입력 상자
element_id.clear()
element_pw = browser.find_element_by_id("pw")  # pw 텍스트 입력 상자
element_pw.clear()

element_id.send_keys("아이디").
element_pw.send_keys("비밀번호")

button = browser.find_element_by_css_selector("input.btn_global[type=submit]")
button.submit()

browser.get("https://mail.naver.com/")

titles = browser.find_elements_by_css_selector("strong.mail_title")

for title in titles:
    print(title.text)

browser.quit()
