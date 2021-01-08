import cv2
import time
import random
import pyautogui as pag
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.parse import quote_plus
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


# 시작 시간과 종료 시간을 측정
def timer():
    now = time.localtime()
    return now


# Chrome Driver 를 이용하여 인스타그램 URL 에 접속
def init_driver(now):
    options = Options()
    time.sleep(random.uniform(1, 2))
    base_url = 'https://www.instagram.com'
    driver = webdriver.Chrome('/Users/parkseongwon/PycharmProjects/pythonProject/chromedriver', chrome_options=options)
    driver.set_window_position(0, 0)
    driver.set_window_size(800, 900)
    driver.get(base_url)
    print('인스타그램 접속 완료: ', end='')
    print('{0}/{1}/{2} {3}:{4}'.format(now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min))
    time.sleep(random.uniform(3, 5))
    return driver


# 아이디와 비밀번호를 입력 후 로그인
def user_login(driver):
    username = '아이디입력'
    input_id = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[0]
    input_id.clear()
    input_id.send_keys(username)
    password = '비밀번호입력'
    input_pw = driver.find_elements_by_css_selector('input._2hvTZ.pexuQ.zyHYP')[1]
    input_pw.clear()
    input_pw.send_keys(password)
    input_pw.submit()
    print('로그인 완료: {0}'.format(username))
    time.sleep(random.uniform(8, 10))


# 팝업버튼 누르기
def user_popup_cl(driver):
    # 정보 다음에 저장하기 버튼
    login_later_button = driver.find_elements_by_css_selector('div.cmbtv')[0]
    login_later_button.click()
    time.sleep(random.uniform(3, 5))
    # 알람 끄기 버튼
    alam_later_button = driver.find_elements_by_css_selector('div.mt3GC')[0]
    alam_later_button.click()
    time.sleep(random.uniform(3, 5))


# 인스타에 키워드 검색 (랜덤 선택)
def user_search(driver):
    key_word_list = ['맞팔', '맞팔해요', '맞팔환영', '맞팔선팔환영', '좋반', '셀스타그램', '선팔', '선팔하면맞팔', '좋아요반사']
    random_num = random.randint(0, len(key_word_list) - 1)
    base_url = 'https://www.instagram.com/explore/tags/'
    keyword = key_word_list[random_num]
    search_url = quote_plus(keyword)
    driver.get(base_url + search_url)
    print('현재 키워드: #{0}'.format(keyword))
    time.sleep(random.uniform(8, 10))


# 최근 게시글의 첫번째 피드를 선택
def feed_click(driver):
    feed = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[2]/div/div[1]/div[1]/a')
    feed.send_keys(Keys.ENTER)
    time.sleep(random.uniform(3, 5))
    print('최근 게시글의 첫번째 피드 선택 완료')


# 게시글 분석
def feed_text(driver):
    time.sleep(random.uniform(3, 5))
    # 현재 페이지 html 정보 가져오기
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    # 본문 내용 가져오기
    try:
        content = soup.select('div.C4VMK > span')[0].text
    except:
        content = ' '
    # 본문 내에 광고로 의심되는 키워드가 있는지 확인
    ad = ad_block(content)
    return ad


# 광고인지 아닌지 여부
def ad_block(content):
    ad_list = ['광고', '명품', '미러', '본계', '협찬', '현금', '할인', '혜택', '고객', '직수입',
               '만원', '속눈썹', '왁싱', '레플', '레플리카', '24시간문의', '퀄리티', '첫방문', '예약', '부계',
               '소개계정', '주문', '방문해주시는', '문의', 'DM', '네일샵', '피어싱샵', '정상영업', '정상운영']
    ad = 0
    for example in ad_list:
        if example in content:
            print('광고 차단 : {0}'.format(content))
            ad = 1
            break
    if ad == 0:
        print('광고 아님 : {0}'.format(content))
    return ad


# 사진을 분석하기 위하여 스크린샷
def recognize_face():
    face_recog = 0
    time.sleep(random.uniform(3, 5))
    pag.screenshot('feedphoto.png', region=(60, 350, 850, 1200))
    print('스크린 캡처 완료')
    # 이미지 파일 경로 지정
    image_file = '/Users/parkseongwon/PycharmProjects/pythonProject/feedphoto.png'
    cascade_file = "/Users/parkseongwon/PycharmProjects/pythonProject/haarcascade_frontalface_alt.xml"
    # 이미지 파일 로드
    image = cv2.imread(image_file)
    # Gray Scale 로 변환
    image_gs = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(cascade_file)
    # 얼굴 인식하기
    face_list = cascade.detectMultiScale(image_gs, scaleFactor=1.1, minNeighbors=1, minSize=(150, 150))
    # 얼굴이 인식되었을 경우
    if len(face_list) > 0:
        print('얼굴 인식 완료')
        face_recog = 1
    else:
        print('얼굴 인식 실패')
    return face_recog


