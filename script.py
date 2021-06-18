from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import os
import json
import time
import pandas as pd

URL = 'https://nid.naver.com/nidlogin.login?url=http%3A%2F%2Fmail.naver.com%2F'


def main():
    try:
        driver = get_driver()
        driver.get(URL)
        config = get_config()
        login_naver_with_execute_script(driver, config['userId'], config['userPw'])
        time.sleep(5)

        lineCount = 30
        maxCount = 30
        allMail = 1200
        pageCount = 15

        a = []
        b = []
        c = []
        for i in range(2, pageCount):
            s = str(i)
            url2 = 'https://mail.naver.com/#%7B%22fClass%22%3A%22list%22%2C%22oParameter%22%3A%7B%22page%22%3A%22' + s \
                   + '%22%2C%22sortField%22%3A%221%22%2C%22sortType%22%3A%220%22%2C%22folderSN%22%3A%220%22%2C%22type' \
                     '%22%3A%22%22%2C%22isUnread%22%3Afalse%7D%7D '
            driver.get(url2)
            get_mail_list(driver.page_source, a, b, c)

        raw_data = {'보낸 사람': a, '제목': b, '발송 시간': c}
        raw_data = pd.DataFrame(raw_data)
        raw_data.to_excel(excel_writer='data.xlsx')

    except Exception as e:
        print(str(e))
    else:
        print("Main process is done.")
    finally:
        os.system("Pause")
        driver.quit()


def get_config():
    try:
        with open('config.json') as json_file:
            json_data = json.load(json_file)
    except Exception as e:
        print('Error in reading config file, {}'.format(e))
        return None
    else:
        return json_data


def login_naver_with_execute_script(driver, id, pw):
    script = "                                      \
    (function execute(){                            \
        document.querySelector('#id').value = '" + id + "'; \
        document.querySelector('#pw').value = '" + pw + "'; \
    })();"
    driver.execute_script(script)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input.btn_global"))
    )
    element.click()
    return False


def get_mail_list(page_source, a, b, c):
    soup = BeautifulSoup(page_source, "html.parser")
    div_list = soup.select("ol.mailList > li > div.mTitle")
    date_list = soup.select("ol.mailList > li > ul.mInfo.split_cell")
    for (div, date) in zip(div_list, date_list):
        soup = BeautifulSoup(str(div), "html.parser")
        soup2 = BeautifulSoup(str(date), "html.parser")
        title = soup.select_one("div.name > a").text
        subject = soup.select_one("div.subject > a:nth-of-type(1) > span > strong").text
        send_date = soup2.select_one("li.iDate").text
        print("{} / {} / {}".format(title, subject, send_date))
        a.append(title)
        b.append(subject)
        c.append(send_date)


def get_driver():
    driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    driver.implicitly_wait(3)
    return driver


if __name__ == '__main__':
    main()
