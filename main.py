from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from datetime import datetime, timedelta
import sys, os

#2021-01-22 ver1.0
#금요일날 사용한다는 가정하에 수동적으로 움직이며, 마스터리 카드가 2종류일때 오류를 보이는 현상이 있다.

# 크롬 드라이버
option = webdriver.ChromeOptions()
option.add_experimental_option("excludeSwitches", ["enable-logging"])
# 실행 프로그램 배포시 활성화
driver = webdriver.Chrome(os.path.join(sys._MEIPASS, "chromedriver.exe"), options=option)
# 디버깅 테스트 시 활성화
# driver = webdriver.Chrome("chromedriver.exe", options=option)
driver.implicitly_wait(10) # seconds

# 자기를 노트북 환경을 위한 자기만의 해상도 세팅(디버깅시에만 활성화 하기)
# driver.set_window_size(1366, 600)

def xpath_wait(your_xpath) :
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, your_xpath)))

def input_user() :
    print("본 프로그램은 크롬 브라우저가 설치되어있어야 합니다.")
    print("본 프로그램은 크롬 브라우저 버전 91.0.4472.19에 맞춰져있습니다.")
    print("#설정 - Chorme정보에서 사용자 환경의 Chorme 브라우저 환경 확인 가능")

    id = input("대교 눈높이 성장판 ID : ")
    pw = input('대교 눈높이 성장판 PW : ')

    return  id, pw


def check_auth(id, pw) :
    driver.get('https://pan.daekyo.co.kr/login.do')
    # id, pw 입력 후 로그인
    driver.find_element_by_name('userId').send_keys(id)
    driver.find_element_by_name('password').send_keys(pw)
    driver.find_element_by_id('actLogin').click()

    # 경고창이 감지된다면 창을 닫고 로그인으로 재이동, 아니라면 홈페이지 접속
    try:
        driver.switch_to.alert.accept()
        driver.minimize_window()
        print("ID 또는 PW가 틀렸습니다. 다시 입력해주세요.")
        p_id, p_pw = input_user()
        check_auth(p_id, p_pw)
    except :
        driver.maximize_window()
        print("로그인 성공")
        print("메인 팝업창을 지웁니다.")
        time.sleep(3)
        ac = ActionChains(driver)
        ac.move_by_offset(50, 50)
        ac.click()
        ac.perform()
        print("이력진단 메뉴로 이동합니다.")
        time.sleep(3)
        # 체크리스트 항목으로 이동을 위한 상단 메뉴바 선택
        elements = driver.find_elements_by_css_selector('#header > div > div.gnbArea > ul > li')
        elements[1].click()

        # driver.find_element_by_xpath('//*[@id="datepicker"]').click()
        #
        # now = datetime.now()
        # monday = now - timedelta(days=now.weekday())
        # week_monday = monday.strftime("%d")
        # week_friday = int(week_monday) + 4
        # print("이번주 월요일은 {}일 입니다.".format(week_monday))
        # print("이번주 금요일은 {}일 입니다.".format(week_friday))
        #
        # day_list = driver.find_elements_by_class_name("ui-state-default")
        #
        # for i in range(0, int(format(len(day_list)))):
        #     if day_list[i].text == week_monday :
        #         day_list[i].click()
        #
        # time.sleep(2)

        # return week_monday, week_friday

def day_check_list() :
    print('미확인 체크리스트를 검사합니다.')
    # 체크리스트 미작성된 항목만 보기
    driver.find_element_by_xpath('//*[@id="sForm"]/div/ul/li[2]/div').click()

    time.sleep(2)
    # 미작성된 항목 갯수 저장
    no_submit_count = driver.find_element_by_xpath('//*[@id="container"]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[2]/span[2]').text
    print("미작성 체크리스트 항목 갯수 : " + no_submit_count)
    # 이번 요일에 체크할 항목이 없다면?
    if not int(no_submit_count) == 0:
        # 가장 상단에 위치하는 체크리스트 항목을 눌러 평가하는 화면 띄우기
        b_btn = driver.find_elements_by_class_name('btnBlue')
        b_btn[0].click()

        # 현재 페이지에서 iframe 을 찾기(레이어 팝업 추적)
        iframes = driver.find_element_by_tag_name('iframe')

        # 추적한 레이어 팝업으로 주 페이지 변환
        driver.switch_to.frame(iframes)
        # 남아 있는 체크리스트 수 만큼 반복
        for i in range(0, int(format(len(b_btn)))):
            try:
                # 3가지 체크 항목 모두 매우 좋음으로 선택
                driver.find_element_by_xpath('//*[@id="uiCheckList"]/li[1]/div[2]/div[1]/label').click()
                #time.sleep(1)
                driver.find_element_by_xpath('// *[ @ id = "uiCheckList"] / li[2] / div[2] / div[1] / label').click()
                #time.sleep(1)
                driver.find_element_by_xpath('// *[ @ id = "uiCheckList"] / li[3] / div[2] / div[1] / label').click()
                #체크항목 저장
                driver.find_element_by_xpath('// *[ @ id = "ui_btn_save"]').click()
                time.sleep(2)
                #나타나는 alert 확인 누르기
                driver.switch_to.alert.accept()
                user_name = driver.find_element_by_xpath('//*[@id="popHeader"]/div[1]').text
                print(user_name + " 체크리스트 점검 완료! 남은 횟수 : [" + str(int(no_submit_count)-1 - i) + "]")
                time.sleep(1)
            except :
                print("정보가 입력되지 않았거나, 오류가 발생했습니다.")
                #만약에 아직 미평가라면?
                #아무것도 안함
            #어찌됬던 평가가 없던 평가를 완료하던 다음 학생으로
            # driver.find_element_by_xpath('// *[ @ id = "uiNext"]').click()
            driver.find_element_by_xpath('// *[ @ id = "uiNext"]').send_keys(Keys.ENTER)


        # 한 요일에 대한 체크리스트 검사가 끝나면 나오기
        driver.find_element_by_xpath('//*[@id="ui_btn_cancel"]').send_keys(Keys.ENTER)
    print('체크리스트 검사 끝!')


