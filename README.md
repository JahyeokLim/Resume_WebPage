# 임재혁 포트폴리오 사이트

임베디드 소프트웨어 개발자 임재혁의 이력/프로젝트 소개 웹 사이트. Django 기반.

자세한 요구사항은 [PRD.txt](PRD.txt), 작업 이력은 [CHANGELOG.txt](CHANGELOG.txt) 참고.
전체 구조 한눈에 보기는 [docs/architecture.svg](docs/architecture.svg) 참고.

## 주요 기능

- 홈: 프로필, 경력/학력 타임라인, 기술 스택, 대표 프로젝트, 이력서 PDF 다운로드
- 프로젝트 소개: 목록 + 상세 페이지 (개요/역할/아키텍처/이미지·동영상, 커버 썸네일, 기간 표시)
- 문의하기: 방문자가 남긴 문의는 로그인한 관리자만 볼 수 있는 문의함(Inbox)에 쌓임
- 한국어/영어 다국어 지원, 라이트/다크 테마 토글
- Django Admin을 통한 콘텐츠 관리 (별도 로그인 화면 없이 `/admin/`으로 관리)

## 요구 사항

- Python 3.10+
- Django, Pillow (`pip install django pillow`)

이 환경은 `python3-venv`가 없어 가상환경 대신 `pip install --user`로 패키지를 설치했습니다.
가상환경을 만들 수 있는 환경이라면 아래 대신 `python3 -m venv venv && source venv/bin/activate`를
먼저 실행한 뒤 패키지를 설치하는 쪽을 권장합니다.

## 로컬 실행 방법

```bash
# 1. 의존성 설치
pip install django pillow

# 2. DB 마이그레이션
python3 manage.py migrate

# 3. 관리자 계정 생성
python3 manage.py createsuperuser

# 4. (선택) 샘플 데이터 채우기 — 이력/기술스택/프로젝트 예시 데이터를 넣어줍니다
python3 manage.py seed_demo

# 5. 개발 서버 실행
python3 manage.py runserver 0.0.0.0:8000
```

실행 후 브라우저에서 다음 주소로 접속:

- 홈: <http://localhost:8000/ko/> (영어는 `/en/`)
- 프로젝트 목록: <http://localhost:8000/ko/projects/>
- 문의하기: <http://localhost:8000/ko/contact/>
- 관리자 페이지: <http://localhost:8000/admin/>

## 콘텐츠 수정 방법

이 사이트는 별도의 콘텐츠 편집 UI가 없고, **Django Admin**에서 모든 데이터를 관리합니다.

1. 사이트 푸터의 작은 "Admin" 링크를 눌러 로그인
2. 로그인하면 헤더 메뉴에 **편집** 버튼이 나타남 — 클릭하면 Admin으로 이동
3. Admin에서 프로필, 경력/학력, 기술 스택, 프로젝트, 받은 문의(Inbox) 등을 수정

일반 방문자에게는 로그인/편집 관련 메뉴가 전혀 보이지 않습니다.

## 프로젝트 구조

```
config/      Django 프로젝트 설정 (settings, urls)
profiles/    홈/프로필/경력/기술스택 앱
projects/    프로젝트 소개 앱
contact/     문의하기 + 관리자 전용 문의함(Inbox) 앱
templates/   HTML 템플릿 (base.html + 앱별 템플릿)
static/css/  스위스 그리드 테마 CSS (라이트/다크 모드 포함)
locale/      한국어→영어 UI 문구 번역 (django.po/.mo)
```

## 다국어 번역 관련 참고

이 환경에는 GNU gettext 도구(`msguniq` 등)가 없어 표준
`python manage.py makemessages` / `compilemessages`를 쓸 수 없었습니다.
대신 `pip install polib`로 설치한 순수 파이썬 라이브러리로 `locale/en/LC_MESSAGES/django.po`를
직접 작성하고 `.mo`까지 컴파일했습니다. gettext가 설치된 환경이라면 이후에는
표준 `makemessages`/`compilemessages` 워크플로우로 전환해도 됩니다.

UI 고정 문구(메뉴, 버튼 등)만 이 번역 파일의 대상이며, Admin에서 입력하는 실제
콘텐츠(이름, 소개글, 프로젝트 설명 등)는 모델에 있는 `_ko`/`_en` 필드에 각각 직접
입력해야 합니다.

## 배포 전 체크리스트

- [ ] 실제 프로필 사진, 이력서 PDF, 프로젝트 데이터로 교체 (Admin에서 입력)
- [ ] 관리자 비밀번호를 안전한 값으로 재설정
- [ ] `config/settings.py`의 `SECRET_KEY`를 환경 변수로 분리
- [ ] `DEBUG = False`, `ALLOWED_HOSTS`에 실제 도메인 설정
- [ ] 정적/미디어 파일 서빙 방식 정리 (WhiteNoise 등)
- [ ] 프로덕션 DB 결정 (SQLite → PostgreSQL 등, 호스팅 환경에 따라)
