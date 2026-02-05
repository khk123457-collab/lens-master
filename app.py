import streamlit as st
import pandas as pd
import os
import time
import plotly.graph_objects as go
import qrcode
from io import BytesIO
import base64

# ==============================================================================
# 1. 설정 및 디자인 (Toss Style CSS)
# ==============================================================================
st.set_page_config(page_title="Lens Master", page_icon="👁️", layout="mobile") # 모바일 레이아웃 최적화

st.markdown("""
<style>
    /* 전체 폰트 및 배경 */
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F2F4F6; }
    
    /* 메인 컨테이너 */
    .main-container { padding: 20px; }
    
    /* 토스 스타일 카드 */
    .toss-card {
        background-color: white;
        border-radius: 20px;
        padding: 24px;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        cursor: pointer;
        transition: transform 0.2s;
    }
    .toss-card:hover { transform: scale(1.02); }
    .card-title { font-size: 20px; font-weight: 700; color: #191F28; margin-bottom: 8px; }
    .card-desc { font-size: 14px; color: #8B95A1; }
    
    /* 헤더 스타일 */
    .header-title { font-size: 28px; font-weight: 800; color: #191F28; margin-bottom: 10px; }
    .header-sub { font-size: 16px; color: #6B7684; margin-bottom: 30px; }
    
    /* 질문지 스타일 */
    .q-box { background: white; padding: 20px; border-radius: 15px; margin-bottom: 20px; }
    .q-text { font-size: 16px; font-weight: 600; color: #333; margin-bottom: 15px; }
    
    /* 버튼 스타일 커스텀 (동그라미 느낌) */
    div[role="radiogroup"] > label > div:first-child { display: none; }
    div[role="radiogroup"] { display: flex; justify-content: space-between; gap: 10px; }
    div[role="radiogroup"] label { 
        background: #F2F4F6; 
        border-radius: 50%; 
        width: 40px; 
        height: 40px; 
        display: flex; 
        align-items: center; 
        justify-content: center;
        font-weight: bold;
        color: #6B7684;
        border: 1px solid transparent;
        transition: 0.2s;
    }
    div[role="radiogroup"] label:hover { background: #E8F3FF; color: #3182F6; }
    div[role="radiogroup"] label[data-checked="true"] { 
        background: #3182F6; 
        color: white; 
        box-shadow: 0 4px 10px rgba(49, 130, 246, 0.4);
    }

    /* 결과 페이지 스타일 */
    .result-header { background: #3182F6; color: white; padding: 40px 20px; border-radius: 0 0 25px 25px; margin: -20px -20px 20px -20px; text-align: center; }
    .mbti-tag { background: rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 20px; font-size: 14px; display: inline-block; margin-bottom: 10px; }
    .mbti-hero { font-size: 48px; font-weight: 900; margin-bottom: 10px; }
    
    /* 제품 카드 */
    .prod-card { border: 2px solid #E5E8EB; border-radius: 15px; padding: 20px; margin-bottom: 15px; background: white; position: relative; }
    .prod-badge { position: absolute; top: -10px; right: 20px; background: #3182F6; color: white; padding: 5px 12px; border-radius: 15px; font-size: 12px; font-weight: bold; }
    .why-box { background: #F9FAFB; padding: 15px; border-radius: 10px; margin-top: 15px; border-left: 4px solid #3182F6; }
    .why-title { font-size: 13px; font-weight: bold; color: #3182F6; margin-bottom: 5px; }
    .why-text { font-size: 13px; color: #4E5968; line-height: 1.5; }

    /* QR 코드 */
    .qr-container { text-align: center; margin-top: 40px; padding: 30px; background: white; border-radius: 20px; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 데이터 및 로직 (Backend)
# ==============================================================================
@st.cache_data
def load_data():
    try:
        # 데이터가 없으면 가상의 데이터를 생성합니다 (에러 방지용)
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'data', 'lens_db_v1.xlsx')
        if os.path.exists(file_path):
            return pd.read_excel(file_path, sheet_name='Sheet1')
        else:
            return None
    except: return None

# 세션 상태 초기화 (페이지 네비게이션용)
if 'page' not in st.session_state: st.session_state['page'] = 'home'
if 'answers' not in st.session_state: st.session_state['answers'] = {}
if 'mbti_result' not in st.session_state: st.session_state['mbti_result'] = None

def go_to(page): st.session_state['page'] = page

# ==============================================================================
# 3. 화면 구성: 메인 홈 (Home)
# ==============================================================================
if st.session_state['page'] == 'home':
    st.markdown("<div class='header-title'>LENS MASTER</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-sub'>내 눈에 딱 맞는 인생 렌즈 찾기</div>", unsafe_allow_html=True)

    # 메뉴 1: Eye-MBTI (핵심 기능)
    if st.button("🧬 나에게 맞는 렌즈는? (Eye-MBTI)", use_container_width=True):
        go_to('mbti_test')

    st.markdown("---")

    # 메뉴 2: 렌즈 평가 (준비중)
    st.button("⭐ 렌즈 평가 및 리뷰 (준비중)", disabled=True, use_container_width=True)
    
    # 메뉴 3: 모든 렌즈 보기 (준비중)
    st.button("👓 모든 렌즈 도감 (준비중)", disabled=True, use_container_width=True)
    
    # 메뉴 4: 내 주변 안경원
    st.button("📍 내 주변 안경원 찾기 (준비중)", disabled=True, use_container_width=True)

    st.info("💡 <b>개발자 노트:</b> 현재 'Eye-MBTI' 기능이 활성화되어 있습니다. 정밀 분석을 체험해보세요!")


# ==============================================================================
# 4. 화면 구성: 20문항 정밀 검사 (Test Page)
# ==============================================================================
elif st.session_state['page'] == 'mbti_test':
    st.markdown("<div class='header-title'>정밀 시력 성향 검사</div>", unsafe_allow_html=True)
    st.progress(50) # 진행률 표시 (예시)

    # --- 질문 리스트 (5개씩 4개 분야 = 20문항) ---
    questions = {
        "E/I (환경)": [
            ("Q1. 하루에 디지털 기기(폰/PC)를 8시간 이상 보나요?", "env_1"),
            ("Q2. 히터나 에어컨이 강한 건조한 실내에 주로 있나요?", "env_2"),
            ("Q3. 야외 활동(캠핑, 골프, 등산)을 자주 즐기나요?", "env_3"),
            ("Q4. 미세먼지가 많거나 바람이 부는 곳에서 일하나요?", "env_4"),
            ("Q5. 조명이 어두운 곳이나 야간에 운전을 많이 하나요?", "env_5")
        ],
        "S/N (예민도)": [
            ("Q6. 오후 4시만 되면 눈이 뻑뻑하고 충혈되나요?", "sen_1"),
            ("Q7. 렌즈를 꼈을 때 이물감(모래알 느낌)을 잘 느끼나요?", "sen_2"),
            ("Q8. 조금만 피곤해도 눈이 쉽게 붓거나 아픈가요?", "sen_3"),
            ("Q9. 화장품이나 땀이 눈에 들어가면 극도로 따갑나요?", "sen_4"),
            ("Q10. 난시(글자가 퍼져 보임)가 심하다고 느끼나요?", "sen_5")
        ],
        "T/F (가치관)": [
            ("Q11. 눈 건강을 위해서라면 가격은 상관없나요?", "val_1"),
            ("Q12. 최신 기술이 들어간 신제품을 써보고 싶나요?", "val_2"),
            ("Q13. '가성비'가 제품 선택의 1순위인가요?", "val_3"),
            ("Q14. 1+1 행사나 할인 이벤트가 중요한가요?", "val_4"),
            ("Q15. 한 번 산 렌즈는 브랜드 변경 없이 쭉 쓰나요?", "val_5")
        ],
        "P/J (숙련도)": [
            ("Q16. 렌즈를 한 번에 끼고 빼는 데 능숙한가요?", "exp_1"),
            ("Q17. 렌즈 세척이나 관리가 귀찮아서 원데이를 선호하나요?", "exp_2"),
            ("Q18. 내 눈의 도수나 베이스커브 정보를 알고 있나요?", "exp_3"),
            ("Q19. 과거에 렌즈 적응에 실패한 경험이 있나요?", "exp_4"),
            ("Q20. 안경원에서 추천해주는 대로 믿고 구매하나요?", "exp_5")
        ]
    }

    answers = {}
    
    # 질문 출력 로직
    for category, q_list in questions.items():
        st.subheader(f"📂 {category}")
        for q_text, key in q_list:
            st.markdown(f"<div class='q-text'>{q_text}</div>", unsafe_allow_html=True)
            # 1~5점 동그라미 선택지
            answers[key] = st.radio(
                label=key, 
                options=[1, 2, 3, 4, 5], 
                horizontal=True, 
                key=key, 
                label_visibility="collapsed"
            )
        st.markdown("---")

    if st.button("결과 분석하기", type="primary", use_container_width=True):
        st.session_state['answers'] = answers
        go_to('result')
        st.rerun()

# ==============================================================================
# 5. 화면 구성: 결과 리포트 & QR (Result Page)
# ==============================================================================
elif st.session_state['page'] == 'result':
    ans = st.session_state['answers']
    
    # --- [알고리즘] 점수 계산 (가중치 적용) ---
    # E(야외) vs I(실내/디지털) -> I가 높으려면: Q1(High), Q2(High), Q3(Low)
    score_i = (ans['env_1'] + ans['env_2'] + (6-ans['env_3']) + ans['env_4'] + ans['env_5']) 
    type_i = "I" if score_i >= 15 else "E" # 기준점

    # S(예민) vs N(둔감) -> S가 높으려면: 점수가 높을수록 예민
    score_s = sum([ans[f'sen_{i}'] for i in range(1, 6)])
    type_s = "S" if score_s >= 15 else "N"

    # T(성능/투자) vs F(가성비) -> T가 높으려면: Q11(High), Q13(Low)
    score_t = (ans['val_1'] + ans['val_2'] + (6-ans['val_3']) + (6-ans['val_4']) + ans['val_5'])
    type_t = "T" if score_t >= 15 else "F"

    # P(숙련/지식) vs J(초보/의존) -> P가 높으려면: Q16(High), Q18(High)
    score_p = (ans['exp_1'] + (6-ans['exp_2']) + ans['exp_3'] + (6-ans['exp_4']) + (6-ans['exp_5']))
    type_p = "P" if score_p >= 15 else "J"

    mbti_res = f"{type_i}{type_s}{type_t}{type_p}"

    # MBTI 상세 설명 데이터
    mbti_details = {
        "ISTP": {"title": "깐깐한 디지털 전문가", "desc": "하루 종일 모니터를 보며 눈을 혹사하지만, 최고급 스펙으로 눈을 보호합니다. 작은 건조감도 용납하지 않는 프로페셔널!"},
        "ENFP": {"title": "자유로운 아웃도어 러버", "desc": "야외 활동을 즐기며 가성비와 편리함을 중시합니다. 렌즈 관리가 귀찮은 당신에겐 막 쓰기 좋은 제품이 딱!"},
        "ISFJ": {"title": "신중한 안전 제일주의자", "desc": "눈이 예민하고 걱정이 많아 검증된 제품만 씁니다. 처음엔 적응하기 쉬운 편안한 렌즈가 필요해요."},
        "ENTJ": {"title": "효율 중심의 리더", "desc": "성능과 가격의 밸런스를 완벽하게 맞춥니다. 남들이 좋다는 건 다 써봐야 직성이 풀리는 얼리어답터!"}
    }
    # (나머지 유형은 기본값 처리)
    persona = mbti_details.get(mbti_res, {"title": "밸런스형 스마트 컨슈머", "desc": "나만의 기준을 가지고 합리적인 소비를 하는 타입입니다. 상황에 맞춰 유연하게 렌즈를 선택하세요!"})

    # --- [화면 출력] ---
    st.markdown(f"""
    <div class="result-header">
        <span class="mbti-tag">Your Eye-Type</span>
        <div class="mbti-hero">{mbti_res}</div>
        <div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">{persona['title']}</div>
        <div style="font-size: 16px; opacity: 0.9; max-width: 600px; margin: 0 auto;">{persona['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    # --- [제품 추천 로직] ---
    # 실제 엑셀 데이터가 있다면 여기서 필터링, 없으면 예시 데이터
    st.markdown("### 🏆 당신을 위한 인생 렌즈 Best 3")
    
    # (예시 로직: 실제로는 DB에서 가져옴)
    recs = []
    if type_s == "S": # 예민하면 프리미엄
        recs.append({"name": "알콘 데일리스 토탈원", "price": "69,000", "tag": "건조감해결 1위", "reason": "눈이 예민하신 편이라 일반 렌즈는 오후에 뻑뻑할 수 있습니다. 이 제품은 표면이 물로 되어 있어 눈에 닿는 느낌이 거의 없습니다.", "why_price": "워터그라디언트라는 특수 기술이 들어가서 제조 단가가 높지만, 인공눈물 값을 아낄 수 있습니다."})
        recs.append({"name": "아큐브 오아시스 원데이", "price": "63,000", "tag": "디지털 피로 감소", "reason": "디지털 기기 사용량이 많으시군요. 눈물 층을 안정화시켜 화면을 오래 봐도 침침해지지 않게 돕습니다.", "why_price": "실리콘 소재 중에서도 가장 검증된 베스트셀러라 가격 방어가 잘 되는 편입니다."})
    else: # 둔감하면 가성비
        recs.append({"name": "쿠퍼비전 클래리티", "price": "45,000", "tag": "가성비 갑", "reason": "눈이 건강하신 편이라 굳이 비싼 걸 쓰지 않아도 됩니다. 이 제품은 실리콘 소재라 산소는 잘 통하면서 가격은 착합니다.", "why_price": "광고비를 줄이고 제품력에 집중해서 가격 거품을 뺐습니다."})
    
    # 3개 채우기용 (MBTI에 따라 달라져야 함)
    if type_t == "T":
        recs.append({"name": "바슈롬 울트라 원데이", "price": "55,000", "tag": "고해상도 시야", "reason": "최신 기술에 관심이 많으시네요. 16시간 착용해도 수분을 96% 유지하는 신기술이 적용되었습니다.", "why_price": "최신 공법이 적용된 신제품 라인업입니다."})
    else:
        recs.append({"name": "미광 클리어 원데이", "price": "32,000", "tag": "초저가", "reason": "가성비를 1순위로 꼽으셨네요. 운동하거나 여행 갈 때 막 쓰고 버리기에 이만한 게 없습니다.", "why_price": "구형 소재이지만 기본 기능에 충실하여 가격을 극한으로 낮췄습니다."})

    # 카드 출력
    for idx, item in enumerate(recs[:3]):
        st.markdown(f"""
        <div class="prod-card">
            <div class="prod-badge">{idx+1}위 추천</div>
            <div style="font-size: 18px; font-weight: bold; color: #333;">{item['name']}</div>
            <div style="font-size: 14px; color: #666; margin-bottom: 10px;">예상가격: {item['price']}원</div>
            <div class="why-box">
                <div class="why-title">🧐 왜 이 렌즈인가요? (Why It Fits)</div>
                <div class="why-text">{item['reason']}</div>
                <div class="why-title" style="margin-top:10px; color:#E11D48;">💰 가격의 비밀 (Price Logic)</div>
                <div class="why-text">{item['why_price']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- [QR 코드 생성] ---
    st.markdown("### 📲 안경사 전용 처방전 (QR)")
    
    # QR에 담을 정보 (텍스트)
    qr_data = f"""
    [LENS MASTER Rx]
    User Type: {mbti_res}
    --- Answers ---
    Env(Digital): {ans['env_1']}
    Env(Dry): {ans['env_2']}
    Sen(Dry): {ans['sen_1']}
    Sen(Astig): {ans['sen_5']}
    Val(Price): {ans['val_3']}
    Exp(Fail): {ans['exp_4']}
    ---------------
    Rec: {recs[0]['name']}
    """
    
    # QR 생성
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(qr_data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # 이미지를 바이트로 변환하여 HTML로 표시
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    st.markdown(f"""
    <div class="qr-container">
        <div style="font-weight:bold; margin-bottom:10px;">안경사님께 이 화면을 보여주세요</div>
        <img src="data:image/png;base64,{img_str}" width="150">
        <div style="font-size:12px; color:#999; margin-top:10px;">스캔 시 고객님의 문진 데이터가 표시됩니다.</div>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("처음으로 돌아가기", use_container_width=True):
        go_to('home')
        st.rerun()
