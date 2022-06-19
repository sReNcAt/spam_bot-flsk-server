# spam_bot-flsk-server

로스트아크 유틸리티인 스팸봇의 API 서버입니다.

https://api.losonsil.com/search/<캐릭터명>

으로 작동을 하며 로스트아크 공식홈페이지의 전투정보실을 크롤링하여 json형태로 가공하여 

추후 본인의 다른 서드파트에서 사용하기 위하여 개발되었습니다.

# 실행환경 - Docker-compose

해당 코드는 설계부터 여러 환경의 서버에서 작동시키기 위하여 Docker-compose를 사용하여 관리하기 위하여 Dockerfile이 존재합니다.

최초 개발당시 Ubuntu 18.04 x64 서버에서 작동하였으며 현재 소모하는 리소스가 적어 ARMv7의 라즈베리파이4 (Ubuntu) 위에서 작동하고있습니다.

# 기능

해당 프로젝트의 기초 기능 설계는

캐릭터 전투정보실검색 (기본정보, 레벨, 장비, 각인, 보석, 카드)

마리샵 현재 목록

거래소 가격 목록

위와 같은 기능을 중점으로 두었으나 로스트아크의 공식홈페이지 거래소 접근에 로그인 권한이 추가됨에 따라 현재 작동하지 않고 있습니다.
