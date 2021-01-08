from utils import *
from selenium.common.exceptions import NoSuchElementException

# Main Function
if __name__ == "__main__":

    # 총 팔로우를 원하는 수
    max_iter = 1000

    # 한 가지 키워드에 대하여 몇 번 반복할 것인지 설정
    iter_count = 100

    # 현재 팔로우를 한 수
    follow_count = 0

    # 시작시간 종료시간 측정
    start = timer()

    # Chrome Driver 실행
    driver = init_driver(start)

    # 아이디와 비밀번호 입력
    user_login(driver)

    # 팝업창 닫기
    user_popup_cl(driver)

    while follow_count < max_iter:

        # 검색어 검색
        user_search(driver)

        # 첫번째 게시글 누르기
        feed_click(driver)

        # 여기에 반복문이 들어가야 함.
        for i in range(0, iter_count):

            # 분석을 위하여 게시글 데이터 수집
            ad = feed_text(driver)

            # 광고가 아닌 경우에만 진행
            if ad == 0:

                # 사진 속 얼굴 포함 여부
                face_recognize = recognize_face()

                # 좋아요 버튼 클릭 / 댓글 달기 / 팔로우 하기 및 다음 게시글로 이동
                try:
                    follow_count = insta_auto(driver, follow_count, face_recognize)
                    next_click(driver)

                # 로딩 실패시 바로 다음 게시글로 이동
                except NoSuchElementException:
                    print('게시물 로딩 오류')
                    next_click(driver)

            # 광고일 경우 바로 다음 게시글로 이동
            elif ad == 1:
                next_click(driver)

            # 현재 키워드로 계속 진행할지 결정
            change = keyword_change()

            if change == 1:
                break

    # 종료시간 종료시간 측정
    end = timer()

    # 요약
    print('시작 시간 : ', end='')
    print('{0}/{1}/{2} {3}:{4}'.format(start.tm_year, start.tm_mon, start.tm_mday, start.tm_hour, start.tm_min))
    print('종료 시간 : ', end='')
    print('{0}/{1}/{2} {3}:{4}'.format(end.tm_year, end.tm_mon, end.tm_mday, end.tm_hour, end.tm_min))
    print('총 팔로우한 사람 수 : {0}'.format(follow_count))
