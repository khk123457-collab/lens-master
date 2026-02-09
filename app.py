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
# 0. 기본 설정 & URL
# ==============================================================================
st.set_page_config(page_title="Lens Master Pro", page_icon="👁️", layout="centered")
BASE_URL = "https://lens-master-fhsfp5b458nqhycwenbvga.streamlit.app/"

# ==============================================================================
# 1. 디자인 (CSS) - v9.0 유지
# ==============================================================================
st.markdown("""
<style>
    @import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/static/pretendard.css');
    html, body, [class*="css"] { font-family: 'Pretendard', sans-serif; background-color: #F8F9FA; }
    
    h1, .header-title { color: #1E3A8A !important; font-weight: 800 !important; letter-spacing: -1px; word-break: keep-all; }
    
    div.stButton > button { border-radius: 12px; height: 50px; font-size: 15px; font-weight: 700; transition: all 0.2s; width: 100%; }
    div.stButton > button:first-child { background-color: #2563EB !important; color: white !important; border: none !important; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.2); }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.1); }
    
    .stSpinner > div { position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); z-index: 9999; }
    
    .spec-table, .price-table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 20px; font-size: 14px; background: white; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
    .spec-table th, .price-table th { background: #F1F5F9; color: #475569; padding: 12px; text-align: left; font-weight: 600; width: 40%; border-bottom: 1px solid #E2E8F0; }
    .spec-table td, .price-table td { padding: 12px; color: #1E293B; border-bottom: 1px solid #E2E8F0; font-weight: 500; text-align: right; }
    .spec-table td { text-align: left; }
    
    .prod-card { background: white; border-radius: 16px; padding: 25px; border: 1px solid #E2E8F0; margin-bottom: 20px; box-shadow: 0 8px 20px rgba(0,0,0,0.05); position: relative; overflow: hidden; }
    .prod-rank { position: absolute; top: 0; left: 0; background: #2563EB; color: white; padding: 6px 16px; border-radius: 0 0 16px 0; font-weight: 800; font-size: 14px; z-index: 10; }
    .match-point { position: absolute; top: 15px; right: 15px; background: #EFF6FF; color: #2563EB; font-weight: 800; font-size: 13px; padding: 6px 12px; border-radius: 20px; border: 1px solid #DBEAFE; }
    
    .why-box { background: #F8FAFC; padding: 20px; border-radius: 12px; margin-top: 15px; border-left: 4px solid #2563EB; }
    .why-cat { font-size: 13px; font-weight: 800; color: #1E3A8A; margin-bottom: 4px; display: block; margin-top: 10px; }
    .why-cat:first-child { margin-top: 0; }
    .why-desc { font-size: 13px; color: #555; line-height: 1.5; margin-bottom: 8px; }
    
    .feature-tag { display: inline-block; background: #F3F4F6; color: #4B5563; font-size: 11px; padding: 4px 8px; border-radius: 6px; margin-right: 5px; margin-bottom: 5px; font-weight: 600; }
    
    .qr-container { text-align: center; margin-top: 40px; padding: 25px; background: white; border-radius: 20px; border: 1px solid #E5E8EB; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .metric-box { margin-bottom: 12px; }
    .metric-header { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 5px; color: #333; font-weight: 600; }
    
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background-color: transparent; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #fff; border-radius: 12px; color: #64748B; font-weight: 600; border: 1px solid #E2E8F0; flex: 1; }
    .stTabs [aria-selected="true"] { background-color: #EFF6FF; color: #2563EB; border-color: #2563EB; }
    
    .hero-container { text-align: center; padding: 50px 20px 30px; }
    .hero-title { font-size: 36px; font-weight: 900; color: #1E3A8A; margin-bottom: 10px; text-shadow: 0 2px 10px rgba(30, 58, 138, 0.1); }
    .hero-sub { font-size: 16px; color: #64748B; font-weight: 500; margin-bottom: 40px; }
    
    .dict-list-item { padding: 15px; background: white; border-radius: 12px; margin-bottom: 10px; border: 1px solid #E2E8F0; cursor: pointer; transition: all 0.2s; }
    .dict-list-item:hover { border-color: #2563EB; box-shadow: 0 4px 10px rgba(37, 99, 235, 0.1); }
    
    .detail-header { background: white; padding: 25px; border-radius: 20px; text-align: center; margin-bottom: 20px; border: 1px solid #E2E8F0; }
    .detail-brand { font-size: 14px; color: #64748B; font-weight: 600; }
    .detail-name { font-size: 24px; font-weight: 900; color: #1E293B; margin: 5px 0 10px 0; }
    .detail-price-main { font-size: 20px; font-weight: 800; color: #2563EB; margin-bottom: 10px; }
    .detail-desc-box { background: white; padding: 20px; border-radius: 12px; border: 1px solid #E2E8F0; margin-bottom: 20px; line-height: 1.6; color: #334155; font-size: 15px; }
    
    .result-header { background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%); color: white; padding: 40px 20px; border-radius: 0 0 30px 30px; margin: -60px -20px 30px -20px; text-align: center; box-shadow: 0 10px 30px rgba(37, 99, 235, 0.3); }
    .mbti-hero { font-size: 60px !important; font-weight: 900; margin: 10px 0; text-shadow: 0 4px 10px rgba(0,0,0,0.3); letter-spacing: 3px; color: #FFFFFF; }
    .persona-desc { background: rgba(255,255,255,0.15); padding: 20px; border-radius: 15px; font-size: 15px; line-height: 1.6; margin-top: 20px; text-align: left; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.2); }

    /* 질문지 */
    .q-text { font-size: 17px; font-weight: 700; color: #111; margin-top: 35px; margin-bottom: 12px; word-break: keep-all; }
    .scale-labels { display: flex; justify-content: space-between; font-size: 12px; color: #888; font-weight: 500; padding: 0 10px; margin-bottom: 8px; }
    div[role="radiogroup"] { gap: 0; justify-content: space-between; margin-bottom: 20px; }
    div[role="radiogroup"] label { background-color: white !important; border: 1px solid #E5E8EB !important; border-radius: 50% !important; width: 48px; height: 48px; display: flex; justify-content: center; align-items: center; cursor: pointer; transition: all 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275); box-shadow: 0 2px 5px rgba(0,0,0,0.03); }
    div[role="radiogroup"] label:hover { background-color: #F8FAFC !important; transform: translateY(-3px); }
    div[role="radiogroup"] label:has(input:checked) { background-color: #2563EB !important; border-color: #2563EB !important; box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3); transform: scale(1.1); }
    div[role="radiogroup"] label p { font-size: 16px !important; margin: 0 !important; color: #888 !important; }
    div[role="radiogroup"] label:has(input:checked) p { color: white !important; font-weight: bold !important; }
    div[role="radiogroup"] label > div:first-child { display: none; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. 데이터 엔진 (상세 분석용 'ai_summary' 필드 추가)
# ==============================================================================
def get_index_recommendation(sph, cyl):
    power = abs(sph) + abs(cyl)
    if power < 2.0: return "1.56 (중굴절)", 0, 6
    elif power < 4.0: return "1.60 (고굴절)", 20000, 7
    elif power < 6.0: return "1.67 (초고굴절)", 50000, 8
    else: return "1.74 (특초고굴절)", 90000, 10

def get_dictionary_data(category):
    # (도감 데이터는 v9.0과 동일, 생략 없이 유지)
    if category == 'glasses':
        return pd.DataFrame([
            {'id': 1, 'brand': '케미', 'name': '퍼펙트 UV', 'price': 30000, 'price_table': {'1.56 (중굴절)': 30000, '1.60 (고굴절)': 60000, '1.67 (초고굴절)': 90000, '1.74 (특초)': 150000}, 'img': 'https://via.placeholder.com/300x200?text=CHEMI+Perfect+UV', 'spec_design': '비구면 (AS)', 'spec_material': 'NK-55/MR-8', 'spec_coat': 'Perfect UV', 'spec_uv': 'UV400 + BlueCut', 'desc': '자외선 99.9% 및 블루라이트 차단 가성비 렌즈.', 'tags': ['#가성비', '#청광차단'], 'thin': 6, 'view': 6, 'coat': 5},
            {'id': 2, 'brand': '니콘', 'name': 'BLUV Plus', 'price': 60000, 'price_table': {'1.56 (중굴절)': 60000, '1.60 (고굴절)': 90000, '1.67 (초고굴절)': 120000}, 'img': 'https://via.placeholder.com/300x200?text=NIKON+BLUV', 'spec_design': '양면 UV', 'spec_material': 'Nikon', 'spec_coat': 'SeeCoat', 'spec_uv': '양면차단', 'desc': '후면 반사 자외선 차단 및 디지털 피로 완화.', 'tags': ['#디지털케어', '#양면차단'], 'thin': 7, 'view': 7, 'coat': 7},
            {'id': 3, 'brand': '호야', 'name': '뉴럭스', 'price': 70000, 'price_table': {'1.60 (고굴절)': 70000, '1.67 (초고굴절)': 110000, '1.74 (특초)': 180000}, 'img': 'https://via.placeholder.com/300x200?text=HOYA+Nulux', 'spec_design': 'Trueform', 'spec_material': 'Eyas 1.60', 'spec_coat': 'VG(Venus Guard)', 'spec_uv': 'UV Ban', 'desc': '스크래치에 강한 고강도 코팅.', 'tags': ['#흠집방지', '#고강도'], 'thin': 7, 'view': 8, 'coat': 9},
            {'id': 4, 'brand': '케미', 'name': '양면비구면 D-Free', 'price': 80000, 'price_table': {'1.60 (고굴절)': 80000, '1.67 (초고굴절)': 110000, '1.74 (특초)': 160000}, 'img': 'https://via.placeholder.com/300x200?text=CHEMI+D-Free', 'spec_design': '양면비구면', 'spec_material': 'MR-8', 'spec_coat': 'Aegis', 'spec_uv': 'UV400', 'desc': '주변부 왜곡 최소화.', 'tags': ['#미용효과', '#난시교정'], 'thin': 8, 'view': 8, 'coat': 7},
            {'id': 5, 'brand': '자이스', 'name': '클리어뷰', 'price': 100000, 'price_table': {'1.60 (고굴절)': 100000, '1.67 (초고굴절)': 140000, '1.74 (특초)': 200000}, 'img': 'https://via.placeholder.com/300x200?text=ZEISS+ClearView', 'spec_design': 'Freeform', 'spec_material': 'Zeiss', 'spec_coat': 'Platinum', 'spec_uv': 'UVProtect', 'desc': '3배 더 넓은 선명한 시야.', 'tags': ['#초선명', '#자이스'], 'thin': 8, 'view': 9, 'coat': 8},
            {'id': 6, 'brand': '에실로', 'name': '트랜지션스 Gen8', 'price': 150000, 'price_table': {'1.50 (일반)': 150000, '1.60 (고굴절)': 220000}, 'img': 'https://via.placeholder.com/300x200?text=Transitions', 'spec_design': '변색', 'spec_material': 'Orma', 'spec_coat': 'Sapphire', 'spec_uv': 'UV400', 'desc': '실내 투명, 실외 선글라스 자동 변색.', 'tags': ['#변색렌즈', '#패션'], 'thin': 7, 'view': 8, 'coat': 8},
            {'id': 7, 'brand': '토카이', 'name': '루티나', 'price': 180000, 'price_table': {'1.60 (고굴절)': 180000, '1.76 (세계최초)': 400000}, 'img': 'https://via.placeholder.com/300x200?text=TOKAI+Lutina', 'spec_design': '비구면', 'spec_material': 'Lutina', 'spec_coat': 'ESC', 'spec_uv': 'HEV', 'desc': '루테인 보호, 망막 건강.', 'tags': ['#눈건강', '#망막보호'], 'thin': 9, 'view': 9, 'coat': 10},
            {'id': 8, 'brand': '자이스', 'name': '드라이브세이프', 'price': 250000, 'price_table': {'1.50 (일반)': 250000, '1.60 (고굴절)': 360000}, 'img': 'https://via.placeholder.com/300x200?text=ZEISS+DriveSafe', 'spec_design': 'Luminance', 'spec_material': 'Zeiss', 'spec_coat': 'DriveSafe', 'spec_uv': 'UVProtect', 'desc': '야간 운전 눈부심 감소.', 'tags': ['#야간운전', '#안전운전'], 'thin': 8, 'view': 10, 'coat': 9}
        ])
    else:
        return pd.DataFrame([
            {'id': 101, 'brand': '미광', 'name': '클리어 원데이', 'price': 32000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Clear', 'spec_mat': 'Hioxifilcon A', 'spec_water': '58%', 'spec_dk': '25', 'spec_bc': '8.7', 'desc': '가성비 최고의 데일리 렌즈.', 'tags': ['#가성비갑'], 'dry': 4, 'handle': 9, 'oxygen': 3},
            {'id': 102, 'brand': '쿠퍼비전', 'name': '클래리티 원데이', 'price': 45000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Clarity', 'spec_mat': 'Somofilcon A', 'spec_water': '56%', 'spec_dk': '86', 'spec_bc': '8.6', 'desc': '실리콘 하이드로겔 소재 가성비.', 'tags': ['#실리콘'], 'dry': 7, 'handle': 7, 'oxygen': 8},
            {'id': 103, 'brand': '인터로조', 'name': '오투오투 원데이', 'price': 45000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=O2O2', 'spec_mat': 'Silicone', 'spec_water': '45%', 'spec_dk': '130', 'spec_bc': '8.8', 'desc': '높은 산소전달률 국산 프리미엄.', 'tags': ['#국산'], 'dry': 7, 'handle': 8, 'oxygen': 9},
            {'id': 104, 'brand': '바슈롬', 'name': '울트라 원데이', 'price': 55000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Ultra', 'spec_mat': 'Kalifilcon A', 'spec_water': '55%', 'spec_dk': '134', 'spec_bc': '8.6', 'desc': '16시간 촉촉함.', 'tags': ['#장시간'], 'dry': 8, 'handle': 8, 'oxygen': 9},
            {'id': 105, 'brand': '아큐브', 'name': '오아시스 원데이', 'price': 63000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Oasys', 'spec_mat': 'Senofilcon A', 'spec_water': '38%', 'spec_dk': '121', 'spec_bc': '8.5/9.0', 'desc': '전 세계 베스트셀러.', 'tags': ['#베스트셀러'], 'dry': 8, 'handle': 8, 'oxygen': 9},
            {'id': 106, 'brand': '알콘', 'name': '데일리스 토탈원', 'price': 69000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Total1', 'spec_mat': 'Delefilcon A', 'spec_water': '33%~80%', 'spec_dk': '156', 'spec_bc': '8.5', 'desc': '워터렌즈, 건조감 해결.', 'tags': ['#강소라렌즈'], 'dry': 10, 'handle': 4, 'oxygen': 10},
            {'id': 107, 'brand': '알콘', 'name': '토탈원 난시', 'price': 79000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Total1+Toric', 'spec_mat': 'Delefilcon A', 'spec_water': '33%', 'spec_dk': '127', 'spec_bc': '8.6', 'desc': '토탈원의 촉촉함에 난시 교정.', 'tags': ['#난시교정'], 'dry': 10, 'handle': 4, 'oxygen': 9},
            {'id': 108, 'brand': '아큐브', 'name': '오아시스 난시', 'price': 74000, 'qty': '30p', 'img': 'https://via.placeholder.com/300x200?text=Oasys+Toric', 'spec_mat': 'Senofilcon A', 'spec_water': '38%', 'spec_dk': '121', 'spec_bc': '8.5', 'desc': '선명한 난시 교정.', 'tags': ['#난시교정'], 'dry': 8, 'handle': 8, 'oxygen': 9}
        ])

# [추천 데이터 - AI 상세 분석용 멘트(ai_summary) 추가]
def load_recommendation_data(mode, sph=0, cyl=0):
    if mode == 'glasses':
        idx_name, idx_price, thin_score = get_index_recommendation(sph, cyl)
        data = [
            {'id': 1, 'brand': '케미', 'name': '퍼펙트 UV', 'base_price': 30000, 'cat': 'general', 'tier': 0, 'view': 6, 'coat': 5, 'tags': ['#블루라이트차단', '#가성비'], 
             'ai_summary': '자외선 99.9% 차단과 블루라이트 부분 차단 기능이 들어간 <b>퍼펙트 UV</b> 기술이 적용된, 가성비 최고의 실속형 렌즈입니다.'},
            {'id': 2, 'brand': '니콘', 'name': 'BLUV Plus', 'base_price': 60000, 'cat': 'digital', 'tier': 1, 'view': 7, 'coat': 7, 'tags': ['#양면차단', '#디지털피로'],
             'ai_summary': '니콘만의 <b>이중 자외선 차단 설계</b>가 적용되어 앞뒷면 UV를 모두 막아주며, 디지털 눈 피로 완화 존이 설계되어 있습니다.'},
            {'id': 3, 'brand': '호야', 'name': '뉴럭스', 'base_price': 70000, 'cat': 'general', 'tier': 1, 'view': 8, 'coat': 9, 'tags': ['#흠집방지', '#선명함'],
             'ai_summary': '호야의 자랑인 <b>VG(Venus Guard) 코팅</b>이 적용되어 일반 렌즈 대비 스크래치에 5배 강하고 먼지가 덜 붙습니다.'},
            {'id': 4, 'brand': '케미', 'name': '양면비구면 D-Free', 'base_price': 80000, 'cat': 'distortions', 'tier': 1, 'view': 8, 'coat': 7, 'tags': ['#왜곡최소화', '#넓은시야'],
             'ai_summary': '렌즈의 앞면과 뒷면을 모두 평평하게 설계한 <b>양면 비구면(D-Free)</b> 기술로, 주변부 왜곡을 줄여 눈이 편안합니다.'},
            {'id': 5, 'brand': '자이스', 'name': '클리어뷰', 'base_price': 100000, 'cat': 'general', 'tier': 2, 'view': 9, 'coat': 8, 'tags': ['#초선명', '#얇은두께'],
             'ai_summary': '자이스의 <b>클리어뷰 프리폼 기술</b>로 렌즈 중심부뿐만 아니라 주변부까지 3배 더 넓은 선명한 시야를 제공합니다.'},
            {'id': 6, 'brand': '에실로', 'name': '트랜지션스 Gen8', 'base_price': 150000, 'cat': 'outdoor', 'tier': 2, 'view': 8, 'coat': 8, 'tags': ['#변색렌즈', '#선글라스'],
             'ai_summary': '전 세계 1위 <b>트랜지션스 Gen8</b> 기술로 실내에서는 투명하고 실외에서는 선글라스처럼 진하게, 빠르게 변색됩니다.'},
            {'id': 7, 'brand': '토카이', 'name': '루티나', 'base_price': 180000, 'cat': 'premium', 'tier': 3, 'view': 9, 'coat': 10, 'tags': ['#눈건강', '#망막보호'],
             'ai_summary': '산화 스트레스를 유발하는 파장을 차단하는 <b>루티나(Lutina)</b> 소재를 사용하여 눈 속 루테인을 보호하는 헬스케어 렌즈입니다.'},
            {'id': 8, 'brand': '자이스', 'name': '드라이브세이프', 'base_price': 250000, 'cat': 'drive', 'tier': 3, 'view': 10, 'coat': 9, 'tags': ['#야간운전', '#빛번짐차단'],
             'ai_summary': '<b>루미넌스 디자인</b> 기술로 야간에 커진 동공 크기를 반영해 빛 번짐을 줄이고 선명도를 극대화한 운전 전용 렌즈입니다.'}
        ]
        df = pd.DataFrame(data)
        df['final_price'] = df['base_price'] + idx_price
        df['index_info'] = idx_name
        df['thin_score'] = [min(10, thin_score + (1 if sph < -4.0 else 0)) for _ in range(len(df))]
        return df
    else:
        # 콘택트렌즈
        data = [
            {'id': 101, 'brand': '미광', 'name': '클리어 원데이', 'category': 'sphere', 'tier': 0, 'price': 32000, 'dry_score': 4, 'dkt': 25, 'handling': 9, 'oxygen': 3, 'tags': ['#가성비갑'],
             'ai_summary': '<b>Hioxifilcon A</b> 재질의 높은 함수율로 초기 착용감이 촉촉하며, 가격 부담 없이 매일 쓰기 좋은 가성비 제품입니다.'},
            {'id': 102, 'brand': '쿠퍼비전', 'name': '클래리티 원데이', 'category': 'sphere', 'tier': 1, 'price': 45000, 'dry_score': 7, 'dkt': 86, 'handling': 7, 'oxygen': 8, 'tags': ['#실리콘'],
             'ai_summary': '눈이 숨 쉴 수 있는 <b>실리콘 하이드로겔</b> 소재를 합리적인 가격에 제공하여, 장시간 착용에도 눈 충혈이 적습니다.'},
            {'id': 106, 'brand': '알콘', 'name': '데일리스 토탈원', 'category': 'sphere', 'tier': 3, 'price': 69000, 'dry_score': 10, 'dkt': 156, 'handling': 4, 'oxygen': 10, 'tags': ['#건조감종결'],
             'ai_summary': '표면 함수율이 80%가 넘는 <b>워터 그라디언트</b> 기술로 눈꺼풀 마찰을 최소화하여 렌즈를 안 낀 듯한 느낌을 줍니다.'},
            {'id': 105, 'brand': '아큐브', 'name': '오아시스 원데이', 'category': 'sphere', 'tier': 2, 'price': 63000, 'dry_score': 8, 'dkt': 121, 'handling': 8, 'oxygen': 9, 'tags': ['#베스트셀러'],
             'ai_summary': '렌즈 재질 내에 눈물 성분과 유사한 습윤 인자를 함유한 <b>하이드라럭스</b> 기술로 디지털 기기 사용 시 건조감을 줄여줍니다.'},
            {'id': 103, 'brand': '인터로조', 'name': '오투오투 원데이', 'category': 'sphere', 'tier': 1, 'price': 45000, 'dry_score': 7, 'dkt': 130, 'handling': 8, 'oxygen': 9, 'tags': ['#국산'],
             'ai_summary': '130 Dk/t의 <b>높은 산소전달률</b>을 자랑하는 국산 프리미엄 렌즈로, 눈 건강과 가성비를 모두 잡았습니다.'},
            {'id': 104, 'brand': '바슈롬', 'name': '울트라 원데이', 'category': 'sphere', 'tier': 2, 'price': 55000, 'dry_score': 8, 'dkt': 134, 'handling': 8, 'oxygen': 9, 'tags': ['#촉촉함'],
             'ai_summary': '<b>모이스처 씰</b> 기술로 16시간 착용 후에도 렌즈 수분의 96%를 유지하여 늦은 저녁까지 편안합니다.'},
            {'id': 107, 'brand': '알콘', 'name': '토탈원 난시', 'category': 'toric', 'tier': 3, 'price': 79000, 'dry_score': 10, 'dkt': 127, 'handling': 4, 'oxygen': 9, 'tags': ['#난시교정'],
             'ai_summary': '토탈원 특유의 워터 그라디언트 재질에 <b>프리시전 밸런스 8/4</b> 디자인을 더해, 건조감 없이 선명한 난시 교정을 제공합니다.'},
            {'id': 108, 'brand': '아큐브', 'name': '오아시스 난시', 'category': 'toric', 'tier': 2, 'price': 74000, 'dry_score': 8, 'dkt': 121, 'handling': 8, 'oxygen': 9, 'tags': ['#축안정'],
             'ai_summary': '눈의 깜빡임을 이용하여 렌즈 축을 안정시키는 <b>ASD 기술</b>로, 눕거나 운동할 때도 흔들림 없는 시야를 유지합니다.'}
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

# 설문 문항 키
all_q_keys = ['env_1', 'env_2', 'env_3', 'env_4', 'env_5', 'sen_1', 'sen_2', 'sen_3', 'sen_4', 'sen_5', 'val_1', 'val_2', 'val_3', 'val_4', 'val_5', 'exp_1', 'exp_2', 'exp_3', 'exp_4', 'exp_5']
q_labels = {
    'env_1': 'Q1.하루 8시간 이상 디지털 기기 사용', 'env_2': 'Q2.건조한 실내 환경 상주', 'env_3': 'Q3.야외 활동 및 자외선 노출', 'env_4': 'Q4.미세먼지/바람 등 거친 환경 노출', 'env_5': 'Q5.야간 운전 빈도',
    'sen_1': 'Q6.오후 시간대 눈 뻑뻑함/충혈 발생', 'sen_2': 'Q7.렌즈 착용 시 이물감 예민하게 느낌', 'sen_3': 'Q8.눈이 쉽게 붓거나 피로감 느낌', 'sen_4': 'Q9.눈 시림 및 따가움 자주 느낌', 'sen_5': 'Q10.난시로 인한 글자 번짐/흐림 심함',
    'val_1': 'Q11.눈을 위한 고가 제품 투자 의향 있음', 'val_2': 'Q12.최신 기술 및 신제품 선호 성향', 'val_3': 'Q13.브랜드 인지도 및 명성 중요시', 'val_4': 'Q14.할인 행사 및 가성비 중요시', 'val_5': 'Q15.기존 사용 제품 고수 성향 (보수적)',
    'exp_1': 'Q16.렌즈 착용 및 제거 능숙도 높음', 'exp_2': 'Q17.렌즈 세척 및 관리 귀찮지 않음', 'exp_3': 'Q18.본인의 정확한 도수 인지하고 있음', 'exp_4': 'Q19.과거 렌즈 착용 성공 경험 있음', 'exp_5': 'Q20.전문가 도움 없이 스스로 제품 선택 가능'
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
if 'source_page' not in st.session_state: st.session_state['source_page'] = None

def go_to(page): 
    st.session_state['page'] = page
    st.session_state['dict_selected_id'] = None
    st.session_state['source_page'] = None

# ==============================================================================
# 4. 안경사 전용 뷰
# ==============================================================================
if st.session_state['page'] == 'optician_view':
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
            price_score = max(1, 10 - (r['base_price'] / 45000))
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            cand_g.at[i, 'total_score'] = total_score
        ranks = cand_g.sort_values('total_score', ascending=False).head(3)
        for rk, (idx, row) in enumerate(ranks.iterrows(), 1):
            st.markdown(f"<div style='background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;'><div style='font-weight:bold; font-size:16px;'>{rk}위. {row['name']}</div><div style='color:#666; font-size:13px;'>{row['brand']} | {format(int(row['final_price']),',')}원 (권장소비자가)</div></div>", unsafe_allow_html=True)

    with tab2:
        df_c = load_recommendation_data('contacts')
        cand_c = df_c.copy()
        for i, r in cand_c.iterrows():
            norm_spec = r['dry_score']; price_score = max(2, 10 - (r['price'] / 10000))
            if type_t == "T": total_score = (norm_spec * 0.8) + (price_score * 0.2)
            else: total_score = (norm_spec * 0.2) + (price_score * 0.8)
            cand_c.at[i, 'total_score'] = total_score
        ranks_c = cand_c.sort_values('total_score', ascending=False).head(3)
        for rk, (idx, row) in enumerate(ranks_c.iterrows(), 1):
            st.markdown(f"<div style='background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:10px;'><div style='font-weight:bold; font-size:16px;'>{rk}위. {row['name']}</div><div style='color:#666; font-size:13px;'>{row['brand']} | {format(row['price'],',')}원 (권장소비자가)</div></div>", unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-weight:bold; margin-bottom:10px; color:#2563EB;'>📊 4대 핵심 지표 분석</div>", unsafe_allow_html=True)
    metrics = [("디지털/실내 환경", data['env']), ("각막 민감도", data['sen']), ("가격/스펙 성향", data['val']), ("렌즈 관리 숙련도", data['pro'])]
    for label, val in metrics:
        st.markdown(f"<div class='metric-box'><div class='metric-header'><span>{label}</span><span style='color:#2563EB;'>{val}점</span></div><div style='background:#F1F5F9; height:8px; border-radius:4px; overflow:hidden;'><div style='background:#2563EB; height:100%; width:{val*10}%;'></div></div></div>", unsafe_allow_html=True)
    
    st.markdown("""<div style="background:#F1F5F9; padding:15px; border-radius:10px; margin-top:15px; font-size:12px; color:#64748B; line-height:1.6;"><div style="font-weight:bold; margin-bottom:5px;">💡 지표 해석 가이드</div>• <b>디지털/실내:</b> 높을수록 디지털 기기 사용량 많음<br>• <b>각막 민감도:</b> 높을수록 건조감에 예민함<br>• <b>가격/스펙:</b> 높을수록 성능(T) 중시, 낮을수록 가성비(F)<br>• <b>관리 숙련도:</b> 높을수록 렌즈 관리에 능숙함</div>""", unsafe_allow_html=True)

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
    st.markdown("<div id='top_anchor'></div>", unsafe_allow_html=True)
    
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
            
            p_rows = "".join([f"<tr><td>{k}</td><td>{format(v,',')}원 (권장소비자가)</td></tr>" for k, v in sel['price_table'].items()])
            st.markdown(f"<table class='price-table'>{p_rows}</table>", unsafe_allow_html=True)
            st.markdown(f"<div class='detail-desc-box'><b>💡 특징:</b><br>{sel['desc']}</div>", unsafe_allow_html=True)
            
            st.plotly_chart(make_radar_chart(sel['name'], [sel['thin'], sel['view'], sel['coat'], 9, 9], ['두께', '시야', '코팅', '가격', '내구']), use_container_width=True)
            
            if st.session_state.get('source_page') == 'result':
                if st.button("🔙 분석 결과로 돌아가기", use_container_width=True): st.session_state['page'] = 'result'; st.rerun()
            else:
                if st.button("목록으로 돌아가기", key="back_g", use_container_width=True): st.session_state['dict_selected_id'] = None; st.rerun()
        else:
            for i, row in df.iterrows():
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    with c1: st.markdown(f"<div class='dict-list-item'><div style='font-size:12px; color:#666; font-weight:bold;'>{row['brand']}</div><div style='font-size:16px; font-weight:800; color:#333;'>{row['name']}</div><div style='font-size:12px; color:#2563EB; font-weight:bold; margin-top:5px;'>{format(row['price'],',')}원~ (권장소비자가)</div></div>", unsafe_allow_html=True)
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
            st.markdown(f"<div class='detail-header'><div class='detail-brand'>{sel['brand']}</div><div class='detail-name'>{sel['name']}</div><div class='detail-price-main'>{format(sel['price'],',')}원 ({sel['qty']}) (권장소비자가)</div></div>", unsafe_allow_html=True)
            st.markdown(f"<table class='spec-table'><tr><th>재질</th><td>{sel['spec_mat']}</td></tr><tr><th>함수율</th><td>{sel['spec_water']}</td></tr><tr><th>산소투과율</th><td>{sel['spec_dk']}</td></tr><tr><th>BC</th><td>{sel['spec_bc']}</td></tr></table>", unsafe_allow_html=True)
            st.markdown(f"<div class='detail-desc-box'><b>💡 특징:</b><br>{sel['desc']}</div>", unsafe_allow_html=True)
            
            # [Fix] KeyError 방지
            dry = sel.get('dry', 5); handle = sel.get('handle', 5); oxygen = sel.get('oxygen', 5)
            st.plotly_chart(make_radar_chart(sel['name'], [dry, handle, oxygen, 9, 9], ['건조', '핸들링', '산소', '가성비', '착용']), use_container_width=True)
            
            if st.session_state.get('source_page') == 'result':
                if st.button("🔙 분석 결과로 돌아가기", use_container_width=True): st.session_state['page'] = 'result'; st.rerun()
            else:
                if st.button("목록으로 돌아가기", key="back_c", use_container_width=True): st.session_state['dict_selected_id'] = None; st.rerun()
        else:
            for i, row in df.iterrows():
                with st.container():
                    c1, c2 = st.columns([3, 1])
                    with c1: st.markdown(f"<div class='dict-list-item'><div style='font-size:12px; color:#666; font-weight:bold;'>{row['brand']}</div><div style='font-size:16px; font-weight:800; color:#333;'>{row['name']}</div><div style='font-size:12px; color:#2563EB; font-weight:bold; margin-top:5px;'>{format(row['price'],',')}원 (권장소비자가)</div></div>", unsafe_allow_html=True)
                    with c2:
                        if st.button("상세보기", key=f"btn_c_{row['id']}", use_container_width=True):
                            st.session_state['dict_selected_id'] = row['id']; st.session_state['dict_cat'] = 'contacts'; st.rerun()

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    if st.button("🏠 홈으로 가기", use_container_width=True): go_to('home'); st.rerun()
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
    # (점수 계산 로직)
    score_i = sum([ans[f'env_{i}'] for i in range(1,6)]); type_i = "I" if score_i >= 15 else "E"
    score_s = sum([ans[f'sen_{i}'] for i in range(1,6)]); type_s = "S" if score_s >= 15 else "N"
    score_t = sum([ans[f'val_{i}'] for i in range(1,6)]); type_t = "T" if score_t >= 15 else "F"
    score_p = sum([ans[f'exp_{i}'] for i in range(1,6)]); type_p = "P" if score_p >= 15 else "J"
    mbti_res = f"{type_i}{type_s}{type_t}{type_p}"
    
    stat_env = round(score_i / 2.5, 1); stat_sen = round(score_s / 2.5, 1)
    stat_val = round(score_t / 2.5, 1) if type_t == 'T' else round(score_t / 2.5, 1)
    stat_pro = round(score_p / 2.5, 1)

    personas = {"ISTP": {"title": "🔎 팩트체크 장인", "desc": "숫자와 스펙을 믿는 당신!", "strategy": "현존 최고 스펙 추천"}, "ENFP": {"title": "🦄 자유로운 영혼", "desc": "복잡한 관리는 딱 질색!", "strategy": "내구성 좋은 원데이 추천"}, "ISFJ": {"title": "🛡️ 눈 건강 지킴이", "desc": "돌다리도 두드려보고 건너는 신중파! <br>새로운 도전보다는 <b>검증된 브랜드와 안전한 소재</b>를 선호합니다.", "strategy": "안과의사 추천 베스트셀러"}, "ENTJ": {"title": "😎 효율 끝판왕", "desc": "가격 대비 성능비(ROI)가 확실해야 지갑을 여는 당신! <br><b>성능과 가격의 황금 밸런스</b>를 중요하게 생각합니다.", "strategy": "거품 빠진 실속형 제품"}, "ESTP": {"title": "⚡ 행동대장", "desc": "야외 활동을 즐기는 인싸! 자외선 차단이 필수입니다.", "strategy": "내구성 좋고 UV 차단 제품"}, "INFJ": {"title": "🔮 섬세한 예언자", "desc": "남들은 모르는 미세한 불편함까지 느끼는 섬세한 눈.", "strategy": "자극이 적은 저자극 소재"}, "INTP": {"title": "🧪 논리적인 분석가", "desc": "원리를 이해해야 직성이 풀립니다. 기술력이 중요해요.", "strategy": "최신 광학 기술 적용 렌즈"}, "ESFJ": {"title": "🤝 평화주의자", "desc": "주변 평판과 추천을 중요하게 생각합니다.", "strategy": "재구매율 1위 제품"}} 
    persona = personas.get(mbti_res, {"title": "⚖️ 밸런스형 스마트 컨슈머", "desc": "합리적인 선택을 하는 유연한 타입", "strategy": "올라운드 제품 추천"})

    st.markdown(f"""<div class="result-header"><div class="mbti-hero">{mbti_res}</div><div style="font-size: 26px; font-weight: 800; margin-bottom: 15px;">{persona['title']}</div><div class="persona-desc"><div style="margin-bottom:8px;"><b>🧐 분석:</b> {persona['desc']}</div><div><b>💡 공략법:</b> {persona['strategy']}</div></div></div>""", unsafe_allow_html=True)

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
            
            reasons = []
            life_reasons = []
            if ans['env_1'] >= 4: life_reasons.append("디지털 과몰입")
            if ans['env_5'] >= 4: life_reasons.append("잦은 야간 운전")
            if ans['env_3'] >= 4: life_reasons.append("활발한 야외 활동")
            
            spec_reasons = []
            if 'digital' in row['cat']: spec_reasons.append("조절력 완화 어시스트")
            if 'drive' in row['cat']: spec_reasons.append("눈부심 차단 드라이브 코팅")
            if abs(vision['cyl']) >= 1.0 and ('distortions' in row['cat'] or 'premium' in row['cat']): spec_reasons.append("난시 왜곡 최소화 설계")
            if row['tier'] == 3: spec_reasons.append("브랜드 최상위 하이엔드")
            
            val_reasons = []
            if type_t == "T": val_reasons.append("<b>성능 최우선</b> 성향에 맞춰 최고 스펙 제품을 선정")
            elif type_t == "F": 
                if row['base_price'] >= 100000: val_reasons.append("가성비를 선호하시지만, <b>고객님의 시력 특성상 교정력을 위해</b> 불가피하게 성능 위주로 선정")
                else: val_reasons.append("<b>가성비</b>를 최우선으로 고려하여 거품 없는 실속형 제품을 선정")
            else: val_reasons.append("가격과 성능의 <b>최적 밸런스</b>를 고려")

            c1, c2 = st.columns([1.6, 1])
            with c1:
                tags_html = "".join([f"<span class='feature-tag'>{t}</span>" for t in row['tags']])
                st.markdown(f"""
                <div class="prod-card">
                    <div class="prod-rank">{rk}위</div>
                    <span class="match-point">{match_percent}% 일치</span>
                    <div style="font-size:20px; font-weight:800; margin-top:20px; margin-bottom:5px; color:#111;">
                        {row['name']}
                    </div>
                    <div style="font-size:14px; color:#666; margin-bottom:8px;">{row['brand']} | 굴절률 {row['index_info']}</div>
                    <div class="tag-box">{tags_html}</div>
                    <div style="font-size:18px; font-weight:800; color:#2563EB;">{format(int(row['final_price']),',')}원 <span style="font-size:12px; color:#999; font-weight:normal;">(권장소비자가)</span></div>
                    <div class="why-box">
                        <div class="why-title">🧐 AI 상세 분석</div>
                        <span class="why-cat">🏢 라이프스타일 매칭</span>
                        <div class="why-desc">{' / '.join(life_reasons) if life_reasons else '일상적인 생활 패턴'}에 적합합니다.</div>
                        <span class="why-cat">👁️ 기술적 해결책</span>
                        <div class="why-desc">{row['ai_summary']}</div>
                        <span class="why-cat">⚖️ 선정 기준</span>
                        <div class="why-desc">{val_reasons[0]}했습니다.</div>
                    </div>
                </div>""", unsafe_allow_html=True)
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
            
            reasons = []
            life_reasons = []
            if ans['sen_1'] >= 4: life_reasons.append("오후 건조감 심함")
            elif ans['sen_1'] == 3: life_reasons.append("간헐적 눈 마름")
            if type_i == "I": life_reasons.append("건조한 실내 환경")
            
            spec_reasons = []
            if row['dkt'] >= 130: spec_reasons.append(f"<b>압도적인 산소투과율(Dk/t {row['dkt']})</b>")
            elif row['dkt'] >= 100: spec_reasons.append(f"우수한 산소 전달량(Dk/t {row['dkt']})")
            if row['dry_score'] >= 9: spec_reasons.append("최상급 습윤성 재질")
            
            val_reasons = []
            if type_t == "T": val_reasons.append("눈 건강을 위해 <b>최고 스펙</b> 제품을 선정")
            elif type_t == "F":
                if row['price'] >= 60000: val_reasons.append("가성비를 선호하시지만, <b>장시간 착용과 건조감 해결을 위해</b> 프리미엄 제품을 권장")
                else: val_reasons.append("매일 착용해도 부담 없는 <b>합리적 가격</b>을 우선")
            else: val_reasons.append("가격과 성능의 <b>최적 밸런스</b>를 고려")

            c1, c2 = st.columns([1.6, 1])
            with c1:
                tags_html = "".join([f"<span class='feature-tag'>{t}</span>" for t in row['tags']])
                st.markdown(f"""
                <div class="prod-card">
                    <div class="prod-rank">{rk}위</div>
                    <span class="match-point">{match_percent}% 일치</span>
                    <div style="font-size:20px; font-weight:800; margin-top:20px; margin-bottom:5px; color:#111;">
                        {row['name']}
                    </div>
                    <div style="font-size:14px; color:#666; margin-bottom:8px;">{row['brand']}</div>
                    <div class="tag-box">{tags_html}</div>
                    <div style="font-size:18px; font-weight:800; color:#2563EB;">{format(row['price'],',')}원 <span style="font-size:12px; color:#999; font-weight:normal;">(권장소비자가)</span></div>
                    <div class="why-box">
                        <div class="why-title">🧐 AI 상세 분석</div>
                        <span class="why-cat">🏢 라이프스타일 매칭</span>
                        <div class="why-desc">{' / '.join(life_reasons) if life_reasons else '데일리 케어'}에 집중했습니다.</div>
                        <span class="why-cat">👁️ 기술적 해결책</span>
                        <div class="why-desc">{row['ai_summary']}</div>
                        <span class="why-cat">⚖️ 선정 기준</span>
                        <div class="why-desc">{val_reasons[0]}했습니다.</div>
                    </div>
                </div>""", unsafe_allow_html=True)
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
    
    st.markdown(f"""<div class="qr-container"><img src="data:image/png;base64,{img_str}" width="160"><div class="capture-guide">📸 안경사님께 이 화면을 보여주세요</div><div style="font-size:12px; color:#888; margin-top:5px; margin-bottom:20px;">(또는 QR코드를 스캔하면 상세 분석 화면으로 이동합니다)</div><div style="border-top:1px solid #eee; padding-top:20px; text-align:left;"><div style="font-weight:bold; margin-bottom:12px; font-size:14px; color:#2563EB;">📊 고객 성향 정량 분석 (10점 만점)</div></div></div>""", unsafe_allow_html=True)
    
    metrics = [("디지털/실내 환경", stat_env, "높을수록 디지털 사용 많음"), 
               ("각막 민감도", stat_sen, "높을수록 예민함"), 
               ("가격/스펙 성향", data['val'], "높을수록 성능(T), 낮을수록 가성비(F)"), 
               ("렌즈 관리 숙련도", data['pro'], "높을수록 숙련자")]
    
    for label, val, desc in metrics:
        st.markdown(f"<div class='metric-box'><div class='metric-header'><span>{label}</span><span style='color:#2563EB;'>{val}점</span></div><div style='background:#F1F5F9; height:8px; border-radius:4px; overflow:hidden;'><div style='background:#2563EB; height:100%; width:{val*10}%;'></div></div></div>", unsafe_allow_html=True)
    
    # [NEW] 해석 가이드 복구
    st.markdown("""
    <div style="background:#F1F5F9; padding:15px; border-radius:10px; margin-top:15px; font-size:12px; color:#64748B; line-height:1.6;">
        <div style="font-weight:bold; margin-bottom:5px;">💡 지표 해석 가이드</div>
        • <b>디지털/실내:</b> 점수가 높을수록 디지털 기기 사용 시간이 길고 실내 활동이 많습니다.<br>
        • <b>각막 민감도:</b> 점수가 높을수록 건조감과 이물감을 예민하게 느낍니다.<br>
        • <b>가격/스펙:</b> 점수가 높을수록 고성능(T)을 선호하며, 낮을수록 가성비(F)를 중시합니다.<br>
        • <b>관리 숙련도:</b> 점수가 높을수록 렌즈 착용 및 관리에 능숙합니다.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='margin-bottom:30px;'></div>", unsafe_allow_html=True)
    
    # [NEW] 안경원 찾기 버튼 추가 (결과 화면 하단)
    if st.button("📍 내 주변 안경원 찾기", use_container_width=True):
        st.session_state['page'] = 'map_view'
        st.rerun()
        
    if st.button("🏠 처음으로 돌아가기", use_container_width=True): go_to('home'); st.rerun()
    
    # [핵심] 스크롤 강제 이동 (맨 마지막에 배치)
    components.html("""<script>window.parent.document.getElementById('top_anchor').scrollIntoView();</script>""", height=0)
