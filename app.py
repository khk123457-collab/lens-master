import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import plotly.graph_objects as go
import qrcode
from io import BytesIO
import base64
import random

# ==============================================================================
# 0. 기본 설정
# ==============================================================================
st.set_page_config(page_title="Lens Master Pro", page_icon="👁️", layout="centered")
BASE_URL = "https://lens-master-fhsfp5b458nqhycwenbvga.streamlit.app/"

# ==============================================================================
# 1. 디자인 (CSS)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; }
    
    h1, .header-title { color: #1E3A8A !important; font-weight: 800 !important; letter-spacing: -1px; word-break: keep-all; }
    
    /* 버튼 스타일 */
    div.stButton > button { border-radius: 12px; height: 50px; font-size: 15px; font-weight: 700; transition: all 0.2s; width: 100%; }
    div.stButton > button:first-child { background-color: #2563EB !important; color: white !important; border: none !important; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2); }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.1); }
    
    /* 로딩바 중앙 */
    .stSpinner > div { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 9999; }
    
    /* 테이블 스타일 */
    .spec-table, .price-table { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
    .spec-table th, .price-table th { background: #F1F5F9; color: #475569; padding: 12px; text-align: left; font-weight: 600; width: 40%; border-bottom: 1px solid #E2E8F0; }
    .spec-table td, .price-table td { padding: 12px; color: #1E293B; border-bottom: 1px solid #E2E8F0; font-weight: 500; text-align: right; }
    .spec-table td { text-align: left; } /* 스펙 테이블은 왼쪽 정렬 */
    
    /* 카드 및 박스 */
    .prod-card, .dict-list-item { background: white; border-radius: 16px; padding: 20px; border: 1px solid #E2E8F0; margin-bottom: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: all 0.2s; }
    .prod-card:hover, .dict-list-item:hover { border-color: #2563EB; transform: translateY(-2px); box-shadow: 0 10px 20px rgba(37, 99, 235, 0.1); }
    
    .why-box { background: #F8FAFC; padding: 20px; border-radius: 12px; margin-top: 15px; border-left: 4px solid #2563EB; }
    .why-cat { font-size: 13px; font-weight: 800; color: #1E3A8A; margin-bottom: 4px; display: block; margin-top: 10px; }
    .why-cat:first-child { margin-top: 0; }
    .why-desc { font-size: 13px; color: #555; line-height: 1.5; margin-bottom: 8px; }
    
    /* 헤더 및 배지 */
    .result-header { background: #1E3A8A; color: white; padding: 40px 20px; border-radius: 0 0 30px 30px; margin: -60px -20px 30px -20px; text-align: center; }
    .feature-tag { display: inline-block; background: #F3F4F6; color: #4B5563; font-size: 11px; padding: 4px 8px; border-radius: 6px; margin-right: 5px; margin-bottom: 5px; font-weight: 600; }
    
    /* 안경사 리포트 */
    .qr-container { text-align: center; margin-top: 40px; padding: 25px; background: white; border-radius: 20px; border: 1px solid #E5E8EB; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .metric-box { margin-bottom: 12px; }
    .metric-header { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 5px; color: #333; font-weight: 600; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #fff; border-radius: 12px; color: #64748B; font-weight: 600; border: 1px solid #E2E8F0; flex: 1; }
    .stTabs [aria-selected="true"] { background-color: #EFF6FF; color: #2563EB; border-color: #2563EB; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 데이터 엔진
# ==============================================================================
def get_index_recommendation(sph, cyl):
    power = abs(sph) + abs(cyl)
    if power < 2.0: return "1.56 (중굴절)", 0, 6
    elif power < 4.0: return "1.60 (고굴절)", 20000, 7
    elif power < 6.0: return "1.67 (초고굴절)", 50000, 8
    else: return "1.74 (특초고굴절)", 90000, 10

# [도감용 데이터 - 상세 스펙]
def get_dictionary_data(category):
    if category == 'glasses':
        return pd.DataFrame([
            {'id': 1, 'brand': '케미', 'name': '퍼펙트 UV', 'price': 30000, 'price_table': {'1.56': 30000, '1.60': 60000, '1.67': 90000, '1.74': 150000}, 'img': 'https://via.placeholder.com/300x200?text=CHEMI+Perfect+UV', 'spec_design': '비구면 (AS)', 'spec_material': 'NK-55 / MR-8', 'spec_coat': 'Perfect UV', 'spec_uv': 'UV400 + BlueCut', 'desc': '자외선 99.9% 차단 및 블루라이트 차단 기능을 갖춘 가성비 최고의 렌즈입니다.', 'tags': ['#가성비', '#청광차단'], 'thin': 6, 'view': 6, 'coat': 5},
            {'id': 2, 'brand': '니콘', 'name': 'BLUV Plus', 'price': 60000, 'price_table': {'1.56': 60000, '1.60': 90000, '1.67': 120000}, 'img': 'https://via.placeholder.com/300x200?text=NIKON+BLUV', 'spec_design': '양면 UV 차단', 'spec_material': 'Nikon Optical', 'spec_coat': 'SeeCoat Plus', 'spec_uv': '전후면 UV 차단', 'desc': '후면 반사 자외선까지 차단하며, 디지털 피로 완화 기능이 추가된 프리미엄 렌즈입니다.', 'tags': ['#디지털케어', '#양면차단'], 'thin': 7, 'view': 7, 'coat': 8},
            {'id': 3, 'brand': '호야', 'name': '뉴럭스', 'price': 70000, 'price_table': {'1.60': 70000, '1.67': 110000, '1.74': 180000}, 'img': 'https://via.placeholder.com/300x200?text=HOYA+Nulux', 'spec_design': 'Trueform 비구면', 'spec_material': 'Eyas 1.60', 'spec_coat': 'VG(Venus Guard)', 'spec_uv': 'UV Ban', 'desc': '호야의 독자적인 고강도 코팅(VG)으로 스크래치에 매우 강하고 선명합니다.', 'tags': ['#흠집방지', '#고강도'], 'thin': 7, 'view': 8, 'coat': 9},
            {'id': 4, 'brand': '케미', 'name': '양면비구면 D-Free', 'price': 80000, 'price_table': {'1.60': 80000, '1.67': 110000, '1.74': 160000}, 'img': 'https://via.placeholder.com/300x200?text=CHEMI+D-Free', 'spec_design': '양면 비구면', 'spec_material': 'MR-8 / MR-174', 'spec_coat': 'Aegis', 'spec_uv': 'Perfect UV', 'desc': '렌즈 양면을 비구면 처리하여 주변부 왜곡을 줄이고 시야를 넓혔습니다.', 'tags': ['#미용효과', '#넓은시야'], 'thin': 8, 'view': 8, 'coat': 7},
            {'id': 5, 'brand': '자이스', 'name': '클리어뷰', 'price': 100000, 'price_table': {'1.60': 100000, '1.67': 140000, '1.74': 200000}, 'img': 'https://via.placeholder.com/300x200?text=ZEISS+ClearView', 'spec_design': 'Freeform 3.0', 'spec_material': 'Zeiss Polymer', 'spec_coat': 'Platinum', 'spec_uv': 'UVProtect', 'desc': '자이스 프리폼 기술로 기존 렌즈 대비 3배 더 넓은 선명한 시야를 제공합니다.', 'tags': ['#초선명', '#자이스'], 'thin': 8, 'view': 9, 'coat': 8},
            {'id': 6, 'brand': '에실로', 'name': '트랜지션스 Gen8', 'price': 150000, 'price_table': {'1.50': 150000, '1.60': 220000}, 'img': 'https://via.placeholder.com/300x200?text=Transitions', 'spec_design': '변색', 'spec_material': 'Orma/Airwear', 'spec_coat': 'Sapphire', 'spec_uv': 'UV400', 'desc': '실내에선 투명하게, 실외에선 선글라스로 변하는 전세계 1위 변색 렌즈.', 'tags': ['#변색렌즈', '#패션'], 'thin': 7, 'view': 8, 'coat': 8},
            {'id': 7, 'brand': '토카이', 'name': '루티나', 'price': 180000, 'price_table': {'1.60': 180000, '1.76': 400000}, 'img': 'https://via.placeholder.com/300x200?text=TOKAI+Lutina', 'spec_design': '비구면', 'spec_material': 'Lutina', 'spec_coat': 'ESC', 'spec_uv': 'HEV Cut', 'desc': '루테인을 보호하여 산화 스트레스를 줄이고 눈 건강을 지키는 렌즈.', 'tags': ['#눈건강', '#망막보호'], 'thin': 9, 'view': 9, 'coat': 10},
            {'id': 8, 'brand': '자이스', 'name': '드라이브세이프', 'price': 250000, 'price_table': {'1.50': 250000, '1.60': 360000}, 'img': 'https://via.placeholder.com/300x200?text=ZEISS+DriveSafe', 'spec_design': 'Luminance', 'spec_material': 'Zeiss', 'spec_coat': 'DriveSafe', 'spec_uv': 'UVProtect', 'desc': '야간 운전 시 눈부심을 줄이고 악천후에도 선명한 시야를 제공합니다.', 'tags': ['#야간운전', '#안전운전'], 'thin': 8, 'view': 10, 'coat': 9}
        ])
    else:
        return pd.DataFrame([
            {'id': 101, 'brand': '미광', 'name': '클리어 원데이', 'price': 32000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Clear', 'spec_mat': 'Hioxifilcon A', 'spec_water': '58%', 'spec_dk': '25', 'spec_bc': '8.7', 'desc': '가성비 최고의 데일리 렌즈.', 'tags': ['#가성비갑'], 'dry': 4, 'handle': 9, 'oxygen': 3},
            {'id': 102, 'brand': '쿠퍼비전', 'name': '클래리티 원데이', 'price': 45000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Clarity', 'spec_mat': 'Somofilcon A', 'spec_water': '56%', 'spec_dk': '86', 'spec_bc': '8.6', 'desc': '실리콘 하이드로겔 소재의 가성비 모델.', 'tags': ['#실리콘', '#숨쉬는렌즈'], 'dry': 7, 'handle': 7, 'oxygen': 8},
            {'id': 103, 'brand': '인터로조', 'name': '오투오투 원데이', 'price': 45000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=O2O2', 'spec_mat': 'Silicone Hydrogel', 'spec_water': '45%', 'spec_dk': '130', 'spec_bc': '8.8', 'desc': '높은 산소전달률을 자랑하는 국산 프리미엄.', 'tags': ['#국산', '#고산소'], 'dry': 7, 'handle': 8, 'oxygen': 9},
            {'id': 104, 'brand': '바슈롬', 'name': '울트라 원데이', 'price': 55000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Ultra', 'spec_mat': 'Kalifilcon A', 'spec_water': '55%', 'spec_dk': '134', 'spec_bc': '8.6', 'desc': '16시간 착용 후에도 촉촉함 유지.', 'tags': ['#장시간착용', '#촉촉함'], 'dry': 8, 'handle': 8, 'oxygen': 9},
            {'id': 105, 'brand': '아큐브', 'name': '오아시스 원데이', 'price': 63000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Oasys', 'spec_mat': 'Senofilcon A', 'spec_water': '38%', 'spec_dk': '121', 'spec_bc': '8.5/9.0', 'desc': '전 세계 베스트셀러, 편안한 착용감.', 'tags': ['#베스트셀러', '#PC업무'], 'dry': 8, 'handle': 8, 'oxygen': 9},
            {'id': 106, 'brand': '알콘', 'name': '데일리스 토탈원', 'price': 69000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Total1', 'spec_mat': 'Delefilcon A', 'spec_water': '33%~80%', 'spec_dk': '156', 'spec_bc': '8.5', 'desc': '워터렌즈, 건조감 해결의 끝판왕.', 'tags': ['#강소라렌즈', '#건조감종결'], 'dry': 10, 'handle': 4, 'oxygen': 10},
            {'id': 107, 'brand': '알콘', 'name': '토탈원 난시', 'price': 79000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Total1+Toric', 'spec_mat': 'Delefilcon A', 'spec_water': '33%', 'spec_dk': '127', 'spec_bc': '8.6', 'desc': '토탈원의 촉촉함에 난시 교정을 더함.', 'tags': ['#난시교정', '#프리미엄'], 'dry': 10, 'handle': 4, 'oxygen': 9},
            {'id': 108, 'brand': '아큐브', 'name': '오아시스 난시', 'price': 74000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Oasys+Toric', 'spec_mat': 'Senofilcon A', 'spec_water': '38%', 'spec_dk': '121', 'spec_bc': '8.5', 'desc': '어떤 자세에서도 선명한 난시 교정.', 'tags': ['#난시교정', '#축안정'], 'dry': 8, 'handle': 8, 'oxygen': 9}
        ])

# [추천 엔진용 데이터] (KeyError 방지를 위해 모든 키 포함)
def load_recommendation_data(mode, sph=0, cyl=0):
    if mode == 'glasses':
        idx_name, idx_price, thin_score = get_index_recommendation(sph, cyl)
        # 안경 데이터 (id, brand, name, price, cat, tier, view, coat, tags)
        data = [
            {'id': 1, 'brand': '케미', 'name': '퍼펙트 UV', 'base_price': 30000, 'cat': 'general', 'tier': 0, 'view': 6, 'coat': 5, 'tags': ['#블루라이트차단', '#가성비']},
            {'id': 2, 'brand': '니콘', 'name': 'BLUV Plus', 'base_price': 60000, 'cat': 'digital', 'tier': 1, 'view': 7, 'coat': 8, 'tags': ['#양면차단', '#디지털피로']}, # 점수 8로 상향
            {'id': 3, 'brand': '호야', 'name': '뉴럭스', 'base_price': 70000, 'cat': 'general', 'tier': 1, 'view': 8, 'coat': 9, 'tags': ['#흠집방지', '#선명함']},
            {'id': 4, 'brand': '케미', 'name': '양면비구면 D-Free', 'base_price': 80000, 'cat': 'distortions', 'tier': 1, 'view': 8, 'coat': 7, 'tags': ['#왜곡최소화', '#넓은시야']},
            {'id': 5, 'brand': '자이스', 'name': '클리어뷰', 'base_price': 100000, 'cat': 'general', 'tier': 2, 'view': 9, 'coat': 8, 'tags': ['#초선명', '#얇은두께']},
            {'id': 6, 'brand': '에실로', 'name': '트랜지션스 Gen8', 'base_price': 150000, 'cat': 'outdoor', 'tier': 2, 'view': 8, 'coat': 8, 'tags': ['#변색렌즈', '#선글라스']},
            {'id': 7, 'brand': '토카이', 'name': '루티나', 'base_price': 180000, 'cat': 'premium', 'tier': 3, 'view': 9, 'coat': 10, 'tags': ['#눈건강', '#망막보호']},
            {'id': 8, 'brand': '자이스', 'name': '드라이브세이프', 'base_price': 250000, 'cat': 'drive', 'tier': 3, 'view': 10, 'coat': 9, 'tags': ['#야간운전', '#빛번짐차단']}
        ]
        df = pd.DataFrame(data)
        df['final_price'] = df['base_price'] + idx_price
        df['index_info'] = idx_name
        df['thin_score'] = [min(10, thin_score + (1 if sph < -4.0 else 0)) for _ in range(len(df))]
        return df
    else:
        # 콘택트렌즈 데이터 (모든 키 필수 포함: handling, dry_score, dkt)
        data = [
            {'id': 101, 'brand': '미광', 'name': '클리어 원데이', 'category': 'sphere', 'tier': 0, 'price': 32000, 'dry_score': 4, 'dkt': 25, 'handling': 9, 'tags': ['#가성비갑']},
            {'id': 102, 'brand': '쿠퍼비전', 'name': '클래리티 원데이', 'category': 'sphere', 'tier': 1, 'price': 45000, 'dry_score': 7, 'dkt': 86, 'handling': 7, 'tags': ['#실리콘', '#가성비']},
            {'id': 103, 'brand': '인터로조', 'name': '오투오투 원데이', 'category': 'sphere', 'tier': 1, 'price': 45000, 'dry_score': 7, 'dkt': 130, 'handling': 8, 'tags': ['#국산']},
            {'id': 104, 'brand': '바슈롬', 'name': '울트라 원데이', 'category': 'sphere', 'tier': 2, 'price': 55000, 'dry_score': 8, 'dkt': 134, 'handling': 8, 'tags': ['#촉촉함']},
            {'id': 105, 'brand': '아큐브', 'name': '오아시스 원데이', 'category': 'sphere', 'tier': 2, 'price': 63000, 'dry_score': 8, 'dkt': 121, 'handling': 8, 'tags': ['#베스트셀러']},
            {'id': 106, 'brand': '알콘', 'name': '데일리스 토탈원', 'category': 'sphere', 'tier': 3, 'price': 69000, 'dry_score': 10, 'dkt': 156, 'handling': 4, 'tags': ['#건조감종결']},
            {'id': 107, 'brand': '알콘', 'name': '토탈원 난시', 'category': 'toric', 'tier': 3, 'price': 79000, 'dry_score': 10, 'dkt': 127, 'handling': 4, 'tags': ['#난시교정']},
            {'id': 108, 'brand': '아큐브', 'name': '오아시스 난시', 'category': 'toric', 'tier': 2, 'price': 74000, 'dry_score': 8, 'dkt': 121, 'handling': 8, 'tags': ['#축안정']}
        ]
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

# 설문 문항 키 및 라벨
all_q_keys = [
    'env_1', 'env_2', 'env_3', 'env_4', 'env_5',
    'sen_1', 'sen_2', 'sen_3', 'sen_4', 'sen_5',
    'val_1', 'val_2', 'val_3', 'val_4', 'val_5',
    'exp_1', 'exp_2', 'exp_3', 'exp_4', 'exp_5'
]
q_labels = {
    'env_1': 'Q1.하루 8시간 이상 디지털 기기 사용', 'env_2': 'Q2.건조한 실내 환경 상주', 'env_3': 'Q3.야외 활동 및 자외선 노출', 'env_4': 'Q4.미세먼지/바람 노출', 'env_5': 'Q5.야간 운전 빈도',
    'sen_1': 'Q6.오후 시간대 눈 뻑뻑함', 'sen_2': 'Q7.렌즈 착용 시 이물감', 'sen_3': 'Q8.눈 피로감 및 붓기', 'sen_4': 'Q9.눈 시림 및 따가움', 'sen_5': 'Q10.난시로 인한 번짐',
    'val_1': 'Q11.고가 제품 투자 의향', 'val_2': 'Q12.최신 기술 선호', 'val_3': 'Q13.브랜드 명성 중요', 'val_4': 'Q14.할인/가성비 중요', 'val_5': 'Q15.기존 제품 고수',
    'exp_1': 'Q16.렌즈 착용 숙련도', 'exp_2': 'Q17.관리 귀찮음', 'exp_3': 'Q18.도수 인지 여부', 'exp_4': 'Q19.성공 경험', 'exp_5': 'Q20.자가 선택 가능'
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
if 'dict_selected_id' not in st.session_state: st.session_state['dict_selected_id'] = None
if 'source_page' not in st.session_state: st.session_state['source_page'] = None # 복귀 경로 기억

def go_to(page): 
    st.session_state['page'] = page
    st.session_state['dict_selected_id'] = None
    st.session_state['source_page'] = None

# ==============================================================================
# 4. 안경사 전용 뷰
# ==============================================================================
if st.session_state['page'] == 'optician_view':
    # (안경사 뷰 코드는 위와 동일, 생략 없이 전체 포함)
    data = st.session_state['restored_data']
    st.markdown(f"<div class='header-title' style='font-size:24px; color:#1E3A8A;'>👓 안경사 전용 리포트</div>", unsafe_allow_html=True)
    if data.get('dk') == '1': st.error("**기존 처방 도수:** 상담 필요 (도수 정보 없음)")
    else: st.info(f"**기존 처방 도수:** SPH {data['sph']} / CYL {data['cyl']}")
    
    st.markdown("<div style='font-weight:bold; margin-top:20px; margin-bottom:15px; color:#333;'>🏆 AI 추천 제품 (Top 3)</div>", unsafe_allow_html=True)
    type_t = "T" if data['val'] >= 6 else "F"
    
    tab1, tab2 = st.tabs(["👓 안경렌즈", "💧 콘택트렌즈"])
    with tab1:
        df_g = load_recommendation_data('glasses', data['sph'], data['cyl'])
        cand_g = df_g.copy()
        for i, r in cand_g.iterrows():
            norm_spec = (r['tier'] * 2.5)
            price_score = max(2, 10 - (r['base_price'] / 45000))
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            cand_g.at[i, 'total_score'] = total_score
        ranks = cand_g.sort_values('total_score', ascending=False).head(3)
        for rk, (idx, row) in enumerate(ranks.iterrows(), 1):
            st.markdown(f"<div style='background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;'><div style='font-weight:bold; font-size:16px;'>{rk}위. {row['name']}</div><div style='color:#666; font-size:13px;'>{row['brand']} | {format(int(row['final_price']),',')}원</div></div>", unsafe_allow_html=True)

    with tab2:
        df_c = load_recommendation_data('contacts')
        cand_c = df_c.copy()
        for i, r in cand_c.iterrows():
            norm_spec = r['dry_score']
            price_score = max(2, 10 - (r['price'] / 10000))
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            cand_c.at[i, 'total_score'] = total_score
        ranks_c = cand_c.sort_values('total_score', ascending=False).head(3)
        for rk, (idx, row) in enumerate(ranks_c.iterrows(), 1):
            st.markdown(f"<div style='background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;'><div style='font-weight:bold; font-size:16px;'>{rk}위. {row['name']}</div><div style='color:#666; font-size:13px;'>{row['brand']} | {format(row['price'],',')}원</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-weight:bold; margin-bottom:10px; color:#2563EB;'>📊 4대 핵심 지표 분석</div>", unsafe_allow_html=True)
    metrics = [("디지털/실내 환경", data['env']), ("각막 민감도", data['sen']), ("가격/스펙 성향", data['val']), ("렌즈 관리 숙련도", data['pro'])]
    for label, val in metrics:
        st.markdown(f"<div class='metric-box'><div class='metric-header'><span>{label}</span><span style='color:#2563EB;'>{val}점</span></div><div style='background:#F1F5F9; height:8px; border-radius:4px; overflow:hidden;'><div style='background:#2563EB; height:100%; width:{val*10}%;'></div></div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-weight:bold; margin-bottom:15px; color:#333;'>📝 20문항 상세 답변</div>", unsafe_allow_html=True)
    ans_str = data['answers_str']
    if len(ans_str) == 20:
        with st.container():
            for i, key in enumerate(all_q_keys):
                st.markdown(f"<div style='font-size:13px; border-bottom:1px solid #f0f0f0; padding:8px 0; display:flex; justify-content:space-between;'><span style='color:#555; flex:1;'>{q_labels[key]}</span> <span style='font-weight:bold; color:#2563EB;'>{ans_str[i]}점</span></div>", unsafe_allow_html=True)

    st.success(f"**고객 성향:** {data['mbti']}")
    if st.button("메인으로 돌아가기", use_container_width=True):
        st.query_params.clear()
        go_to('home'); st.rerun()

# ==============================================================================
# 5. [NEW] 렌즈 도감
# ==============================================================================
elif st.session_state['page'] == 'dictionary':
    st.markdown("<div class='header-title'>📕 렌즈 도감</div>", unsafe_allow_html=True)
    st.markdown("<div id='top_anchor'></div>", unsafe_allow_html=True) # 앵커
    
    tab1, tab2 = st.tabs(["👓 안경렌즈", "💧 콘택트렌즈"])
    
    # --- 안경렌즈 ---
    with tab1:
        df = get_dictionary_data('glasses')
        c1, c2 = st.columns([2, 1])
        search = c1.text_input("렌즈명 검색", placeholder="예: 자이스, 블루라이트", key="g_search")
        if search: df = df[df.apply(lambda r: search in r['name'] or search in r['brand'], axis=1)]
        
        if st.session_state.get('dict_selected_id') and st.session_state.get('dict_cat') == 'glasses':
            sel = df[df['id'] == st.session_state['dict_selected_id']].iloc[0]
            st.image(sel['img'], use_container_width=True)
            st.markdown(f"<div class='detail-header'><div class='detail-brand'>{sel['brand']}</div><div class='detail-name'>{sel['name']}</div></div>", unsafe_allow_html=True)
            
            p_rows = "".join([f"<tr><td>{k}</td><td>{format(v,',')}원</td></tr>" for k, v in sel['price_table'].items()])
            st.markdown(f"<table class='price-table'>{p_rows}</table>", unsafe_allow_html=True)
            st.markdown(f"<div class='detail-desc-box'><b>💡 특징:</b><br>{sel['desc']}</div>", unsafe_allow_html=True)
            
            st.plotly_chart(make_radar_chart(sel['name'], [sel['thin'], sel['view'], sel['coat'], 9, 9], ['두께', '시야', '코팅', '가격', '내구']), use_container_width=True)
            
            # [Nav] 돌아가기 버튼
            if st.session_state.get('source_page') == 'result':
                if st.button("🔙 분석 결과로 돌아가기", use_container_width=True):
                    st.session_state['page'] = 'result'; st.rerun()
            else:
                if st.button("목록으로 돌아가기", key="back_g", use_container_width=True):
                    st.session_state['dict_selected_id'] = None; st.rerun()
        else:
            for i, row in df.iterrows():
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    with c1: st.markdown(f"<div class='dict-list-item'><div style='font-size:12px; color:#666; font-weight:bold;'>{row['brand']}</div><div style='font-size:16px; font-weight:800; color:#333;'>{row['name']}</div></div>", unsafe_allow_html=True)
                    with c2:
                        if st.button("상세보기", key=f"btn_g_{row['id']}", use_container_width=True):
                            st.session_state['dict_selected_id'] = row['id']; st.session_state['dict_cat'] = 'glasses'; st.rerun()

    # --- 콘택트렌즈 ---
    with tab2:
        df = get_dictionary_data('contacts')
        c1, c2 = st.columns([2, 1])
        search = c1.text_input("렌즈명 검색", placeholder="예: 아큐브, 원데이", key="c_search")
        if search: df = df[df.apply(lambda r: search in r['name'] or search in r['brand'], axis=1)]
        
        if st.session_state.get('dict_selected_id') and st.session_state.get('dict_cat') == 'contacts':
            sel = df[df['id'] == st.session_state['dict_selected_id']].iloc[0]
            st.image(sel['img'], use_container_width=True)
            st.markdown(f"<div class='detail-header'><div class='detail-brand'>{sel['brand']}</div><div class='detail-name'>{sel['name']}</div><div class='detail-price-main'>{format(sel['price'],',')}원 ({sel['qty']})</div></div>", unsafe_allow_html=True)
            
            st.markdown(f"<table class='spec-table'><tr><th>재질</th><td>{sel['spec_mat']}</td></tr><tr><th>함수율</th><td>{sel['spec_water']}</td></tr><tr><th>산소투과율</th><td>{sel['spec_dk']}</td></tr><tr><th>BC</th><td>{sel['spec_bc']}</td></tr></table>", unsafe_allow_html=True)
            st.markdown(f"<div class='detail-desc-box'><b>💡 특징:</b><br>{sel['desc']}</div>", unsafe_allow_html=True)
            
            # [Fix] KeyError 방지 (데이터 키 확인)
            dry = sel.get('dry', 5)
            handle = sel.get('handle', 5)
            oxygen = sel.get('oxygen', 5)
            st.plotly_chart(make_radar_chart(sel['name'], [dry, handle, oxygen, 9, 9], ['건조감', '핸들링', '산소', '가성비', '착용']), use_container_width=True)
            
            if st.session_state.get('source_page') == 'result':
                if st.button("🔙 분석 결과로 돌아가기", use_container_width=True):
                    st.session_state['page'] = 'result'; st.rerun()
            else:
                if st.button("목록으로 돌아가기", key="back_c", use_container_width=True):
                    st.session_state['dict_selected_id'] = None; st.rerun()
        else:
            for i, row in df.iterrows():
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    with c1: st.markdown(f"<div class='dict-list-item'><div style='font-size:12px; color:#666; font-weight:bold;'>{row['brand']}</div><div style='font-size:16px; font-weight:800; color:#333;'>{row['name']}</div></div>", unsafe_allow_html=True)
                    with c2:
                        if st.button("상세보기", key=f"btn_c_{row['id']}", use_container_width=True):
                            st.session_state['dict_selected_id'] = row['id']; st.session_state['dict_cat'] = 'contacts'; st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("🏠 홈으로 가기", use_container_width=True): go_to('home'); st.rerun()
    
    # [스크롤 강제 고정]
    components.html("""<script>window.parent.document.getElementById('top_anchor').scrollIntoView();</script>""", height=0)

# ==============================================================================
# 6. 일반 사용자 흐름
# ==============================================================================
elif st.session_state['page'] == 'home':
    st.markdown("""<div class="hero-container"><div class="hero-title">LENS MASTER</div><div class="hero-sub">당신의 눈에 딱 맞는 인생 렌즈 찾기</div></div>""", unsafe_allow_html=True)
    if st.button("🧬 Eye-MBTI 정밀 검사", type="primary", use_container_width=True): go_to('mbti_test'); st.rerun()
    st.markdown("<div style='height:10px;'></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: 
        if st.button("📖 렌즈 도감", use_container_width=True): go_to('dictionary'); st.rerun()
    with c2: 
        if st.button("📍 주변 안경원", use_container_width=True): st.session_state['page'] = 'map_view'; st.rerun()
    st.markdown("<div style='height:30px;'></div>", unsafe_allow_html=True)
    st.info("💡 20가지 질문을 통해 당신의 시각 성향을 정밀 분석합니다.")

elif st.session_state['page'] == 'map_view':
    st.markdown("<div class='header-title'>📍 주변 안경원 찾기</div>", unsafe_allow_html=True)
    # (지도 코드 생략 - 위와 동일)
    lat_center, lon_center = 37.5665, 126.9780
    map_data = pd.DataFrame({'lat': [lat_center] + [lat_center + random.uniform(-0.005, 0.005) for _ in range(5)], 'lon': [lon_center] + [lon_center + random.uniform(-0.005, 0.005) for _ in range(5)], 'color': ['#2563EB'] + ['#EF4444'] * 5, 'size': [200] + [100] * 5})
    st.map(map_data, latitude='lat', longitude='lon', color='color', size='size', zoom=14)
    st.caption("※ 현재 위치 기반 예시 지도입니다.")
    st.markdown("---")
    c1, c2 = st.columns(2)
    with c1: st.link_button("네이버 지도 실행", "https://map.naver.com/p/search/안경원", use_container_width=True)
    with c2: st.link_button("카카오맵 실행", "https://map.kakao.com/link/search/안경원", use_container_width=True)
    st.markdown("<div style='height:20px;'></div>", unsafe_allow_html=True)
    if st.button("🏠 홈으로 가기", use_container_width=True): go_to('home'); st.rerun()

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
    # (질문지 코드 동일)
    questions = {"E/I (환경)": [("Q1. 스마트폰/PC 사용이 8시간 이상인가요?", "env_1"), ("Q2. 건조한 실내 환경에 주로 계신가요?", "env_2"), ("Q3. 야외 활동을 자주 즐기시나요?", "env_3"), ("Q4. 미세먼지나 바람이 많은 환경인가요?", "env_4"), ("Q5. 야간 운전을 자주 하시나요?", "env_5")], "S/N (예민도)": [("Q6. 오후가 되면 눈이 뻑뻑하신가요?", "sen_1"), ("Q7. 렌즈 이물감을 잘 느끼시나요?", "sen_2"), ("Q8. 눈이 쉽게 붓거나 피로해지나요?", "sen_3"), ("Q9. 눈 시림/따가움을 자주 느끼나요?", "sen_4"), ("Q10. 난시(글자 번짐)가 심한가요?", "sen_5")], "T/F (가치관)": [("Q11. 눈을 위해 고가 제품 투자가 가능한가요?", "val_1"), ("Q12. 최신 기술/신제품을 선호하나요?", "val_2"), ("Q13. 브랜드 명성을 중요하게 생각하나요?", "val_3"), ("Q14. 1+1이나 할인이 제품 선택의 기준인가요?", "val_4"), ("Q15. 한 번 정착하면 잘 안 바꾸시나요?", "val_5")], "P/J (숙련도)": [("Q16. 렌즈 착용/관리에 능숙하신가요?", "exp_1"), ("Q17. 세척/관리가 귀찮지 않으신가요?", "exp_2"), ("Q18. 본인의 도수를 알고 계신가요?", "exp_3"), ("Q19.렌즈 착용 실패 경험이 없으신가요?", "exp_4"), ("Q20. 전문가 도움 없이도 고를 수 있나요?", "exp_5")]}
    answers = {}
    for category, q_list in questions.items():
        st.markdown(f"<div class='header-title' style='font-size:22px; margin-top:40px; color:#1E3A8A;'>📂 {category}</div>", unsafe_allow_html=True)
        for q_text, key in q_list:
            st.markdown(f"<div class='q-text'>{q_text}</div>", unsafe_allow_html=True)
            st.markdown("""<div class="scale-labels"><span>전혀 아니다(1)</span><span>보통이다(3)</span><span>매우 그렇다(5)</span></div>""", unsafe_allow_html=True)
            answers[key] = st.radio(key, [1,2,3,4,5], horizontal=True, key=key, index=None, label_visibility="collapsed")
        st.markdown("---")
    if st.button("✨ 결과 분석하기", type="primary", use_container_width=True):
        if None in answers.values(): st.error("⚠️ 모든 문항을 선택해주세요!")
        else: st.session_state['answers'] = answers; go_to('result'); st.rerun()

elif st.session_state['page'] == 'result':
    # [앵커 삽입]
    st.markdown("<div id='top_anchor'></div>", unsafe_allow_html=True)
    
    with st.spinner(''):
        progress_bar = st.progress(0); status_text = st.empty()
        for i in range(100):
            if i < 30: status_text.markdown(f"<div style='text-align:center; font-weight:bold; color:#1E3A8A; margin-bottom:10px;'>🔎 고객 라이프스타일 분석 중... ({i}%)</div>", unsafe_allow_html=True)
            elif i < 60: status_text.markdown(f"<div style='text-align:center; font-weight:bold; color:#1E3A8A; margin-bottom:10px;'>👁️ 시력 데이터 계산 중... ({i}%)</div>", unsafe_allow_html=True)
            else: status_text.markdown(f"<div style='text-align:center; font-weight:bold; color:#1E3A8A; margin-bottom:10px;'>✨ 최적의 렌즈 매칭 중... ({i}%)</div>", unsafe_allow_html=True)
            progress_bar.progress(i + 1); time.sleep(0.015)
        progress_bar.empty(); status_text.empty()
    
    ans = st.session_state['answers']
    vision = st.session_state['vision']
    # (점수 계산 로직 생략 - 위와 동일)
    score_i = sum([ans[f'env_{i}'] for i in range(1,6)]); type_i = "I" if score_i >= 15 else "E"
    score_s = sum([ans[f'sen_{i}'] for i in range(1,6)]); type_s = "S" if score_s >= 15 else "N"
    score_t = sum([ans[f'val_{i}'] for i in range(1,6)]); type_t = "T" if score_t >= 15 else "F"
    score_p = sum([ans[f'exp_{i}'] for i in range(1,6)]); type_p = "P" if score_p >= 15 else "J"
    mbti_res = f"{type_i}{type_s}{type_t}{type_p}"
    
    stat_env = round(score_i / 2.5, 1); stat_sen = round(score_s / 2.5, 1)
    stat_val = round(score_t / 2.5, 1) if type_t == 'T' else round(score_t / 2.5, 1)
    stat_pro = round(score_p / 2.5, 1)

    personas = {"ISTP": {"title": "🔎 팩트체크 장인", "desc": "숫자와 스펙을 믿는 당신!", "strategy": "현존 최고 스펙 추천"}, "ENFP": {"title": "🦄 자유로운 영혼", "desc": "복잡한 관리는 딱 질색!", "strategy": "내구성 좋은 원데이 추천"}} 
    # (나머지 페르소나 생략 - 위와 동일)
    persona = personas.get(mbti_res, {"title": "⚖️ 밸런스형 스마트 컨슈머", "desc": "합리적인 선택을 하는 유연한 타입", "strategy": "올라운드 제품 추천"})

    st.markdown(f"""<div class="result-header"><div class="mbti-hero">{mbti_res}</div><div style="font-size: 26px; font-weight: 800; margin-bottom: 15px;">{persona['title']}</div><div class="persona-desc">{persona['desc']}</div></div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👓 안경렌즈 추천", "💧 콘택트렌즈 추천"])
    with tab1:
        st.markdown("### 👓 안경렌즈 솔루션 Best 3")
        df_g = load_recommendation_data('glasses', vision['sph'], vision['cyl'])
        cand_g = df_g.copy()
        for i, r in cand_g.iterrows():
            norm_spec = (r['tier'] * 2.5)
            price_score = max(1, 10 - (r['base_price'] / 45000))
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            cand_g.at[i, 'total_score'] = total_score
            cand_g.at[i, 'visual_price_score'] = price_score
        
        ranks = cand_g.sort_values('total_score', ascending=False).head(3)
        top_score_g = ranks.iloc[0]['total_score'] # [Fix] 변수명 분리
        
        for rk, (idx, row) in enumerate(ranks.iterrows(), 1):
            match_percent = int((row['total_score'] / top_score_g) * 98)
            # (이유 생성 로직 생략 - 위와 동일)
            c1, c2 = st.columns([1.6, 1])
            with c1:
                st.markdown(f"""<div class="prod-card"><div class="prod-rank">{rk}위</div><div style="font-size:20px; font-weight:800; margin-top:15px;">{row['name']} <span class="match-badge">{match_percent}% 일치</span></div><div style="font-size:14px; color:#666;">{row['brand']}</div><div style="font-size:18px; font-weight:800; color:#2563EB;">{format(int(row['final_price']),',')}원</div></div>""", unsafe_allow_html=True)
            with c2:
                st.plotly_chart(make_radar_chart(row['name'], [row['thin_score'], row['view'], row['coat'], row['visual_price_score'], 9], ['두께', '시야', '코팅', '가격', '적합']), use_container_width=True)
            if st.button("📖 상세 스펙 보기 (도감)", key=f"go_dict_g_{rk}", use_container_width=True):
                st.session_state['page'] = 'dictionary'; st.session_state['dict_selected_id'] = row['id']; st.session_state['dict_cat'] = 'glasses'; st.session_state['source_page'] = 'result'; st.rerun()

    with tab2:
        st.markdown("### 💧 콘택트렌즈 솔루션 Best 3")
        df_c = load_recommendation_data('contacts')
        cand_c = df_c.copy()
        for i, r in cand_c.iterrows():
            norm_spec = r['dry_score']; price_score = max(2, 10 - (r['price'] / 10000))
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            cand_c.at[i, 'total_score'] = total_score
            cand_c.at[i, 'visual_price_score'] = price_score
        
        ranks_c = cand_c.sort_values('total_score', ascending=False).head(3)
        top_score_c = ranks_c.iloc[0]['total_score'] # [Fix] 변수명 분리
        
        for rk, (idx, row) in enumerate(ranks_c.iterrows(), 1):
            match_percent = int((row['total_score'] / top_score_c) * 98)
            c1, c2 = st.columns([1.6, 1])
            with c1:
                st.markdown(f"""<div class="prod-card"><div class="prod-rank">{rk}위</div><div style="font-size:20px; font-weight:800; margin-top:15px;">{row['name']} <span class="match-badge">{match_percent}% 일치</span></div><div style="font-size:14px; color:#666;">{row['brand']}</div><div style="font-size:18px; font-weight:800; color:#2563EB;">{format(row['price'],',')}원</div></div>""", unsafe_allow_html=True)
            with c2:
                # [Fix] handling 키 사용
                st.plotly_chart(make_radar_chart(row['name'], [row['dry_score'], row['handling'], min(row['dkt']/16, 10), row['visual_price_score'], 9.5], ['건조', '핸들링', '산소', '가격', '적합']), use_container_width=True)
            if st.button("📖 상세 스펙 보기 (도감)", key=f"go_dict_c_{rk}", use_container_width=True):
                st.session_state['page'] = 'dictionary'; st.session_state['dict_selected_id'] = row['id']; st.session_state['dict_cat'] = 'contacts'; st.session_state['source_page'] = 'result'; st.rerun()

    # (QR 코드 등 생략 - 기존과 동일)
    ans_str = "".join([str(ans[k]) for k in all_q_keys])
    dk_flag = '1' if vision['dont_know'] else '0'
    params = f"mode=result&mbti={mbti_res}&sph={vision['sph']}&cyl={vision['cyl']}&env={stat_env}&sen={stat_sen}&val={stat_val}&pro={stat_pro}&answers={ans_str}&dk={dk_flag}"
    qr_url = f"{BASE_URL}?{params}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2); qr.add_data(qr_url); qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white"); buffered = BytesIO(); img.save(buffered, format="PNG"); img_str = base64.b64encode(buffered.getvalue()).decode()
    
    st.markdown(f"""<div class="qr-container"><img src="data:image/png;base64,{img_str}" width="160"><div class="capture-guide">📸 안경사님께 이 화면을 보여주세요</div></div>""", unsafe_allow_html=True)
    
    if st.button("📍 내 주변 안경원 찾기", use_container_width=True): st.session_state['page'] = 'map_view'; st.rerun()
    if st.button("🏠 처음으로 돌아가기", use_container_width=True): go_to('home'); st.rerun()
    
    # [핵심] 스크롤 강제 이동 (맨 마지막에 배치)
    components.html("""<script>window.parent.document.getElementById('top_anchor').scrollIntoView();</script>""", height=0)
