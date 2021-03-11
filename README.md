# 17-2st-shockx-backend
![main](https://user-images.githubusercontent.com/72085261/109430603-8ce3bf00-7a45-11eb-8123-e9eae234e756.gif)

'샥엑스'는 학습 목적으로 제작된 StockX 홈페이지를 클론 프로젝트입니다. 신발 리셀 중개 거래 업체 StockX 웹사이트 기본적인 기능들을 구현했습니다. 사용된 이미지는 전부 오픈 소스 이미지들 입니다. 

## 프로젝트 기간
2021.03.02(화) ~ 2021.03.12(금)

## 팀 구성
### 프론트엔드 
- 김민주
- 서유진
- 유승현
### 백엔드
- 김하성 (PM) 
- 송빈호 
- 조수아
- 조혜윤

## 사용한 기술 스택
- 프론트엔드: html, css, jsx, react
- 백엔드: Python, Django, MySQL, AQueryTool, Git, AWS, S3

## 프로젝트 진행 방식
- Trello, Slack 앱을 활용해 Scrum 방식으로 진행

## 내가 한 일들
https://velog.io/@markkimjr/SHockx
- 백엔드 팀원들이랑 같이 data 모델링 (AQueryTool 사용)
- 백엔드 팀원들이랑 같이 models.py 작성
- product/views.py 작성 (ProductListView GET, ProductDetailView GET)
- 상품 전체 리스트 나열 (필터링 기능, pagination) 구현
- 상품 상세페이지 구현
- product/tests.py 작성
- product/urls.py 작성 (REST API방식)

## 백엔드 구현 목록
#### 회원가입 & 로그인
- Bcrypt를 활용한 비밀번호 암호화
- JWT를 활용한 Access Token 발행
- 로그인 @decorator 
- Kakao API 사용하여 소셜 로그인 구현
#### 상품 리스트 나열
- Jordan 브랜드 신발 리스트 나열
- 신발 사이즈, 가격 별 상품 필터링
- pagination (limit, offset) 구현
#### 상품 상세페이지
- 모델별 상세페이지 리스트 나열 & detail 정보 전달
- 신발 사이즈 선택에 따라 상품 상세 정보 전달
#### 상품 주문/결제 
- 상품 성택하여 원하는 사이즈에 ask/bid 등록
- 매칭 ask랑 bid가 있을떄 order생성
- 주문 상태 저장

## Reference
- 이 프로젝트는 <a href="http://www.stockx.com">StockX</a> 사이트를 참조하여 학습목적으로 만들었습니다.
- 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.
