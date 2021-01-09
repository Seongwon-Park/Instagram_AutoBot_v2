# Instagram_AutoBot_v2
Using selenium of python

## Youtube Link
Video : [[Youtube](https://youtu.be/SNVXSpRYyGc)]

# 목표
* 인스타그램 봇을 이용하여 "맞팔", "선팔하면 맞팔해요" 등의 태그를 올린 유저를 
 "팔로우 및 좋아요 그리고 댓글" 을 남김으로써 내 계정의 노출도를 증가하여 보고자 한다.


# 알고리즘
1. selenium을 이용하여 인스타그램에 자동으로 접속한다.
2. 태그 목록 중 임의로 한개를 골라 그 태그로 검색을 한다.
3. 첫 번째 게시글을 클릭한 후, 좋아요와 댓글 그리고 팔로우를 한다.
 - 이 때 좋아요의 개수가 150개가 넘는 게시글은 대상에서 제외하였다. (지난 버전에서의 0%의 맞팔률)
 4. 이미 좋아요, 팔로우를 한 유저일 경우 다음 게시글로 바로 이동한다.
 - 광고로 추측되는 글에 경우에도 다음 게시글로 바로 이동한다.
 5. 무작위로 검색태그를 변경하여 진행한다.
 
 # 시작 및 결과
 * 2020년 12월 24일 (목) 22:00 ~ 2020년 12월 25일 (금) 10:00 (종료)
 
 * 시작시점의 팔로워 / 팔로잉 : ( 217 / 500 )
 * 종료시점의 팔로워 / 팔로잉 : ( 307 / 1020)
 
 * 팔로잉 증가량 : 520 명
 * 총 팔로워 수: 90 명
 
 * 맞팔 비율 :  18 % (430 명은 맞팔을 하지 않았다.)

# 결론
* 기존의 버전과 다르게 댓글을 달아주는 기능을 넣었더니 많은 유저의 반응이 있었다.
 - 기존 대비 2배 넘는 맞팔 비율
* 좀 더 세분화하여 상황에 맞는 댓글을 달 수 있도록 계획한다.
 - ex) 고양이에 대한 태그 -> 귀여움, 음식에 대한 태그 -> 맛있음

# 참고 자료
[노마드코더 님의 유튜브] - https://www.youtube.com/watch?v=uUIFN0mHpE4&t=283s