# 좋아요 버튼 클릭 / 댓글 달기 / 팔로우 하기
def insta_auto(driver, count, face_recog):
    like_error = like_click(driver)
    if like_error != 1:
        comment_click(driver, face_recog)
        follow_error = follow_click(driver)
        if follow_error != 1:
            count += 1
            print('현재까지 팔로우 한 사람 : {}'.format(count))
    return count


# 좋아요 누르기
def like_click(driver):
    time.sleep(random.uniform(3, 6))
    error = 0
    like = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[1]/span[1]/button')
    likebtn = driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > div.eo2As '
                                                  '> section.ltpMr.Slqrh > span.fr66n > button > div > span > svg ')
    likebtn = likebtn.get_attribute('aria-label')
    try:
        like_count = driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > '
                                                         'div.eo2As > section.EDfFK.ygqzn > div > div > button > span')
        like_int = int(like_count.text)
    except:
        print('좋아요 개수를 알 수 없는 게시물')
        like_int = 0
    if like_int > 150:
        print('좋아요 실패 : 너무 많은 좋아요 개수')
        error = 1
    elif likebtn != '좋아요':
        print('좋아요 실패 : 이미 좋아요를 누른 게시물')
        error = 1
    else:
        like.send_keys(Keys.ENTER)
        print('좋아요 완료 : {} 개'.format(like_int + 1))
    return error


# 게시글에 댓글 달기
def comment_click(driver, face_recog):
    noface_comment_list = ['안녕하세요! 선팔하고 갑니다!', '잘 나왔네요! 소통해요!', '사진이 잘 나왔네요! 맞팔부탁드려요!',
                           '사진이 잘 나왔네요! 선팔하고 갑니다!', '잘 보고 갑니다! 제 게시글도 확인 해 주세요!', '잘 보고 갑니다!',
                           '너무 잘 나왔어요! 맞팔해주세요!', '소통해요! 선팔하고 갑니다!', '좋아요 누르고 갑니다! 총총=3',
                           '사진 잘 봤습니다! 소통해요!']
    face_comment_list = ['잘 보고 갑니다! 제 피드에도 놀러와 주세요!', '사진 잘 나왔네요! 팔로우 하고 갑니다!',
                         '잘 나온 사진이네요! 좋아요 누르고 갑니다!', '팔로우하고 갑니다! 좋반해주세요!', '사진이 잘 나왔네요! 좋은 하루 보내세요!',
                         '소통해요! 팔로우 누르고 갑니다!', '이쁜 사진 보고 갑니다! 좋은 하루 보내세요!', '사진이 잘 나왔어요! 맞팔 기다릴게요!']
    time.sleep(random.uniform(3, 10))
    # 얼굴이 사진에 존재하지 않는 경우
    if face_recog == 0:
        comment_choose = random.randint(0, len(noface_comment_list) - 1)
        comment_txt = noface_comment_list[comment_choose]
    else:
        comment_choose = random.randint(0, len(face_comment_list) - 1)
        comment_txt = face_comment_list[comment_choose]
    comment = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/div[3]/section[3]/div/form/textarea')
    ac = webdriver.ActionChains(driver)
    ac.move_to_element(comment)
    ac.click()
    ac.pause(random.uniform(3, 7))
    ac.send_keys(comment_txt)
    ac.pause(random.uniform(2, 5))
    ac.send_keys(Keys.ENTER)
    ac.perform()
    print('댓글 달기 완료 : {}'.format(comment_txt))


# 팔로우 버튼 클릭하기
def follow_click(driver):
    time.sleep(random.uniform(2, 7))
    error = 0
    follow = driver.find_element_by_xpath('/html/body/div[5]/div[2]/div/article/header/div[2]/div[1]/div[2]/button')
    followbtn = driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.zZYga > div > article > '
                                                    'header > div.o-MQd > div.PQo_0 > div.bY2yH > button')
    followbtn = followbtn.text
    if followbtn != '팔로우':
        error = 1
        print('팔로우 실패 : 이미 팔로우 중인 유저')
    else:
        follow.send_keys(Keys.ENTER)
        print('팔로우 완료')
    return error


# 주제어를 바꿀지의 여부
def keyword_change():
    change = 0
    random_num = random.randint(1, 100)
    if random_num <= 5:
        print('키워드를 변경합니다.')
        change = 1
    else:
        print('현재 키워드로 계속 진행합니다.')
    return change


# 다음 게시글로 이동
def next_click(driver):
    print('다음 게시글로 넘어갑니다.\n')
    time.sleep(random.uniform(3, 6))
    next_feed = driver.find_element_by_css_selector('body > div._2dDPU.CkGkG > div.EfHg9 > '
                                                    'div > div > a._65Bje.coreSpriteRightPaginationArrow')
    ac = webdriver.ActionChains(driver)
    ac.move_to_element(next_feed)
    ac.click()
    ac.perform()
