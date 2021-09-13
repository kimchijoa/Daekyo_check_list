try:
    #대교 홈페이지 접속
    driver.get('https://pan.daekyo.co.kr/login.do')
    # id, pw 입력 후 로그인
    pan_pwd = driver.find_element_by_id('password')
    driver.find_element_by_name('userId').send_keys(p_id)
    # driver.find_element_by_name('password').send_keys('dyoexo0704*')
    driver.find_element_by_name('password').send_keys(p_pw)
    driver.find_element_by_id('actLogin').click()
    # 나타나는 alert 확인 누르기
    # driver.switch_to.alert.accept()
    # 팝업창을 없애기 위해 빈 공간 아무대나 클릭
    ac = ActionChains(driver)
    ac.move_by_offset(50,50)
    ac.click()
    ac.perform()
    # 체크리스트 항목으로 이동을 위한 상단 메뉴바 선택
    elements = driver.find_elements_by_css_selector('#header > div > div.gnbArea > ul > li')
    elements[1].click()
    #요일 이동하기
    #요일 이동은 월 ~ 금 까지다 이 버젼에서는 금요일날 해당 매크로를 실행한다는 가정하에 만들것이다.
    for i in range(0, 4):
        driver.find_element_by_xpath('//*[@id="container"]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div/a[1]').click()
        print('요일 이동 -1')
        time.sleep(3)

    #월요일 부터 해당 로직 시작, 체크리스트 미항목 확인, 마스터리 카드 미발급 확인이 끝난 후, 다음 요일로 넘어간다.
    for a in range(0, 5):
        # 체크리스트 미작성된 항목만 보기
        time.sleep(2)
        print('이번 요일의 미확인 체크리스트를 검사합니다.')
        driver.find_element_by_xpath('//*[@id="sForm"]/div/ul/li[2]/div/label').click()
        time.sleep(2)
        # 미작성된 항목 갯수 저장
        test = driver.find_element_by_xpath('//*[@id="container"]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[2]/span[2]').text
        print("미작성 체크리스트 항목 갯수 : " + test)

    if not test == '0':
        # 가장 상단에 위치하는 체크리스트 항목을 눌러 평가하는 화면 띄우기
        b_btn = driver.find_elements_by_class_name('btnBlue')
        print('수정해야할 버튼 : {}'.format(len(b_btn)))
        b_btn[0].click()

        # 현재 페이지에서 iframe 을 찾기(레이어 팝업 추적)
        iframes = driver.find_element_by_tag_name('iframe')

        # 추적한 레이어 팝업으로 주 페이지 변환
        driver.switch_to.frame(iframes)
        # 남아 있는 체크리스트 수 만큼 반복
    for i in range(0, int(format(len(b_btn)))):
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
        time.sleep(1)
        # 다음 체크리스트 항목으로 이동하기
        driver.find_element_by_xpath('// *[ @ id = "uiNext"]').click()

        #한 요일에 대한 체크리스트 검사가 끝나면 나오기
        driver.find_element_by_xpath('//*[@id="ui_btn_cancel"]').click()
        print('이번 요일에 대한 체크리스트 검사 끝!')

        time.sleep(1)
        print('이번 요일의 미발급 마스터리 카드를 검사합니다.')
        #미확인 마스터리 카드 검사
        driver.find_element_by_xpath('//*[@id="sForm"]/div/ul/li[3]/div/label').click()
        print('미확인 마스터리 카드 선택')
        time.sleep(3)
        #총 미확인 된 마스터리 카드 갯수 추출
        test02 = driver.find_element_by_xpath('//*[@id="container"]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[2]/span[2]').text
        print("미발급 마스터리 카드 갯수 : " + test02)
        time.sleep(3)

    if not test02 == '0':
        # 가장 상단에 위치하는 체크리스트 항목을 눌러 평가하는 화면 띄우기
        y_btn = driver.find_elements_by_class_name('btnYellow')
        print('발급해야 할 마스터리 카드 큰 갯수 : {}'.format(len(y_btn)))

    for i in range(0, int(format(len(y_btn)))):
        driver.find_element_by_class_name('btnYellow').click()
        # 현재 페이지에서 iframe 을 찾기(레이어 팝업 추적)
        iframes = driver.find_element_by_tag_name('iframe')
        # 추적한 레이어 팝업으로 주 페이지 변환
        driver.switch_to.frame(iframes)

        # 남아 있는 체크리스트 수 만큼 반복할 리스트 생성
        y_btn_list = driver.find_elements_by_class_name('btnIssue')

        print("현재 창 발급해야할 마스터리 카드 갯수 : {}".format(len(y_btn_list)))

        for j in range(0, int(format(len(y_btn_list)))):
            print(j)
            time.sleep(2)
            y_btn_list[j].click()
            time.sleep(3)
            # 나타나는 alert 확인 누르기
            driver.switch_to.alert.accept()
            # 팝업창을 없애기 위해 빈 공간 아무대나 클릭
            driver.find_element_by_xpath('// *[ @ id = "popCont"] / div[2] / div[3] / div[3] / a').click()

            time.sleep(2)
            # 다음 마스터리카드 항목으로 이동하기
            # driver.find_element_by_xpath('// *[ @ id = "uiNext"]').click()

        # 한 요일에 대한 마스터리 카드 발급이 끝나면 나오기
        # driver.find_element_by_xpath('//*[@id="popCont"]/div[2]/div[3]/div[3]/a').click()
        print('이번 요일에 대한 마스터리 카드 발급 끝!')
        driver.find_element_by_xpath('//*[@id="container"]/div/div/div[3]/div[1]/div/div/div/div/div[1]/div[1]/div/a[2]').click()
        print("다음 요일로 이동합니다.")

        #마스터리 카드 2개 인식 안됨

except Exception as e:
    print(e)

finally:
    # 드라이버 종료
    driver.close()
    print('닫기')

