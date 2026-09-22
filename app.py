import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv
import google.generativeai as genai

# 1. 로깅(Logging) 설정: 서버 콘솔에 요청과 오류를 시간대별로 기록
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# 2. .env 파일에서 환경변수 로드
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY가 .env 파일에 설정되어 있지 않습니다.")
else:
    logger.info("GEMINI_API_KEY가 성공적으로 로드되었습니다.")
    genai.configure(api_key=GEMINI_API_KEY)

# 3. Flask 웹 애플리케이션 초기화 (Vercel Serverless 및 로컬 호환 루트 디렉토리 지정)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

# 4. 프롬프트 생성 함수 (Prompt Engineering + 포켓몬 모티브)
def build_prompt(name, job_title, experience, projects, tone, prompt_type, partner_pokemon="피카츄"):
    tone_description = {
        "professional": "전문적이고 신뢰감을 주는 비즈니스 어조",
        "confident": "자신감 넘치고 주도적인 성과 중심 어조",
        "creative": "창의적이고 독창적인 감각적 어조",
        "friendly": "친근하고 협력적인 팀워크 중심 어조"
    }.get(tone, "전문적이고 명확한 어조")

    pokemon_strengths = {
        "피카츄": "빠른 실행력과 10만 볼트급의 적극적인 열정",
        "파이리": "꺼지지 않는 불꽃 같은 끈기와 도전 정신",
        "꼬부기": "다양한 환경에 유연하게 적응하는 문제 해결력",
        "이상해씨": "탄탄한 기본기와 무궁무진한 성장 잠재력",
        "이브이": "상황에 맞춰 빠르게 진화하는 다재다능한 스킬셋",
        "잠만보": "어떤 위기 상황에서도 흔들리지 않는 든든한 안정감",
        "리자몽": "목표를 향해 거침없이 돌파하는 강력한 주도성과 리더십",
        "팬텀": "기존 틀을 깨는 번뜩이는 창의력과 전략적 센스",
        "뮤츠": "데이터와 논리에 기반한 정밀한 분석력과 압도적 전문성",
        "루카리오": "팀원의 니즈를 정확히 파악하는 깊은 공감과 직관적 소통"
    }.get(partner_pokemon, "탁월한 열정과 성장 잠재력")

    if prompt_type == "B":
        # Prompt B: 전문가(Expert) 모드 - 정량적 성과 및 STAR 기법 기반
        system_instruction = f"""
당신은 최고 수준의 테크 리크루터이자 이력서/포트폴리오 전문 컨설턴트입니다.
제공된 지원자 정보를 바탕으로 채용 담당자의 시선을 사로잡을 수 있는 고품질의 국문 Resume(이력서)와 Portfolio(포트폴리오)를 Markdown 형식으로 작성해 주세요.

[작성 원칙]
1. 어조: {tone_description}를 일관되게 유지하세요.
2. 성과 중심: STAR 기법(Situation, Task, Action, Result)을 적용하고 구체적인 수치와 액션 위주로 기술하세요.
3. 전문성: 직무({job_title})에 맞는 핵심 키워드와 업계 표준 기술 용어를 적극적으로 활용하세요.
4. 모티브 반영: 지원자의 핵심 강점 키워드로 '{pokemon_strengths}' 특성을 역량 설명에 자연스럽고 설득력 있게 녹여내세요. (비즈니스 품격 유지)
5. 구성:
   - ## 1. 이력서 (Resume)
     - 기본 정보 및 프로필 요약 (강렬한 헤드라인)
     - 핵심 역량 (Core Competencies)
     - 경력 사항 (STAR 기반의 역할 및 성과 불렛포인트)
   - ## 2. 포트폴리오 (Portfolio)
     - 주요 프로젝트별 문제 정의, 해결 과정, 사용 기술, 핵심 기여도 및 결과
"""
    else:
        # Prompt A: 일반(General) 모드 - 깔끔하고 직관적인 표준 초안
        system_instruction = f"""
당신은 친절하고 유능한 취업 멘토입니다.
제공된 지원자 정보를 바탕으로 깔끔하고 완성도 높은 국문 Resume(이력서)와 Portfolio(포트폴리오)를 Markdown 형식으로 작성해 주세요.

[작성 원칙]
1. 어조: {tone_description}로 자연스럽게 작성하세요.
2. 가독성: 읽기 쉽고 직관적인 구조로 내용을 정리하세요.
3. 모티브 반영: 지원자의 특별한 강점으로 '{pokemon_strengths}' 특성을 역량 설명에 긍정적으로 녹여내세요.
4. 구성:
   - ## 1. 이력서 (Resume)
     - 자기소개 요약
     - 보유 기술 및 경험
     - 상세 경력 내용
   - ## 2. 포트폴리오 (Portfolio)
     - 프로젝트 개요, 주요 기능, 기여한 부분
"""

    prompt = f"""{system_instruction}

[지원자 정보]
- 성명: {name}
- 지원 직무: {job_title}
- 파트너 포켓몬 모티브: {partner_pokemon} ({pokemon_strengths})
- 주요 경력:
{experience}
- 수행 프로젝트:
{projects}

위 정보를 참고하여 즉시 제출 가능한 수준의 완벽한 국문 이력서와 포트폴리오를 Markdown 형식으로 출력해 주세요.
"""
    return prompt

