# ⚡ AI 포켓몬 트레이너 이력서 & 포트폴리오 빌더
> **Pokémon Trainer Edition - AI Resume & Portfolio Builder**  
> 나의 파트너 포켓몬과 함께 합격률 100%의 전설적인 커리어 스펙을 완성해 보세요! 🎮🔴⚪

---

## 📖 프로젝트 소개

본 프로젝트는 **Google Gemini API**와 **Flask**를 기반으로 지원자의 경험과 경력을 분석하여, 완성도 높은 **국문 이력서(Resume)** 및 **포트폴리오(Portfolio)**를 자동 생성해 주는 웹 애플리케이션입니다.

지원자가 선택한 **10종의 파트너 포켓몬**의 핵심 특성과 장점을 비즈니스 품격을 잃지 않으면서 자연스럽게 지원자의 강점으로 녹여내는 독창적인 프롬프트 엔지니어링이 적용되어 있습니다.

---

## ✨ 주요 기능

1. **🐾 10종의 파트너 포켓몬 모티브 역량 매칭**
   - **피카츄**: 빠른 실행력과 10만 볼트급의 적극적인 열정
   - **파이리**: 꺼지지 않는 불꽃 같은 끈기와 도전 정신
   - **꼬부기**: 다양한 환경에 유연하게 적응하는 문제 해결력
   - **이상해씨**: 탄탄한 기본기와 무궁무진한 성장 잠재력
   - **이브이**: 상황에 맞춰 빠르게 진화하는 다재다능한 스킬셋
   - **잠만보**: 어떤 위기 상황에서도 흔들리지 않는 든든한 안정감
   - **리자몽**: 목표를 향해 거침없이 돌파하는 강력한 주도성과 리더십
   - **팬텀**: 기존 틀을 깨는 번뜩이는 창의력과 전략적 센스
   - **뮤츠**: 데이터와 논리에 기반한 정밀한 분석력과 압도적 전문성
   - **루카리오**: 팀원의 니즈를 정확히 파악하는 깊은 공감과 직관적 소통

2. **🎯 2가지 생성 모드 지원 (프롬프트 엔지니어링)**
   - **일반 모드 (Mode A)**: 직관적이고 깔끔한 표준형 이력서 & 포트폴리오 초안
   - **전문가 모드 (Mode B)**: 테크 리크루터 관점에서 **STAR 기법**(Situation, Task, Action, Result)과 정량적 성과 수치 중심으로 고도화된 작성

3. **🎨 맞춤형 어조(Tone) 선택**
   - 전문적이고 신뢰감을 주는 비즈니스 어조 (Professional)
   - 자신감 넘치고 성과 중심의 주도적 어조 (Confident)
   - 창의적이고 독창적인 감각적 어조 (Creative)
   - 친근하고 협력적인 팀워크 중심 어조 (Friendly)

4. **⚡ 직관적인 사용자 경험 (UX)**
   - 2열 반응형 레이아웃 (입력 폼 & 실시간 결과창)
   - Markdown 결과 렌더링 및 원클릭 클립보드 복사 / 텍스트 다운로드 기능
   - 파트너 포켓몬 인터랙티브 카드 선택 UI

---

## 🛠 기술 스택

- **Backend**: Python 3, Flask 3.0.3, python-dotenv
- **AI Model**: Google Gemini API (`gemini-3.6-flash` / `google-generativeai`)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript, Pretendard Font

---

## 📁 프로젝트 구조

```text
resume-builder/
├── app.py                 # Flask 백엔드 서버 및 Gemini API 연동 로직
├── requirements.txt       # 의존성 패키지 목록
├── .env.example           # 환경변수 예시 파일
├── .env                   # API 키 설정 파일 (비공개)
├── templates/
│   └── index.html         # 메인 웹 페이지 마크업
├── static/
│   ├── css/
│   │   └── style.css      # 포켓몬 테마 카드 덱 및 전체 반응형 스타일
│   └── js/
│       └── app.js         # 비동기 요청, UI 인터랙션 및 결과 처리 스크립트
└── README.md              # 프로젝트 안내 문서
```

---

## 🚀 시작하기

### 1. 사전 요구사항
- Python 3.10 이상
- [Google AI Studio](https://aistudio.google.com/)에서 발급받은 **Gemini API Key**

### 2. 가상환경 구성 및 패키지 설치

```bash
# 가상환경 생성 (최초 1회)
python -m venv venv

# 가상환경 활성화 (Windows PowerShell 기준)
.\venv\Scripts\Activate.ps1

# 필수 라이브러리 설치
pip install -r requirements.txt
```

> **PowerShell 실행 정책 오류 발생 시:**
> ```powershell
> Set-ExecutionPolicy -Scope Process Bypass
> .\venv\Scripts\Activate.ps1
> ```

### 3. 환경 변수 설정
프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 발급받은 Gemini API 키를 입력합니다:

```ini
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. 로컬 서버 실행

```bash
python app.py
```

서버가 정상적으로 구동되면 브라우저에서 아래 주소로 접속합니다:
👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 📝 라이선스
이 프로젝트는 개인 학습 및 비상업적 용도로 자유롭게 활용하실 수 있습니다.
