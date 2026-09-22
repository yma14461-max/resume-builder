// ==========================================================================
// AI Resume & Portfolio Builder - 클라이언트 스크립트 (app.js)
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
    // 1. 주요 DOM 엘리먼트 참조
    const form = document.getElementById("resume-form");
    const nameInput = document.getElementById("name");
    const jobTitleInput = document.getElementById("job-title");
    const toneSelect = document.getElementById("tone");
    const experienceInput = document.getElementById("experience");
    const projectsInput = document.getElementById("projects");
    const submitBtn = document.getElementById("submit-btn");
    const errorMessage = document.getElementById("error-message");

    const loadingSpinner = document.getElementById("loading-spinner");
    const placeholderBox = document.getElementById("placeholder-box");
    const resultCard = document.getElementById("result-card");
    const resultContent = document.getElementById("result-content");
    const copyBtn = document.getElementById("copy-btn");
    const downloadBtn = document.getElementById("download-btn");
    const partnerPokemonInput = document.getElementById("partner-pokemon");
    const pokemonCards = document.querySelectorAll(".pokemon-card");
    const loadingPokeImg = document.getElementById("loading-poke-img");
    const loadingTitle = document.getElementById("loading-title");
    const resultPokeBadge = document.getElementById("result-poke-badge");
    const partnerTag = document.getElementById("partner-tag");
    let rawMarkdownResult = "";

    // 🐾 파트너 포켓몬 카드 클릭 이벤트 등록
    if (pokemonCards.length > 0) {
        pokemonCards.forEach(card => {
            card.addEventListener("click", () => {
                pokemonCards.forEach(c => c.classList.remove("active"));
                card.classList.add("active");
                const pokeName = card.dataset.name;
                const pokeId = card.dataset.id;
                const pokeCheer = card.dataset.cheer;
                if (partnerPokemonInput) partnerPokemonInput.value = pokeName;

                const pokeImgUrl = `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${pokeId}.png`;
                if (loadingPokeImg) loadingPokeImg.src = pokeImgUrl;
                if (loadingTitle) loadingTitle.textContent = pokeCheer;
                if (resultPokeBadge) resultPokeBadge.src = pokeImgUrl;
                if (partnerTag) partnerTag.textContent = `파트너: ${pokeName}`;
            });
        });
    }

    // 2. 에러 메시지 표시/숨김 함수
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove("hidden");
    }

    function hideError() {
        errorMessage.textContent = "";
        errorMessage.classList.add("hidden");
    }

    // 3. 로딩 상태 전환 함수
    function setLoading(isLoading) {
        if (isLoading) {
            hideError();
            loadingSpinner.classList.remove("hidden");
            placeholderBox.classList.add("hidden");
            resultCard.classList.add("hidden");
            submitBtn.disabled = true;
            submitBtn.querySelector(".btn-text").textContent = "AI 트레이너가 작성하는 중...";
        } else {
            loadingSpinner.classList.add("hidden");
            submitBtn.disabled = false;
            submitBtn.querySelector(".btn-text").textContent = "AI 이력서 & 포트폴리오 생성하기";
        }
    }

    // 4. 폼 제출(Submit) 이벤트 리스너
    form.addEventListener("submit", async (e) => {
        e.preventDefault(); // 기본 폼 제출(페이지 새로고침) 방지
        hideError();

        // 4-1. 입력값 가져오기
        const name = nameInput.value.trim();
        const jobTitle = jobTitleInput.value.trim();
        const tone = toneSelect.value;
        const promptType = document.querySelector('input[name="prompt_type"]:checked')?.value || "A";
        const experience = experienceInput.value.trim();
        const projects = projectsInput.value.trim();

        // 4-2. 프론트엔드 유효성 검증 (Frontend Validation)
        if (!name) {
            showError("성명을 입력해 주세요.");
            nameInput.focus();
            return;
        }
        if (!jobTitle) {
            showError("지원 직무를 입력해 주세요.");
            jobTitleInput.focus();
            return;
        }
        if (!experience) {
            showError("주요 경력 사항을 입력해 주세요.");
            experienceInput.focus();
            return;
        }
        if (!projects) {
            showError("수행 프로젝트 내용을 입력해 주세요.");
            projectsInput.focus();
            return;
        }

        // 4-3. 로딩 상태 활성화
        setLoading(true);

        // 4-4. 백엔드 Flask API(/generate)로 비동기 요청 전송
        try {
            const response = await fetch("/generate", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    name: name,
                    job_title: jobTitle,
                    partner_pokemon: partnerPokemonInput ? partnerPokemonInput.value : "피카츄",
                    tone: tone,
                    prompt_type: promptType,
                    experience: experience,
                    projects: projects
                })
            });

            const data = await response.json();

            if (!response.ok || !data.success) {
                throw new Error(data.error || "이력서 생성 중 문제가 발생했습니다.");
            }

            // 4-5. 결과 화면 출력 (마크다운 파싱 렌더링)
            rawMarkdownResult = data.result;
            if (typeof marked !== "undefined") {
                resultContent.innerHTML = marked.parse(rawMarkdownResult);
            } else {
                resultContent.textContent = rawMarkdownResult;
            }
            resultCard.classList.remove("hidden");
            placeholderBox.classList.add("hidden");

        } catch (error) {
            console.error("생성 요청 오류:", error);
            showError(error.message || "서버와 통신하는 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.");
            placeholderBox.classList.remove("hidden");
        } finally {
            setLoading(false);
        }
    });

    // 5. 결과 복사 기능 (클립보드 API)
    copyBtn.addEventListener("click", async () => {
        const textToCopy = rawMarkdownResult || resultContent.innerText;
        if (!textToCopy) return;

        try {
            await navigator.clipboard.writeText(textToCopy);
            const originalText = copyBtn.textContent;
            copyBtn.textContent = "✅ 복사 완료!";
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        } catch (err) {
            console.error("복사 실패:", err);
            alert("클립보드 복사에 실패했습니다. 직접 드래그하여 복사해 주세요.");
        }
    });

    // 6. 마크다운(.md) 파일 다운로드 기능
    downloadBtn.addEventListener("click", () => {
        const textToDownload = rawMarkdownResult || resultContent.innerText;
        if (!textToDownload) return;

        // 텍스트를 Blob 객체로 변환
        const blob = new Blob([textToDownload], { type: "text/markdown;charset=utf-8" });
        const downloadUrl = URL.createObjectURL(blob);

        // 가상 <a> 태그를 만들어 파일 다운로드 트리거
        const tempLink = document.createElement("a");
        const applicantName = nameInput.value.trim() || "지원자";
        tempLink.href = downloadUrl;
        tempLink.download = `${applicantName}_이력서_포트폴리오.md`;
        document.body.appendChild(tempLink);
        tempLink.click();

        // 사용 완료된 객체 정리
        document.body.removeChild(tempLink);
        URL.revokeObjectURL(downloadUrl);
    });
});