def day_mastery_list() :
    print('미발급 마스터리 카드를 검사합니다.')
    # 미확인 마스터리 카드 검사
    driver.find_element_by_xpath('//*[@id="sForm"]/div/ul/li[3]/div/label').click()
    time.sleep(2)
    # 총 미확인 된 마스터리 카드 갯수 추출
    no_submit_count = driver.find_element_by_xpath(
        '//*[@id="container"]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[2]/span[2]').text
    print("미발급 마스터리 카드 갯수 : " + no_submit_count)
    time.sleep(1)
    if not int(no_submit_count) == 0:
        # 가장 상단에 위치하는 체크리스트 항목을 눌러 평가하는 화면 띄우기
        y_btn = driver.find_elements_by_class_name('btnYellow')

        for i in range(0, int(format(len(y_btn)))):
            try:
                time.sleep(1)
                driver.find_element_by_class_name('btnYellow').click()
                # 현재 페이지에서 iframe 을 찾기(레이어 팝업 추적)
                iframes = driver.find_element_by_tag_name('iframe')
                # 추적한 레이어 팝업으로 주 페이지 변환
                driver.switch_to.frame(iframes)

                # 남아 있는 마스터리 수 만큼 반복할 리스트 생성
                y_btn_list = driver.find_elements_by_class_name('btnIssue')
                time.sleep(2)
                y_btn_list[0].click()
                time.sleep(3)
                # 나타나는 alert 확인 누르기
                driver.switch_to.alert.accept()
                user_name = driver.find_element_by_xpath('//*[@id="popHeader"]/div[1]').text
                print(user_name + " 마스터리 카드 점검 완료! 남은 횟수 : [" + str(int(no_submit_count)-1 - i) + "]")
                # 팝업창을 없애기 위해 빈 공간 아무대나 클릭
                driver.find_element_by_xpath('// *[ @ id = "popCont"] / div[2] / div[3] / div[3] / a').click()
            except :
                print("정보가 입력되지 않았거나, 오류가 발생했습니다.")
                #만약에 아직 미평가라면?
                #아무것도 안함
                driver.find_element_by_xpath('// *[ @ id = "popCont"] / div[2] / div[3] / div[3] / a').click()

    print('마스터리 카드 발급 끝!')

def day_check_change(day) :
    if day == 0:
        driver.find_element_by_xpath('// *[ @ id = "container"] / div / div / div[3] / div[1] / div / div / div / div / div[1] / div[3] / a[1]').click()
        print("월요일로 이동합니다.")
        time.sleep(2)
    if day == 1:
        driver.find_element_by_xpath('//*[@id="container"]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[3]/a[2]').click()
        print("화요일로 이동합니다.")
        time.sleep(2)

    if day == 2:
        driver.find_element_by_xpath('// *[ @ id = "container"] / div / div / div[3] / div[1] / div / div / div / div / div[1] / div[3] / a[3]').click()
        print("수요일로 이동합니다.")
        time.sleep(2)

    if day == 3:
        driver.find_element_by_xpath('// *[ @ id = "container"] / div / div / div[3] / div[1] / div / div / div / div / div[1] / div[3] / a[4]').click()
        print("목요일로 이동합니다.")
        time.sleep(2)

    if day == 4:
        driver.find_element_by_xpath('// *[ @ id = "container"] / div / div / div[3] / div[1] / div / div / div / div / div[1] / div[3] / a[5]').click()
        print("금요일로 이동합니다.")
        time.sleep(2)

# ID : 32098192
# PW : jkluio1*


#ID, PW 입력
p_id, p_pw = input_user()


#입력한 ID, PW 기반으로 홈페이지 접속, 틀릴경우 ID, PW 입력창 재호출
check_auth(p_id, p_pw)


for i in range(0, 5):
    print("")
    day_check_change(i)
    time.sleep(1)
    day_check_list()
    day_mastery_list()
    #다음 단계로 이동
    driver.find_element_by_xpath('//*[@id="container"]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div/a[2]').click()

print("")
print("이번 주에 대한 회원이력검사가 끝났습니다.")
print("10초 후 브라우저가 자동으로 닫힙니다.")
print("이번 주도 고생하셨습니다! 사랑해요 이현수 자기")
time.sleep(9)
driver.close()





