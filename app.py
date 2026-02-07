import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import plotly.graph_objects as go
import qrcode
from io import BytesIO
import base64

# ==============================================================================
# 0. 기본 설정 & URL
# ==============================================================================
st.set_page_config(page_title="Lens Master Pro", page_icon="👁️", layout="centered")
BASE_URL = "https://lens-master-fhsfp5b458nqhycwenbvga.streamlit.app/"

# ==============================================================================
# 1. 디자인 (CSS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F0F2F6; }
    
    h1, .header-title { color: #1E3A8A !important; font-weight: 800 !important; letter-spacing: -1px; word-break: keep-all; }
    
    div.stButton > button:first-child { background-color: #2563EB !important; color: white !important; border-color: #2563EB !important; font-weight: bold; }
    div.stButton > button:hover { background-color: #1D4ED8 !important; border-color: #1D4ED8 !important; }
    div.stButton > button:focus { box-shadow: none !important; outline: none !important; }

    .stSpinner > div { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 9999; }
    
    .desc-box { background-color: #fff; padding: 22px; border-radius: 16px; border: 1px solid #E5E8EB; margin-bottom: 25px; box-shadow: 0 4px 20px rgba(0,0,0,0.04); }
    .desc-title { font-size: 16px; font-weight: 700; color: #333; margin-bottom: 12px; border-bottom: 2px solid #F2F4F6; padding-bottom: 8px; }
    .desc-text { font-size: 14px; color: #555; line-height: 1.7; margin-bottom: 6px; }
    .desc-highlight { color: #2563EB; font-weight: 700; background-color: #EFF6FF; padding: 2px 8px; border-radius: 6px; }

    .q-text { font-size: 17px; font-weight: 700; color: #111; margin-top: 35px; margin-bottom: 12px; word-break: keep-all; }
    .scale-labels { display: flex; justify-content: space-between; font-size: 12px; color: #888; font-weight: 500; padding: 0 10px; margin-bottom: 8px; }
    div[role="radiogroup"] { gap: 0; justify-content: space-between; margin-bottom: 20px; }
    div[role="radiogroup"] label { background-color: white !important; border: 1px solid #E5E8EB !important; border-radius: 50% !important; width: 48px; height: 48px; display: flex; justify-content: center; align-items: center; cursor: pointer; transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
    div[role="radiogroup"] label:hover { background-color: #F8FAFC !important; transform: translateY(-3px); }
    div[role="radiogroup"] label:has(input:checked) { background-color: #2563EB !important; border-color: #2563EB !important; box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3); transform: scale(1.1); }
    div[role="radiogroup"] label p { font-size: 16px !important; margin: 0 !important; color: #888 !important; }
    div[role="radiogroup"] label:has(input:checked) p { color: white !important; font-weight: bold !important; }
    div[role="radiogroup"] label > div:first-child { display: none; }

    .result-header { background: #1E3A8A; color: white; padding: 45px 25px; border-radius: 0 0 30px 30px; margin: -25px -25px 25px -25px; text-align: center; box-shadow: 0 10px 30px rgba(30, 58, 138, 0.3); }
    .mbti-hero { font-size: 60px; font-weight: 900; margin: 15px 0; text-shadow: 0 4px 15px rgba(0,0,0,0.2); letter-spacing: 2px; }
    .persona-desc { background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px; font-size: 15px; line-height: 1.6; margin-top: 20px; text-align: left; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }
    
    .prod-card { border: 1px solid #E5E8EB; border-radius: 20px; padding: 25px; margin-bottom: 25px; background: white; box-shadow: 0 8px 25px rgba(0,0,0,0.05); position: relative; overflow: hidden; }
    .prod-rank { position: absolute; top: 0; left: 0; background: #2563EB; color: white; padding: 8px 18px; border-radius: 0 0 20px 0; font-weight: 800; font-size: 15px; z-index: 10; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .match-badge { display: inline-block; background: #E0F2FE; color: #0284C7; font-size: 12px; font-weight: 800; padding: 4px 8px; border-radius: 6px; margin-left: 8px; vertical-align: middle; }
    .tag-box { margin-top: 8px; margin-bottom: 15px; }
    .feature-tag { display: inline-block; background: #F3F4F6; color: #4B5563; font-size: 11px; padding: 4px 8px; border-radius: 6px; margin-right: 5px; margin-bottom: 5px; font-weight: 600; }
    
    .why-box { background: #F8FAFC; padding: 20px; border-radius: 12px; margin-top: 20px; border-left: 4px solid #2563EB; word-break: keep-all; }
    .why-cat { font-size: 13px; font-weight: 800; color: #1E3A8A; margin-bottom: 4px; display: block; margin-top: 10px; }
    .why-cat:first-child { margin-top: 0; }
    .why-desc { font-size: 13px; color: #555; line-height: 1.5; margin-bottom: 8px; }

    .qr-container { text-align: center; margin-top: 50px; padding: 30px; background: white; border-radius: 24px; border: 1px solid #E5E8EB; box-shadow: 0 10px 40px rgba(0,0,0,0.05); }
    .capture-guide { color: #E11D48; font-weight: 800; margin-top: 10px; font-size: 14px; }
    .metric-box { margin-bottom: 15px; }
    .metric-header { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 5px; color: #333; font-weight: 600; }
    .metric-meaning { font-size: 11px; color: #666; text-align: right; margin-top: 2px; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { height: 55px; background-color: #fff; border-radius: 12px; color: #64748B; font-weight: 600; border: 1px solid #E2E8F0; flex: 1; transition: all 0.2s; }
    .stTabs [aria-selected="true"] { background-color: #EFF6FF; color: #2563EB; border-color: #2563EB; box-shadow: 0 4px 12px rgba(37, 99, 235, 0.15); }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 데이터 엔진 (알고리즘 수정됨)
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
            {'brand': '케미', 'name': '퍼펙트 UV', 'base_price': 30000, 'cat': 'general', 'tier': 0, 'view': 6, 'coat': 5, 'tags': ['#블루라이트차단', '#가성비', '#국민렌즈']},
            {'brand': '니콘', 'name': 'BLUV Plus', 'base_price': 60000, 'cat': 'digital', 'tier': 1, 'view': 7, 'coat': 7, 'tags': ['#양면자외선차단', '#디지털피로완화']},
            {'brand': '호야', 'name': '뉴럭스', 'base_price': 70000, 'cat': 'general', 'tier': 1, 'view': 8, 'coat': 9, 'tags': ['#고강도코팅', '#스크래치방지', '#선명함']},
            {'brand': '케미', 'name': '양면비구면 D-Free', 'base_price': 80000, 'cat': 'distortions', 'tier': 1, 'view': 8, 'coat': 7, 'tags': ['#왜곡최소화', '#눈이덜작아보임', '#난시추천']},
            {'brand': '자이스', 'name': '클리어뷰', 'base_price': 100000, 'cat': 'general', 'tier': 2, 'view': 9, 'coat': 8, 'tags': ['#더넓은시야', '#더얇은두께', '#프리미엄']},
            {'brand': '에실로', 'name': '트랜지션스 Gen8', 'base_price': 150000, 'cat': 'outdoor', 'tier': 2, 'view': 8, 'coat': 8, 'tags': ['#변색렌즈', '#선글라스겸용', '#빠른변색']},
            {'brand': '토카이', 'name': '루티나', 'base_price': 180000, 'cat': 'premium', 'tier': 3, 'view': 9, 'coat': 10, 'tags': ['#루테인보호', '#망막케어', '#최상급코팅']},
            {'brand': '자이스', 'name': '드라이브세이프', 'base_price': 250000, 'cat': 'drive', 'tier': 3, 'view': 10, 'coat': 9, 'tags': ['#야간운전', '#빛번짐차단', '#우천시선명']}
        ]
        df = pd.DataFrame(data)
        df['final_price'] = df['base_price'] + idx_price
        df['index_info'] = idx_name
        df['thin_score'] = [min(10, thin_score + (1 if sph < -4.0 else 0)) for _ in range(len(df))]
        return df
    else:
        data = {
            'brand': ['미광', '쿠퍼비전', '인터로조', '바슈롬', '아큐브', '알콘', '알콘', '아큐브'],
            'name': ['클리어 원데이', '클래리티', '오투오투', '울트라 원데이', '오아시스 원데이', '데일리스 토탈원', '토탈원 난시', '오아시스 난시'],
            'category': ['sphere', 'sphere', 'sphere', 'sphere', 'sphere', 'sphere', 'toric', 'toric'],
            'tier': [0, 1, 1, 2, 2, 3, 3, 2],
            'price': [32000, 45000, 45000, 55000, 63000, 69000, 79000, 74000],
            'water': [58, 56, 45, 55, 38, 33, 33, 38],
            'dkt': [25, 86, 130, 134, 121, 156, 127, 121],
            'dry_score': [4, 7, 7, 8, 8, 10, 10, 8],
            'handling': [9, 7, 8, 8, 8, 4, 4, 8],
            'tags': [['#가성비갑', '#막쓰기좋음'], ['#실리콘하이드로겔', '#입문용'], ['#국산프리미엄', '#산소전달굿'], ['#16시간지속', '#디지털기기'], ['#베스트셀러', '#PC업무'], ['#워터렌즈', '#건조감종결', '#이물감제로'], ['#난시워터렌즈', '#프리미엄'], ['#난시교정탁월', '#안정감']]
        }
        return pd.DataFrame(data)

def make_radar_chart(product_name, scores, categories):
    scores_closed = scores + [scores[0]]
    categories_closed = categories + [categories[0]]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores_closed, theta=categories_closed, fill='toself', name=product_name,
        line=dict(color='#2563EB', width=2), fillcolor='rgba(37, 99, 235, 0.15)'
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 10], showticklabels=False, gridcolor='#E2E8F0', gridwidth=1)),
        showlegend=False, margin=dict(t=30, b=30, l=40, r=40), height=240,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12, color='#475569', family="Pretendard", weight="bold")
    )
    return fig

all_q_keys = [
    'env_1', 'env_2', 'env_3', 'env_4', 'env_5',
    'sen_1', 'sen_2', 'sen_3', 'sen_4', 'sen_5',
    'val_1', 'val_2', 'val_3', 'val_4', 'val_5',
    'exp_1', 'exp_2', 'exp_3', 'exp_4', 'exp_5'
]
q_labels = {
    'env_1': 'Q1.하루 8시간 이상 디지털 기기 사용', 
    'env_2': 'Q2.건조한 실내 환경(히터/에어컨) 상주', 
    'env_3': 'Q3.야외 활동 및 자외선 노출 빈도 높음', 
    'env_4': 'Q4.미세먼지/바람 등 거친 환경 노출', 
    'env_5': 'Q5.야간 운전 빈도 높음',
    'sen_1': 'Q6.오후 시간대 눈 뻑뻑함/충혈 발생', 
    'sen_2': 'Q7.렌즈 착용 시 이물감 예민하게 느낌', 
    'sen_3': 'Q8.눈이 쉽게 붓거나 피로감 느낌', 
    'sen_4': 'Q9.눈 시림 및 따가움 자주 느낌', 
    'sen_5': 'Q10.난시로 인한 글자 번짐/흐림 심함',
    'val_1': 'Q11.눈을 위한 고가 제품 투자 의향 있음', 
    'val_2': 'Q12.최신 기술 및 신제품 선호 성향', 
    'val_3': 'Q13.브랜드 인지도 및 명성 중요시', 
    'val_4': 'Q14.할인 행사 및 가성비 중요시', 
    'val_5': 'Q15.기존 사용 제품 고수 성향 (보수적)',
    'exp_1': 'Q16.렌즈 착용 및 제거 능숙도 높음', 
    'exp_2': 'Q17.렌즈 세척 및 관리 귀찮지 않음', 
    'exp_3': 'Q18.본인의 정확한 도수 인지하고 있음', 
    'exp_4': 'Q19.과거 렌즈 착용 성공 경험 있음', 
    'exp_5': 'Q20.전문가 도움 없이 스스로 제품 선택 가능'
}

# ==============================================================================
# 3. 상태 관리
# ==============================================================================
query_params = st.query_params
if 'mode' in query_params and query_params['mode'] == 'result':
    st.session_state['page'] = 'optician_view'
    try:
        st.session_state['restored_data'] = {
            'mbti': query_params.get('mbti', 'ISTP'),
            'sph': float(query_params.get('sph', 0.0)),
            'cyl': float(query_params.get('cyl', 0.0)),
            'env': float(query_params.get('env', 5.0)),
            'sen': float(query_params.get('sen', 5.0)),
            'val': float(query_params.get('val', 5.0)),
            'pro': float(query_params.get('pro', 5.0)),
            'answers_str': query_params.get('answers', '3'*20),
            'dk': query_params.get('dk', '0')
        }
    except:
        st.session_state['page'] = 'home'

if 'page' not in st.session_state: st.session_state['page'] = 'home'
if 'answers' not in st.session_state: st.session_state['answers'] = {}
if 'vision' not in st.session_state: st.session_state['vision'] = {'sph': 0.0, 'cyl': 0.0, 'dont_know': False}

def go_to(page): st.session_state['page'] = page

# ==============================================================================
# 4. 안경사 전용 뷰
# ==============================================================================
if st.session_state['page'] == 'optician_view':
    data = st.session_state['restored_data']
    st.markdown(f"<div class='header-title' style='font-size:24px; color:#1E3A8A;'>👓 안경사 전용 리포트</div>", unsafe_allow_html=True)
    
    if data.get('dk') == '1':
        st.error("**기존 처방 도수:** 상담 필요 (도수 정보 없음)")
    else:
        st.info(f"**기존 처방 도수:** SPH {data['sph']} / CYL {data['cyl']}")
    
    st.markdown("<div style='font-weight:bold; margin-top:20px; margin-bottom:15px; color:#333;'>🏆 AI 추천 제품 (Top 3)</div>", unsafe_allow_html=True)
    
    type_t = "T" if data['val'] >= 6 else "F"
    
    # [수정] 랭킹 로직 동일 적용 (안경사 뷰)
    tab1, tab2 = st.tabs(["👓 안경렌즈", "💧 콘택트렌즈"])
    with tab1:
        df_g = load_data('glasses', data['sph'], data['cyl'])
        cand_g = df_g.copy()
        for i, r in cand_g.iterrows():
            norm_spec = r['tier'] * 2.5 # 0~3 -> 0~7.5점
            price_score = max(2, 10 - (r['final_price'] / 45000))
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            cand_g.at[i, 'total_score'] = total_score
        
        ranks = cand_g.sort_values('total_score', ascending=False).head(3)
        for rk, (idx, row) in enumerate(ranks.iterrows(), 1):
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;">
                <div style="font-weight:bold; font-size:16px;">{rk}위. {row['name']}</div>
                <div style="color:#666; font-size:13px;">{row['brand']} | {format(int(row['final_price']),',')}원</div>
            </div>""", unsafe_allow_html=True)

    with tab2:
        df_c = load_data('contacts')
        is_toric = True if abs(data['cyl']) >= 0.75 else False
        cand_c = df_c[df_c['category'].str.contains('toric' if is_toric else 'sphere')].copy()
        for i, r in cand_c.iterrows():
            norm_spec = r['dry_score'] # 0~10
            price_score = max(2, 10 - (r['price'] / 10000))
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            cand_c.at[i, 'total_score'] = total_score
        
        ranks_c = cand_c.sort_values('total_score', ascending=False).head(3)
        for rk, (idx, row) in enumerate(ranks_c.iterrows(), 1):
            st.markdown(f"""
            <div style="background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;">
                <div style="font-weight:bold; font-size:16px;">{rk}위. {row['name']}</div>
                <div style="color:#666; font-size:13px;">{row['brand']} | {format(row['price'],',')}원</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-weight:bold; margin-bottom:10px; color:#2563EB;'>📊 4대 핵심 지표 분석</div>", unsafe_allow_html=True)
    
    def get_status(val, type):
        if type == "env": return "디지털 과몰입 (주의)" if val >= 7 else "보통 수준"
        if type == "sen": return "초예민 (건조감 호소)" if val >= 7 else "건강한 편"
        if type == "val": return "고스펙 중시 (T형)" if val >= 6 else "가성비 중시 (F형)"
        if type == "pro": return "숙련자 (관리 능숙)" if val >= 7 else "입문자 (관리 미숙)"
        return ""

    metrics = [
        ("디지털/실내 환경", data['env'], "env"),
        ("각막 민감도", data['sen'], "sen"),
        ("가격/스펙 성향", data['val'], "val"),
        ("렌즈 관리 숙련도", data['pro'], "pro")
    ]
    for label, val, type in metrics:
        status = get_status(val, type)
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-header"><span>{label}</span><span style="color:#2563EB;">{val}점</span></div>
            <div style="background:#F1F5F9; height:8px; border-radius:4px; overflow:hidden;"><div style="background:#2563EB; height:100%; width:{val*10}%;"></div></div>
            <div class="metric-meaning">{status}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-weight:bold; margin-bottom:15px; color:#333;'>📝 20문항 상세 답변</div>", unsafe_allow_html=True)
    ans_str = data['answers_str']
    if len(ans_str) == 20:
        with st.container():
            for i, key in enumerate(all_q_keys):
                score = ans_str[i]
                st.markdown(f"<div style='font-size:13px; border-bottom:1px solid #f0f0f0; padding:8px 0; display:flex; justify-content:space-between;'><span style='color:#555; flex:1; word-break:keep-all; padding-right:10px;'>{q_labels[key]}</span> <span style='font-weight:bold; color:#2563EB;'>{score}점</span></div>", unsafe_allow_html=True)

    st.success(f"**고객 성향:** {data['mbti']}")

    if st.button("메인으로 돌아가기", use_container_width=True):
        st.query_params.clear()
        go_to('home'); st.rerun()

# ==============================================================================
# 5. 일반 사용자 흐름
# ==============================================================================
elif st.session_state['page'] == 'home':
    st.markdown("<div class='header-title'>LENS MASTER</div>", unsafe_allow_html=True)
    st.markdown("<div class='header-sub'>당신의 눈에 딱 맞는 인생 렌즈 찾기</div>", unsafe_allow_html=True)
    if st.button("🧬 나에게 맞는 렌즈는? (Eye-MBTI)", type="primary", use_container_width=True):
        go_to('mbti_test'); st.rerun()
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.button("⭐ 렌즈 평가 및 리뷰 (준비중)", disabled=True, use_container_width=True)
    st.button("👓 모든 렌즈 도감 (준비중)", disabled=True, use_container_width=True)

elif st.session_state['page'] == 'mbti_test':
    st.markdown("<div class='header-title'>정밀 시력 성향 검사</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='background:#F8FAFC; padding:20px; border-radius:15px; margin-bottom:30px; border:1px solid #E2E8F0;'>", unsafe_allow_html=True)
        st.markdown("<b>🎛️ 기존 처방 도수 (선택)</b>", unsafe_allow_html=True)
        dont_know = st.checkbox("🤔 정확한 도수를 몰라요 (상담 필요)", value=False)
        if not dont_know:
            c1, c2 = st.columns(2)
            sph = c1.number_input("SPH (근시)", -20.0, 10.0, -2.5, 0.25)
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
        st.markdown(f"<div class='header-title' style='font-size:22px; margin-top:40px; color:#1E3A8A;'>📂 {category}</div>", unsafe_allow_html=True)
        desc = ""
        if "E/I" in category: desc = "<div class='desc-title'>👀 시각적 환경 (Environment)</div><div class='desc-text'>• <span class='desc-highlight'>E (Exterior):</span> 다이내믹한 야외 활동, 미세먼지/자외선 노출</div><div class='desc-text'>• <span class='desc-highlight'>I (Interior):</span> 정적인 실내 생활, 디지털 기기 과몰입</div>"
        elif "S/N" in category: desc = "<div class='desc-title'>👀 각막 민감도 (Sensitivity)</div><div class='desc-text'>• <span class='desc-highlight'>S (Sensitive):</span> 작은 먼지에도 눈물 나는 예민보스</div><div class='desc-text'>• <span class='desc-highlight'>N (Natural):</span> 강철 각막, 아무거나 껴도 OK</div>"
        elif "T/F" in category: desc = "<div class='desc-title'>👀 소비 가치관 (Value)</div><div class='desc-text'>• <span class='desc-highlight'>T (Technology):</span> 성능/스펙이 1순위, 비싼 건 이유가 있다</div><div class='desc-text'>• <span class='desc-highlight'>F (Frugality):</span> 가성비 1순위, 1+1 행사는 못 참지</div>"
        elif "P/J" in category: desc = "<div class='desc-title'>👀 관리 숙련도 (Proficiency)</div><div class='desc-text'>• <span class='desc-highlight'>P (Professional):</span> 렌즈 착용 10년 차 고인물, 관리의 신</div><div class='desc-text'>• <span class='desc-highlight'>J (Junior):</span> 렌즈 입문자, 끼고 빼는 게 무서움</div>"
        st.markdown(f"<div class='desc-box'>{desc}</div>", unsafe_allow_html=True)
        
        for q_text, key in q_list:
            st.markdown(f"<div class='q-text'>{q_text}</div>", unsafe_allow_html=True)
            st.markdown("""<div class="scale-labels"><span>전혀 아니다(1)</span><span>보통이다(3)</span><span>매우 그렇다(5)</span></div>""", unsafe_allow_html=True)
            answers[key] = st.radio(key, [1,2,3,4,5], horizontal=True, key=key, index=None, label_visibility="collapsed")
        st.markdown("---")
    
    if st.button("✨ 결과 분석하기", type="primary", use_container_width=True):
        if None in answers.values():
            st.error("⚠️ 정확한 분석을 위해 모든 문항을 선택해주세요!")
        else:
            st.session_state['answers'] = answers
            go_to('result'); st.rerun()

elif st.session_state['page'] == 'result':
    # [강력한 스크롤 강제 이동: 앵커 트릭]
    st.markdown("<div id='top_anchor'></div>", unsafe_allow_html=True)
    components.html("""
        <script>
            function scrollToAnchor() {
                var anchor = window.parent.document.getElementById("top_anchor");
                if (anchor) {
                    anchor.scrollIntoView(true);
                } else {
                    window.parent.document.querySelector('section.main').scrollTo(0, 0);
                }
            }
            scrollToAnchor();
            setTimeout(scrollToAnchor, 100);
            setTimeout(scrollToAnchor, 500);
        </script>
    """, height=0)
    
    with st.spinner(''):
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i in range(100):
            if i < 30: status_text.markdown(f"<div style='text-align:center; font-weight:bold; color:#1E3A8A; margin-bottom:10px;'>🔎 고객 라이프스타일 정밀 분석 중... ({i}%)</div>", unsafe_allow_html=True)
            elif i < 60: status_text.markdown(f"<div style='text-align:center; font-weight:bold; color:#1E3A8A; margin-bottom:10px;'>👁️ 시력 데이터 및 굴절률 계산 중... ({i}%)</div>", unsafe_allow_html=True)
            else: status_text.markdown(f"<div style='text-align:center; font-weight:bold; color:#1E3A8A; margin-bottom:10px;'>✨ 최적의 렌즈 매칭 중... ({i}%)</div>", unsafe_allow_html=True)
            progress_bar.progress(i + 1)
            time.sleep(0.015)
        progress_bar.empty()
        status_text.empty()
    
    components.html("""
        <script>
            window.parent.document.querySelector('section.main').scrollTo(0, 0);
        </script>
    """, height=0)
    
    ans = st.session_state['answers']
    vision = st.session_state['vision']
    
    score_i = sum([ans[f'env_{i}'] for i in range(1,6)]); type_i = "I" if score_i >= 15 else "E"
    score_s = sum([ans[f'sen_{i}'] for i in range(1,6)]); type_s = "S" if score_s >= 15 else "N"
    score_t = sum([ans[f'val_{i}'] for i in range(1,6)]); type_t = "T" if score_t >= 15 else "F"
    score_p = sum([ans[f'exp_{i}'] for i in range(1,6)]); type_p = "P" if score_p >= 15 else "J"
    mbti_res = f"{type_i}{type_s}{type_t}{type_p}"
    
    stat_env = round(score_i / 2.5, 1)
    stat_sen = round(score_s / 2.5, 1)
    stat_val = round(score_t / 2.5, 1) if type_t == 'T' else round(score_t / 2.5, 1)
    stat_pro = round(score_p / 2.5, 1)

    personas = {
        "ISTP": {"title": "🔎 팩트체크 장인 (ISTP)", "desc": "화려한 마케팅 문구보다 <b>숫자와 스펙</b>을 믿는 당신! <br>작은 불편함도 용납 못 하는 예민한 눈의 소유자입니다.", "strategy": "묻지도 따지지도 말고 <b>현존 최고 스펙</b>으로 가야 후회가 없습니다."},
        "ENFP": {"title": "🦄 자유로운 영혼 (ENFP)", "desc": "복잡한 관리는 딱 질색! <br>활동적이고 에너지가 넘치는 당신에겐 <b>편하고 막 쓸 수 있는 렌즈</b>가 필요합니다.", "strategy": "끼고 빼기 쉽고, <b>내구성 좋은 원데이</b> 제품이 딱입니다."},
        "ISFJ": {"title": "🛡️ 눈 건강 지킴이 (ISFJ)", "desc": "돌다리도 두드려보고 건너는 신중파! <br>새로운 도전보다는 <b>검증된 브랜드와 안전한 소재</b>를 선호합니다.", "strategy": "안과의사들이 추천하는 <b>글로벌 베스트셀러</b>가 정답입니다."},
        "ENTJ": {"title": "😎 효율 끝판왕 (ENTJ)", "desc": "가격 대비 성능비(ROI)가 확실해야 지갑을 여는 당신! <br><b>성능과 가격의 황금 밸런스</b>를 중요하게 생각합니다.", "strategy": "프리미엄급 성능이지만 <b>가격 거품은 빠진 실속형</b> 제품."},
        "ESTP": {"title": "⚡ 행동대장 (ESTP)", "desc": "야외 활동을 즐기는 인싸! 자외선 차단이 필수입니다.", "strategy": "내구성 좋고 UV 차단되는 제품"},
        "INFJ": {"title": "🔮 섬세한 예언자 (INFJ)", "desc": "남들은 모르는 미세한 불편함까지 느끼는 섬세한 눈.", "strategy": "자극이 가장 적은 저자극 소재"},
        "INTP": {"title": "🧪 논리적인 분석가 (INTP)", "desc": "원리를 이해해야 직성이 풀립니다. 기술력이 중요해요.", "strategy": "최신 광학 기술이 적용된 렌즈"},
        "ESFJ": {"title": "🤝 평화주의자 (ESFJ)", "desc": "주변 평판과 추천을 중요하게 생각합니다.", "strategy": "재구매율 1위 베스트셀러"},
    }
    persona = personas.get(mbti_res, {"title": "⚖️ 밸런스형 스마트 컨슈머", "desc": "상황에 맞춰 합리적인 선택을 하는 유연한 타입입니다.", "strategy": "모든 면에서 평균 이상인 올라운드 제품"})

    st.markdown(f"""
    <div class="result-header">
        <div style="font-size:16px; opacity:0.9; margin-bottom:5px;">당신의 시각 성향 분석 결과</div>
        <div class="mbti-hero">{mbti_res}</div>
        <div style="font-size: 26px; font-weight: 800; margin-bottom: 15px;">{persona['title']}</div>
        <div class="persona-desc">
            <div style="margin-bottom:8px;"><b>🧐 분석:</b> {persona['desc']}</div>
            <div><b>💡 공략법:</b> {persona['strategy']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👓 안경렌즈 추천", "💧 콘택트렌즈 추천"])
    with tab1:
        st.markdown("### 👓 안경렌즈 솔루션 Best 3")
        df_g = load_data('glasses', vision['sph'], vision['cyl'])
        cand_g = df_g.copy()
        for i, r in cand_g.iterrows():
            # [수정] 랭킹 로직 개편: 가성비(F) 선택 시 가격 가중치 대폭 강화 (0.8)
            # 성능(0~100)을 10점 만점으로 환산(Normalize)하여 가격 점수와 동등하게 비교
            norm_spec = (r['tier'] * 2.5) # 0~3 tier -> 0~7.5점
            if 'digital' in r['cat'] and ans['env_1'] >= 4: norm_spec += 1.5
            if 'drive' in r['cat'] and ans['env_5'] >= 4: norm_spec += 1.5
            
            price_score = max(1, 10 - (r['final_price'] / 45000))
            
            if type_t == "T": 
                total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: 
                # F타입은 가격이 깡패 (80% 비중)
                total_score = (norm_spec * 0.2) + (price_score * 0.8)
                
            cand_g.at[i, 'total_score'] = total_score
            cand_g.at[i, 'visual_price_score'] = price_score

        ranks = cand_g.sort_values('total_score', ascending=False).head(3)
        top_score = ranks.iloc[0]['total_score']
        
        for rk, (idx, row) in enumerate(ranks.iterrows(), 1):
            match_percent = int((row['total_score'] / top_score) * 98)
            reasons = []
            
            life_reasons = []
            if ans['env_1'] == 5: life_reasons.append("하루 8시간 이상 모니터를 보는 극한의 디지털 환경")
            elif ans['env_1'] == 4: life_reasons.append("디지털 기기 사용량이 많은 환경")
            if ans['env_5'] >= 4: life_reasons.append("잦은 야간 운전")
            if ans['env_3'] >= 4: life_reasons.append("활발한 야외 활동")
            
            spec_reasons = []
            if 'digital' in row['cat']: spec_reasons.append("조절력 피로를 완화하는 <b>어시스트 설계</b>")
            if 'drive' in row['cat']: spec_reasons.append("헤드라이트 눈부심을 90% 차단하는 <b>드라이브 코팅</b>")
            if abs(vision['cyl']) >= 1.0 and ('distortions' in row['cat'] or 'premium' in row['cat']): spec_reasons.append("난시 왜곡을 최소화하는 <b>양면비구면 설계</b>")
            if row['tier'] == 3: spec_reasons.append("브랜드 최상위 <b>하이엔드 등급</b>")
            
            val_reasons = []
            if type_t == "T": val_reasons.append("<b>성능 최우선</b> 성향에 맞춰 최고 스펙 제품을 선정")
            elif type_t == "F": 
                # [수정] F타입인데 비싼 제품이 1등인 경우에 대한 AI의 변명(Justification) 추가
                if row['final_price'] >= 100000:
                    val_reasons.append("가성비를 선호하시지만, <b>고객님의 시력 특성(난시/고도수)상 교정력을 위해</b> 불가피하게 성능 위주로 선정")
                else:
                    val_reasons.append("<b>가성비</b>를 최우선으로 고려하여 거품 없는 실속형 제품을 선정")
            else: val_reasons.append("가격과 성능의 <b>최적 밸런스</b>를 고려")

            c1, c2 = st.columns([1.6, 1])
            with c1:
                tags_html = "".join([f"<span class='feature-tag'>{t}</span>" for t in row['tags']])
                st.markdown(f"""
                <div class="prod-card">
                    <div class="prod-rank">{rk}위</div>
                    <div style="font-size:20px; font-weight:800; margin-top:15px; color:#111;">
                        {row['name']} <span class="match-badge">{match_percent}% 일치</span>
                    </div>
                    <div style="font-size:14px; color:#666; margin-bottom:8px;">{row['brand']} | 굴절률 {row['index_info']}</div>
                    <div class="tag-box">{tags_html}</div>
                    <div style="font-size:18px; font-weight:800; color:#2563EB;">{format(int(row['final_price']),',')}원 <span style="font-size:12px; color:#999; font-weight:normal;">(권장소비자가)</span></div>
                    <div class="why-box">
                        <div class="why-title">🧐 AI 상세 분석</div>
                        <span class="why-cat">🏢 라이프스타일 매칭</span>
                        <div class="why-desc">{' / '.join(life_reasons) if life_reasons else '일상적인 생활 패턴'}에 적합합니다.</div>
                        <span class="why-cat">👁️ 기술적 해결책</span>
                        <div class="why-desc">{' + '.join(spec_reasons) if spec_reasons else '표준 광학 설계'}가 적용되었습니다.</div>
                        <span class="why-cat">⚖️ 선정 기준</span>
                        <div class="why-desc">{val_reasons[0]}했습니다.</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.plotly_chart(make_radar_chart(row['name'], [row['thin_score'], row['view'], row['coat'], row['visual_price_score'], 9], ['두께(얇음)', '시야(넓음)', '코팅(강함)', '가격경쟁력', '적합도']), use_container_width=True)

    with tab2:
        st.markdown("### 💧 콘택트렌즈 솔루션 Best 3")
        df_c = load_data('contacts')
        is_toric = True if abs(vision['cyl']) >= 0.75 and not vision['dont_know'] else False
        cand_c = df_c[df_c['category'].str.contains('toric' if is_toric else 'sphere')].copy()
        for i, r in cand_c.iterrows():
            norm_spec = r['dry_score'] # 0~10
            if ans['sen_1'] >= 4: norm_spec += 2
            
            price_score = max(2, 10 - (r['price'] / 10000))
            
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            
            cand_c.at[i, 'total_score'] = total_score
            cand_c.at[i, 'visual_price_score'] = price_score

        ranks_c = cand_c.sort_values('total_score', ascending=False).head(3)
        top_score_c = ranks_c.iloc[0]['total_score']
        for rk, (idx, row) in enumerate(ranks_c.iterrows(), 1):
            match_percent = int((row['total_score'] / top_score_c) * 98)
            
            life_reasons = []
            if ans['sen_1'] >= 4: life_reasons.append("오후 시간대 극심한 건조감 호소")
            elif ans['sen_1'] == 3: life_reasons.append("간헐적인 눈 마름 증상")
            if type_i == "I": life_reasons.append("건조한 실내/디지털 환경 상주")
            
            spec_reasons = []
            if row['dkt'] >= 130: spec_reasons.append(f"<b>압도적인 산소투과율(Dk/t {row['dkt']})</b>")
            elif row['dkt'] >= 100: spec_reasons.append(f"우수한 산소 전달량(Dk/t {row['dkt']})")
            if row['dry_score'] >= 9: spec_reasons.append("최상급 습윤성 재질")
            
            val_reasons = []
            if type_t == "T": val_reasons.append("눈 건강을 위해 <b>최고 스펙</b> 제품을 선정")
            elif type_t == "F":
                if row['price'] >= 60000:
                    val_reasons.append("가성비를 선호하시지만, <b>장시간 착용과 건조감 해결을 위해</b> 프리미엄 제품을 권장")
                else:
                    val_reasons.append("매일 착용해도 부담 없는 <b>합리적 가격</b>을 우선")
            else: val_reasons.append("가격과 성능의 <b>최적 밸런스</b>를 고려")

            c1, c2 = st.columns([1.6, 1])
            with c1:
                tags_html = "".join([f"<span class='feature-tag'>{t}</span>" for t in row['tags']])
                st.markdown(f"""
                <div class="prod-card">
                    <div class="prod-rank">{rk}위</div>
                    <div style="font-size:20px; font-weight:800; margin-top:15px; color:#111;">
                        {row['name']} <span class="match-badge">{match_percent}% 일치</span>
                    </div>
                    <div style="font-size:14px; color:#666; margin-bottom:8px;">{row['brand']}</div>
                    <div class="tag-box">{tags_html}</div>
                    <div style="font-size:18px; font-weight:800; color:#2563EB;">{format(row['price'],',')}원 <span style="font-size:12px; color:#999; font-weight:normal;">(권장소비자가)</span></div>
                    <div class="why-box">
                        <div class="why-title">🧐 AI 상세 분석</div>
                        <span class="why-cat">🏢 라이프스타일 매칭</span>
                        <div class="why-desc">{' / '.join(life_reasons) if life_reasons else '데일리 케어'}에 집중했습니다.</div>
                        <span class="why-cat">👁️ 기술적 해결책</span>
                        <div class="why-desc">{' + '.join(spec_reasons) if spec_reasons else '표준 재질'}이 눈을 보호합니다.</div>
                        <span class="why-cat">⚖️ 선정 기준</span>
                        <div class="why-desc">{val_reasons[0]}했습니다.</div>
                    </div>
                </div>""", unsafe_allow_html=True)
            with c2: 
                st.plotly_chart(make_radar_chart(row['name'], [row['dry_score'], row['handling'], min(row['dkt']/16, 10), row['visual_price_score'], 9.5], ['건조감', '핸들링', '산소', '가격경쟁력', '적합도']), use_container_width=True)

    ans_str = "".join([str(ans[k]) for k in all_q_keys])
    dk_flag = '1' if vision['dont_know'] else '0'
    params = f"mode=result&mbti={mbti_res}&sph={vision['sph']}&cyl={vision['cyl']}&env={stat_env}&sen={stat_sen}&val={stat_val}&pro={stat_pro}&answers={ans_str}&dk={dk_flag}"
    qr_url = f"{BASE_URL}?{params}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2); qr.add_data(qr_url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white"); buffered = BytesIO(); img.save(buffered, format="PNG"); img_str = base64.b64encode(buffered.getvalue()).decode()
    
    st.markdown(f"""
    <div class="qr-container">
        <div style="font-weight:bold; margin-bottom:10px; font-size:16px;">👨‍⚕️ 안경사 전용 리포트 (Scan Me)</div>
        <img src="data:image/png;base64,{img_str}" width="160">
        <div class="capture-guide">📸 이 화면을 캡처해서 안경사님께 보여주세요!</div>
        <div style="font-size:12px; color:#888; margin-top:5px; margin-bottom:20px;">
            (또는 QR코드를 스캔하면 상세 분석 화면으로 이동합니다)
        </div>
        <div style="border-top:1px solid #eee; padding-top:20px; text-align:left;">
            <div style="font-weight:bold; margin-bottom:12px; font-size:14px; color:#2563EB;">📊 고객 성향 정량 분석 (10점 만점)</div>
        </div>
    </div>""", unsafe_allow_html=True)
    
    metrics = [("디지털/실내 환경", stat_env), ("각막 민감도", stat_sen), ("가격 민감도", stat_val), ("관리 숙련도", stat_pro)]
    for label, val in metrics:
        col1, col2 = st.columns([2, 5])
        with col1: st.write(f"**{label}** ({val}점)")
        with col2: st.progress(val / 10)
    
    st.markdown("<div style='margin-bottom:30px;'></div>", unsafe_allow_html=True)
    if st.button("처음으로 돌아가기", use_container_width=True): go_to('home'); st.rerun()