# 5. 메인 홈 화면 라우트
@app.route("/")
def index():
    logger.info("메인 화면(/) 요청 수신")
    return render_template("index.html")

# 5-1. PWA 설정 파일 및 서비스 워커 서빙 라우트
@app.route("/manifest.json")
def manifest():
    return send_from_directory(app.static_folder, "manifest.json", mimetype="application/manifest+json")

@app.route("/sw.js")
def service_worker():
    return send_from_directory(app.static_folder, "sw.js", mimetype="application/javascript")

# 6. AI 생성 API 라우트
@app.route("/generate", methods=["POST"])
def generate():
    logger.info("이력서 및 포트폴리오 생성(/generate) 요청 수신")
    
    # 6-1. 요청 데이터 파싱
    data = request.get_json()
    if not data:
        logger.warning("요청 본문(JSON)이 비어 있습니다.")
        return jsonify({"success": False, "error": "요청 데이터가 올바르지 않습니다."}), 400

    # 6-2. 필드 추출
    name = data.get("name", "").strip()
    job_title = data.get("job_title", "").strip()
    partner_pokemon = data.get("partner_pokemon", "피카츄").strip()
    experience = data.get("experience", "").strip()
    projects = data.get("projects", "").strip()
    tone = data.get("tone", "professional").strip()
    prompt_type = data.get("prompt_type", "A").strip()

    # 6-3. 백엔드 입력값 검증 (Validation)
    if not name:
        logger.warning("검증 실패: 이름 누락")
        return jsonify({"success": False, "error": "이름을 입력해 주세요."}), 400
    if not job_title:
        logger.warning("검증 실패: 지원 직무 누락")
        return jsonify({"success": False, "error": "지원 직무를 입력해 주세요."}), 400
    if not experience:
        logger.warning("검증 실패: 경력 사항 누락")
        return jsonify({"success": False, "error": "경력 사항을 입력해 주세요."}), 400
    if not projects:
        logger.warning("검증 실패: 프로젝트 경험 누락")
        return jsonify({"success": False, "error": "프로젝트 경험을 입력해 주세요."}), 400

    # 6-4. API Key 설정 검증
    if not GEMINI_API_KEY:
        logger.error("Gemini API Key가 .env에 설정되지 않음")
        return jsonify({
            "success": False,
            "error": ".env 파일에 GEMINI_API_KEY가 설정되어 있지 않습니다. 키를 등록해 주세요."
        }), 500

    # 6-5. Gemini API 호출
    try:
        logger.info(f"Gemini API 호출 시작 - 지원자: {name}, 직무: {job_title}, 파트너: {partner_pokemon}, 모드: {prompt_type}")
        prompt = build_prompt(name, job_title, experience, projects, tone, prompt_type, partner_pokemon)

        # 최신 고성능 Gemini Flash 모델 사용 (gemini-3.6-flash)
        try:
            model = genai.GenerativeModel("gemini-3.6-flash")
            response = model.generate_content(prompt)
        except Exception as model_err:
            logger.warning(f"gemini-3.6-flash 실패, gemini-flash-latest로 재시도: {model_err}")
            model = genai.GenerativeModel("gemini-flash-latest")
            response = model.generate_content(prompt)

        result_text = response.text
        logger.info(f"Gemini API 생성 성공 - 글자 수: {len(result_text)}자")

        return jsonify({
            "success": True,
            "result": result_text
        })

    except Exception as e:
        logger.error(f"Gemini API 호출 중 오류 발생: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": f"AI 응답을 생성하는 중 오류가 발생했습니다: {str(e)}"
        }), 500

# 7. 서버 실행 진입점
if __name__ == "__main__":
    logger.info("Flask 웹 애플리케이션 시작: http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
