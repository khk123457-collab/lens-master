import streamlit as st
import pandas as pd
import time
import plotly.graph_objects as go
import qrcode
from io import BytesIO
import base64

# ==============================================================================
# 1. 설정 및 디자인 (Classic Blue Style)
# ==============================================================================
st.set_page_config(page_title="Lens Master Pro", page_icon="👁️", layout="centered")

st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F2F4F6; }
    
    .header-title { font-size: 28px; font-weight: 800; color: #191F28; margin-bottom: 5px; }
    .header-sub { font-size: 16px; color: #6B7684; margin-bottom: 30px; }
    
    /* 설명 박스 스타일 */
    .desc-box { background-color: #fff; padding: 20px; border-radius: 15px; border: 1px solid #E5E8EB; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
    .desc-title { font-size: 15px; font-weight: 700; color: #333; margin-bottom: 8px; }
    .desc-text { font-size: 13px; color: #6B7684; line-height: 1.6; margin-bottom: 4px; }
    .desc-highlight { color: #3182F6; font-weight: 600; background-color: #E8F3FF; padding: 2px 6px; border-radius: 4px;}

    .q-text { font-size: 16px; font-weight: 700; color: #333; margin-top: 30px; margin-bottom: 8px; }
    
    /* 점수 라벨 */
    .scale-labels { 
        display: flex; justify-content: space-between; 
        font-size: 12px; color: #8B95A1; font-weight: 500;
        padding: 0 8px; margin-bottom: 5px;
    }
    
    /* 라디오 버튼 스타일 */
    div[role="radiogroup"] { gap: 0; justify-content: space-between; margin-bottom: 20px; }
    div[role="radiogroup"] label {
        background-color: white !important; border: 1px solid #E5E8EB !important; border-radius: 50% !important;
        width: 45px; height: 45px; display: flex; justify-content: center; align-items: center;
        cursor: pointer; transition: all 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    div[role="radiogroup"] label p { font-size: 16px !important; margin: 0 !important; color: #6B7684 !important; }
    div[role="radiogroup"] label:hover { background-color: #F2F4F6 !important; transform: scale(1.1); }
    div[role="radiogroup"] label:has(input:checked) {
        background-color: #3182F6 !important; border-color: #3182F6 !important; box-shadow: 0 4px 10px rgba(49, 130, 246, 0.4);
    }
    div[role="radiogroup"] label:has(input:checked) p { color: white !important; font-weight: bold !important; }
    div[role="radiogroup"] label > div:first-child { display: none; }

    /* 결과 페이지 */
    .result-header { background: linear-gradient(135deg, #3182F6 0%, #1B64DA 100%); color: white; padding: 40px 20px; border-radius: 0 0 25px 25px; margin: -20px -20px 20px -20px; text-align: center; }
    .mbti-hero { font-size: 52px; font-weight: 900; margin: 10px 0; text-shadow: 0 4px 10px rgba(0,0,0,0.2); }
    .persona-desc { background: rgba(255,255,255,0.15); padding: 15px; border-radius: 15px; font-size: 14px; line-height: 1.6; margin-top: 15px; text-align: left; }
    
    .prod-card { border: 1px solid #E5E8EB; border-radius: 20px; padding: 25px; margin-bottom: 20px; background: white; box-shadow: 0 4px 20px rgba(0,0,0,0.03); position: relative; }
    .prod-rank { position: absolute; top: 0; left: 0; background: #3182F6; color: white; padding: 8px 15px; border-radius: 20px 0 20px 0; font-weight: 800; font-size: 14px; }
    .why-box { background: #FAFAFA; padding: 15px; border-radius: 12px; margin-top: 15px; border: 1px solid #F2F4F6; }
    .why-title { font-size: 14px; font-weight: bold; color: #333; margin-bottom: 5px; display: flex; align-items: center; gap: 5px; }
    .qr-container { text-align: center; margin-top: 40px; padding: 30px; background: white; border-radius: 20px; border: 1px solid #E5E8EB; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { height: 50px; white-space: pre-wrap; background-color: #fff; border-radius: 10px; color: #4e5968; font-weight: 600; border: 1px solid #E5E8EB; }
    .stTabs [aria-selected="true"] { background-color: #E8F3FF; color: #3182F6; border-color: #3182F6; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 로직 엔진 & 차트
# ==============================================================================
def get_index_recommendation(sph, cyl):
    power = abs(sph) + abs(cyl)
    if power < 2.0: return "1.56 (중굴절)", 0, 6
    elif power < 4.0: return "1.60 (고굴절)", 20000, 7
    elif power < 6.0: return "1.67 (초고굴절)", 50000, 8
    else: return "1.74 (특초고굴절)", 90000, 10

def load_data(mode, sph=0, cyl=0):
    if mode == 'glasses':
        idx_name, idx_price, thin_score = get_index_recommendation(sph, cyl)
        data = [
            {'brand': '케미', 'name': '퍼펙트 UV', 'base_price': 30000, 'cat': 'general', 'tier': 0, 'view_score': 6, 'coat_score': 5},
            {'brand': '케미', 'name': '양면비구면 D-Free', 'base_price': 80000, 'cat': 'distortions', 'tier': 1, 'view_score': 8, 'coat_score': 7},
            {'brand': '자이스', 'name': '클리어뷰', 'base_price': 100000, 'cat': 'general', 'tier': 2, 'view_score': 9, 'coat_score': 8},
            {'brand': '자이스', 'name': '드라이브세이프', 'base_price': 250000, 'cat': 'drive', 'tier': 2, 'view_score': 9, 'coat_score': 9},
            {'brand': '호야', 'name': '뉴럭스', 'base_price': 70000, 'cat': 'general', 'tier': 1, 'view_score': 8, 'coat_score': 8},
            {'brand': '니콘', 'name': 'BLUV Plus', 'base_price': 60000, 'cat': 'digital', 'tier': 1, 'view_score': 7, 'coat_score': 7},
            {'brand': '에실로', 'name': '트랜지션스 Gen8', 'base_price': 150000, 'cat': 'outdoor', 'tier': 2, 'view_score': 8, 'coat_score': 8},
            {'brand': '토카이', 'name': '루티나', 'base_price': 180000, 'cat': 'premium', 'tier': 2, 'view_score': 9, 'coat_score': 10}
        ]
        df = pd.DataFrame(data)
        df['final_price'] = df['base_price'] + idx_price
        df['index_info'] = idx_name
        df['thin_score'] = thin_score + (1 if sph < -4.0 else 0)
        return df
    else:
        data = {
            'brand': ['알콘', '알콘', '아큐브', '아큐브', '쿠퍼비전', '쿠퍼비전', '바슈롬', '미광'],
            'name': ['데일리스 토탈원', '토탈원 난시', '오아시스 원데이', '오아시스 난시', '클래리티', '클래리티 난시', '울트라 원데이', '클리어 원데이'],
            'category': ['sphere', 'toric', 'sphere', 'toric', 'sphere', 'toric', 'sphere', 'sphere'],
            'tier': [2, 2, 2, 2, 1, 1, 2, 0],
            'price': [69000, 79000, 63000, 74000, 45000, 49000, 55000, 32000],
            'dry': [10, 9.8, 8.5, 8.5, 7.5, 7.2, 8.7, 5.0],
            'handling': [4, 4, 8, 8, 7.5, 7.5, 8, 9],
            'dkt': [156, 127, 121, 121, 86, 57, 134, 25],
            'water': [33, 33, 38, 38, 56, 56, 55, 58]
        }
        return pd.DataFrame(data)

def make_bar_chart(scores, categories):
    fig = go.Figure(go.Bar(
        x=scores, y=categories, orientation='h',
        marker=dict(color='#3182F6',  line=dict(color='#1B64DA', width=1)),
        # [수정] 소수점 1자리까지만 텍스트로 표시
        text=[f'{s:.1f}' for s in scores], 
        textposition='auto',
        hovertemplate='%{y}: %{x:.1f}점<extra></extra>'
    ))
    fig.update_layout(
        xaxis=dict(range=[0, 10.5], showticklabels=False, visible=False),
        yaxis=dict(showgrid=False, tickfont=dict(size=12, color='#333', family="Pretendard")),
        margin=dict(l=0, r=0, t=0, b=0),
        height=180,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        dragmode=False
    )
    return fig

if 'page' not in st.session_state: st.session_state['page'] = 'home'
if 'answers' not in st.session_state: st.session_state['answers'] = {}
if 'vision' not in st.session_state: st.session_state['vision'] = {'sph': 0.0, 'cyl': 0.0, 'dont_know': False}

def go_to(page): st.session_state['page'] = page

# ==============================================================================
# 3. 메인 홈
# ==============================================================================
if st.session_state['page'] == 'home':
    st.markdown("<div class='header-title'>LENS MASTER</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-sub'>내 눈에 딱 맞는 인생 렌즈 찾기</div>", unsafe_allow_html=True)
    if st.button("🧬 나에게 맞는 렌즈는? (Eye-MBTI)", type="primary", use_container_width=True):
        go_to('mbti_test'); st.rerun()
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.button("⭐ 렌즈 평가 및 리뷰 (준비중)", disabled=True, use_container_width=True)
    st.button("👓 모든 렌즈 도감 (준비중)", disabled=True, use_container_width=True)

# ==============================================================================
# 4. 정밀 검사
# ==============================================================================
elif st.session_state['page'] == 'mbti_test':
    st.markdown("<div class='header-title'>정밀 시력 성향 검사</div>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown("<div style='background:#F9FAFB; padding:20px; border-radius:15px; margin-bottom:30px;'>", unsafe_allow_html=True)
        st.markdown("<b>🎛️ 도수 정보 (선택)</b>", unsafe_allow_html=True)
        dont_know = st.checkbox("🤔 정확한 도수를 몰라요 (검안 필요)", value=False)
        if not dont_know:
            c1, c2 = st.columns(2)
            sph = c1.number_input("SPH (근시)", -20.0, 10.0, -2.0, 0.25)
            cyl = c2.number_input("CYL (난시)", -10.0, 0.0, 0.0, 0.25)
            st.session_state['vision'] = {'sph': sph, 'cyl': cyl, 'dont_know': False}
        else:
            st.session_state['vision'] = {'sph': 0.0, 'cyl': 0.0, 'dont_know': True}
            st.info("✅ 안경원에서 정밀 검안 후 정확한 도수를 확인해 드립니다.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.progress(50)
    questions = {
        "E/I (환경)": [("Q1. 스마트폰/PC 사용이 8시간 이상인가요?", "env_1"), ("Q2. 건조한 실내 환경에 주로 계신가요?", "env_2"), ("Q3. 야외 활동을 자주 즐기시나요?", "env_3"), ("Q4. 미세먼지나 바람이 많은 환경인가요?", "env_4"), ("Q5. 야간 운전을 자주 하시나요?", "env_5")],
        "S/N (예민도)": [("Q6. 오후가 되면 눈이 뻑뻑하신가요?", "sen_1"), ("Q7. 렌즈 이물감을 잘 느끼시나요?", "sen_2"), ("Q8. 눈이 쉽게 붓거나 피로해지나요?", "sen_3"), ("Q9. 눈 시림/따가움을 자주 느끼나요?", "sen_4"), ("Q10. 난시(글자 번짐)가 심한가요?", "sen_5")],
        "T/F (가치관)": [("Q11. 눈을 위해 고가 제품 투자가 가능한가요?", "val_1"), ("Q12. 최신 기술/신제품을 선호하나요?", "val_2"), ("Q13. 브랜드 명성을 중요하게 생각하나요?", "val_3"), ("Q14. 1+1이나 할인이 제품 선택의 기준인가요?", "val_4"), ("Q15. 한 번 정착하면 잘 안 바꾸시나요?", "val_5")],
        "P/J (숙련도)": [("Q16. 렌즈 착용/관리에 능숙하신가요?", "exp_1"), ("Q17. 세척/관리가 귀찮지 않으신가요?", "exp_2"), ("Q18. 본인의 도수를 알고 계신가요?", "exp_3"), ("Q19. 렌즈 착용 실패 경험이 없으신가요?", "exp_4"), ("Q20. 전문가 도움 없이도 고를 수 있나요?", "exp_5")]
    }
    
    answers = {}
    for category, q_list in questions.items():
        st.markdown(f"<div class='header-title' style='font-size:20px; margin-top:30px;'>📂 {category}</div>", unsafe_allow_html=True)
        # [수정] 영어 풀스펠링 적용
        desc = ""
        if "E/I" in category: desc = "<div class='desc-title'>👀 시각적 환경 (Environment)</div><div class='desc-text'>• <span class='desc-highlight'>E (Exterior):</span> 야외 활동이 많고 거친 환경에 노출됨</div><div class='desc-text'>• <span class='desc-highlight'>I (Interior):</span> 실내 디지털 기기 사용이 많고 정적임</div>"
        elif "S/N" in category: desc = "<div class='desc-title'>👀 각막 민감도 (Sensitivity)</div><div class='desc-text'>• <span class='desc-highlight'>S (Sensitive):</span> 작은 자극에도 예민하고 건조감을 느낌</div><div class='desc-text'>• <span class='desc-highlight'>N (Natural):</span> 눈이 건강하고 웬만한 렌즈는 잘 맞음</div>"
        elif "T/F" in category: desc = "<div class='desc-title'>👀 소비 가치관 (Value)</div><div class='desc-text'>• <span class='desc-highlight'>T (Technology):</span> 가격보다는 최신 스펙과 고성능을 추구</div><div class='desc-text'>• <span class='desc-highlight'>F (Frugality):</span> 합리적인 가격과 가성비, 행사 상품을 선호</div>"
        elif "P/J" in category: desc = "<div class='desc-title'>👀 관리 숙련도 (Proficiency)</div><div class='desc-text'>• <span class='desc-highlight'>P (Professional):</span> 렌즈 관리에 능숙하고 지식이 해박함</div><div class='desc-text'>• <span class='desc-highlight'>J (Junior):</span> 아직은 관리가 서툴고 전문가 도움이 필요함</div>"
        st.markdown(f"<div class='desc-box'>{desc}</div>", unsafe_allow_html=True)
        
        for q_text, key in q_list:
            st.markdown(f"<div class='q-text'>{q_text}</div>", unsafe_allow_html=True)
            st.markdown("""<div class="scale-labels"><span>전혀 아니다(1)</span><span>그저 그렇다(3)</span><span>매우 그렇다(5)</span></div>""", unsafe_allow_html=True)
            answers[key] = st.radio(key, [1,2,3,4,5], horizontal=True, key=key, label_visibility="collapsed")
        st.markdown("---")
    if st.button("결과 분석하기", type="primary", use_container_width=True):
        st.session_state['answers'] = answers
        go_to('result'); st.rerun()

# ==============================================================================
# 5. 통합 결과 리포트
# ==============================================================================
elif st.session_state['page'] == 'result':
    with st.spinner('🧬 AI가 고객님의 시각 성향을 분석하여 최적의 제품을 매칭 중입니다...'): time.sleep(1.5)
    ans = st.session_state['answers']
    vision = st.session_state['vision']
    
    score_i = sum([ans[f'env_{i}'] for i in range(1,6)]); type_i = "I" if score_i >= 15 else "E"
    score_s = sum([ans[f'sen_{i}'] for i in range(1,6)]); type_s = "S" if score_s >= 15 else "N"
    score_t = sum([ans[f'val_{i}'] for i in range(1,6)]); type_t = "T" if score_t >= 15 else "F"
    score_p = sum([ans[f'exp_{i}'] for i in range(1,6)]); type_p = "P" if score_p >= 15 else "J"
    mbti_res = f"{type_i}{type_s}{type_t}{type_p}"
    
    user_titles = {
        "ISTP": {"title": "깐깐한 디지털 전문가", "desc": "작은 불편함도 용납하지 않는 프로페셔널! 최고 사양이 필요해요.", "strategy": "피로 감소 & 초정밀 교정"},
        "ENFP": {"title": "자유로운 가성비 러버", "desc": "활동적이고 자유로워요! 막 써도 좋은 실속형이 딱!", "strategy": "내구성 & 가격 경쟁력"},
        "ISFJ": {"title": "신중한 안전 제일주의자", "desc": "눈 건강을 최우선으로 생각하는 당신. 검증된 브랜드가 필수!", "strategy": "생체 친화 소재 & 브랜드 신뢰"},
        "ENTJ": {"title": "효율 중심의 리더", "desc": "성능과 가격의 완벽한 밸런스를 찾습니다.", "strategy": "High-End 급의 가심비 제품"}
    }
    persona = user_titles.get(mbti_res, {"title": "밸런스형 스마트 컨슈머", "desc": "상황에 맞춰 합리적인 선택을 하는 유연한 타입!", "strategy": "올라운드형 밸런스 제품"})

    st.markdown(f"""<div class="result-header"><div style="font-size:16px; opacity:0.8;">당신의 시각적 성향은?</div><div class="mbti-hero">{mbti_res}</div><div style="font-size: 24px; font-weight: bold; margin-bottom: 10px;">{persona['title']}</div><div class="persona-desc"><b>📝 분석 결과:</b> {persona['desc']}<br><b>💡 교정 전략:</b> {persona['strategy']}</div></div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👓 안경렌즈 솔루션", "💧 콘택트렌즈 솔루션"])

    with tab1:
        st.markdown("### 👓 안경렌즈 Best 3")
        df_g = load_data('glasses', vision['sph'], vision['cyl'])
        cand_g = df_g.copy()
        
        for i, r in cand_g.iterrows():
            # [수정] 가격 점수: 비쌀수록 낮음, 저렴할수록 높음 (Affordability)
            # 30만원 -> 2.5점, 3만원 -> 9.25점
            price_score = max(2, 10 - (r['final_price'] / 40000))
            
            # 랭킹용 적합도 가산점 (Rank Score)
            fit_score = 7
            if 'drive' in r['cat'] and ans['env_5'] >= 4: fit_score += 3
            if 'digital' in r['cat'] and type_i == 'I': fit_score += 3
            if 'distortions' in r['cat'] and abs(vision['cyl']) >= 1.0: fit_score += 3
            if r['tier'] == 2 and type_t == "T": fit_score += 4 # T타입이면 프리미엄 가산점 대폭 강화
            
            # 실제 표출용 점수 저장
            cand_g.at[i, 'price_score'] = price_score
            cand_g.at[i, 'fit_score'] = min(10, fit_score)
            
            # 최종 랭킹 산정식 (화면에 보이는 점수와 별개로 순위 결정)
            if type_t == "T": 
                # T형은 가격 점수가 낮아도(비싸도), Tier(등급)와 시야 점수가 높으면 1등
                cand_g.at[i, 'rank_score'] = (r['tier'] * 25) + (fit_score * 3) + r['view_score']
            else: 
                # F형은 가격 점수(저렴함)가 깡패
                cand_g.at[i, 'rank_score'] = (price_score * 4) + (fit_score * 2)

        ranks = cand_g.sort_values('rank_score', ascending=False).head(3)
        for rk, (idx, row) in enumerate(ranks.iterrows(), 1):
            reasons = []
            if type_t == "T" and row['tier'] == 2: reasons.append("고객님의 <b>'최고 사양 선호(T)'</b> 성향에 맞춰, 광학 성능이 가장 우수한 <b>하이엔드 렌즈</b>를 1순위로 추천합니다.")
            elif type_t == "F" and row['tier'] == 0: reasons.append("고객님의 <b>'가성비 중시(F)'</b> 성향에 맞춰, 거품을 뺀 <b>실속형 렌즈</b>입니다.")
            if 'drive' in row['cat'] and ans['env_5'] >= 3: reasons.append("야간 운전 시 <b>빛 번짐 차단 코팅</b>이 눈의 피로를 획기적으로 줄여줍니다.")
            if abs(vision['cyl']) >= 1.0 and row['cat'] == 'distortions': reasons.append(f"난시(-{abs(vision['cyl'])}D)로 인한 <b>주변부 울렁임을 잡는 설계</b>가 필수입니다.")
            if not reasons: reasons.append("고객님의 라이프스타일 데이터와 도수 정보를 종합했을 때 가장 밸런스가 좋은 제품입니다.")
            
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.markdown(f"""<div class="prod-card"><div class="prod-rank">{rk}위</div><div style="font-size:18px; font-weight:800; margin-top:10px;">{row['name']}</div><div style="font-size:13px; color:#666; margin-bottom:8px;">{row['brand']} | 굴절률 {row['index_info']}</div><div style="font-size:16px; font-weight:bold; color:#3182F6;">{format(int(row['final_price']),',')}원~</div><div class="why-box"><div class="why-title">🧐 추천 사유 (Why?)</div><ul style="margin:0; padding-left:15px; font-size:13px; color:#555;">{"".join([f"<li>{r}</li>" for r in reasons])}</ul></div></div>""", unsafe_allow_html=True)
            with c2: 
                st.plotly_chart(make_bar_chart([row['thin_score'], row['view_score'], row['coat_score'], row['price_score'], row['fit_score']], ['두께', '시야', '코팅', '가격경쟁력', '적합도']), use_container_width=True)
            st.divider()

    with tab2:
        st.markdown("### 💧 콘택트렌즈 Best 3")
        df_c = load_data('contacts')
        is_toric = True if abs(vision['cyl']) >= 0.75 and not vision['dont_know'] else False
        cand_c = df_c[df_c['category'].str.contains('toric' if is_toric else 'sphere')].copy()
        
        for i, r in cand_c.iterrows():
            # [수정] 렌즈 가격 점수도 동일하게 적용 (저렴=10, 비쌈=2)
            price_score = max(2, 10 - (r['price'] / 10000))
            cand_c.at[i, 'price_score'] = price_score
            
            if type_t == "T": cand_c.at[i, 'rank_score'] = (r['tier'] * 20) + (r['dkt'] / 10) + r['dry']
            else: cand_c.at[i, 'rank_score'] = (price_score * 5) + r['dry']

        ranks_c = cand_c.sort_values('rank_score', ascending=False).head(3)
        for rk, (idx, row) in enumerate(ranks_c.iterrows(), 1):
            reasons = []
            if type_t == "T" and row['tier'] == 2: reasons.append("최고 사양을 원하시는 고객님을 위해, <b>산소투과율이 압도적인 프리미엄 렌즈</b>입니다.")
            elif type_t == "F": reasons.append("가성비를 1순위로 꼽으셔서, 성능 대비 <b>가격 경쟁력이 가장 뛰어난 제품</b>입니다.")
            if ans['sen_1'] >= 4: reasons.append(f"오후 건조감 방어 점수({row['dry']}점)가 높아 장시간 착용에도 편안합니다.")
            
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.markdown(f"""<div class="prod-card"><div class="prod-rank">{rk}위</div><div style="font-size:18px; font-weight:800; margin-top:10px;">{row['name']}</div><div style="font-size:13px; color:#666; margin-bottom:8px;">{row['brand']}</div><div style="font-size:16px; font-weight:bold; color:#3182F6;">{format(row['price'],',')}원</div><div class="why-box"><div class="why-title">🧐 추천 사유 (Why?)</div><ul style="margin:0; padding-left:15px; font-size:13px; color:#555;">{"".join([f"<li>{r}</li>" for r in reasons])}</ul></div></div>""", unsafe_allow_html=True)
            with c2: 
                # [수정] '가격' -> '가격경쟁력'으로 라벨 변경 (오해 방지)
                st.plotly_chart(make_bar_chart([row['dry'], row['handling'], min(row['dkt']/16, 10), row['price_score'], 9.5], ['건조감', '핸들링', '산소', '가격경쟁력', '적합도']), use_container_width=True)
            st.divider()

    st.markdown("### 📲 안경사 전용 처방전 (QR)")
    qr_data = f"Type:{mbti_res}\nSPH:{vision['sph']}/CYL:{vision['cyl']}\nRec:{ranks.iloc[0]['name'] if 'ranks' in locals() else 'None'}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2); qr.add_data(qr_data); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white"); buffered = BytesIO(); img.save(buffered, format="PNG"); img_str = base64.b64encode(buffered.getvalue()).decode()
    st.markdown(f"""<div class="qr-container"><div style="font-weight:bold; margin-bottom:10px;">안경사님께 이 화면을 보여주세요</div><img src="data:image/png;base64,{img_str}" width="150"><div style="font-size:12px; color:#999; margin-top:10px;">스캔 시 고객님의 도수 및 추천 렌즈 정보가 표시됩니다.</div></div>""", unsafe_allow_html=True)
    if st.button("처음으로 돌아가기", use_container_width=True): go_to('home'); st.rerun()
