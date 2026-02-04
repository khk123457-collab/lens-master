import streamlit as st
import pandas as pd
import os
import sys
import plotly.graph_objects as go

# 백엔드 연결
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend import logic 

st.set_page_config(page_title="Lens Master", page_icon="👁️", layout="wide")

# --- [UI 디자인] 헤더 영역 ---
st.title("👁️ LENS MASTER")
st.markdown("""
<style>
    .big-font { font-size:20px !important; color: #555; }
    .highlight { color: #0066cc; font-weight: bold; }
    .warning-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #00A0E9; }
</style>
""", unsafe_allow_html=True)
st.markdown('<p class="big-font">Clinical Eye-MBTI Analysis System</p>', unsafe_allow_html=True)
st.divider()

# --- [사이드바] 문진표 ---
with st.sidebar:
    st.header("📝 Vision Profile")
    
    # 도수 모름 체크박스
    dont_know = st.checkbox("도수를 몰라요 (상담 전용 모드)")
    
    if dont_know:
        st.info("💡 **시나리오 분석 모드**\n\n고객님의 생활 패턴을 바탕으로 **[근시일 경우]**와 **[난시일 경우]** 최적의 제품을 각각 추천합니다.")
        sph, cyl = 0.0, 0.0 # 로직 통과용 가상 도수
    else:
        col1, col2 = st.columns(2)
        sph = col1.number_input("SPH (근시)", value=-5.00, step=0.25)
        cyl = col2.number_input("CYL (난시)", value=-1.25, step=0.25)
    
    st.subheader("Condition & Lifestyle")
    dry_sensitivity = st.slider("건조 민감도 (Corneal Sensitivity)", 1, 5, 3, help="1: 둔감함 ~ 5: 매우 예민함")
    digital_time = st.slider("디지털 부하 (Digital Load)", 0, 16, 6, help="하루 PC/스마트폰 사용 시간")
    
    st.subheader("Preferences")
    is_beginner = st.checkbox("렌즈 착용 초심자 (Beginner)")
    price_pref = st.radio("우선순위", ["performance (성능 중심)", "value (가성비 중심)"])
    
    analyze_btn = st.button("🔍 정밀 분석 시작 (Analyze)", type="primary")

# --- [함수] 레이더 차트 (수정됨: 완벽한 오각형 닫기) ---
def make_radar_chart(product_name, scores):
    categories = ['건조감 방어', '핸들링', '산소투과율', '가격경쟁력', '적합도']
    
    # [핵심 수정] 데이터를 닫아주기 위해 첫 번째 값을 맨 뒤에 추가 (A-B-C-D-E-A 연결)
    scores_closed = scores + [scores[0]]
    categories_closed = categories + [categories[0]]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores_closed,
        theta=categories_closed,
        fill='toself',
        name=product_name,
        line=dict(color='#00A0E9', width=2),
        fillcolor='rgba(0, 160, 233, 0.15)' # 색상 약간 진하게 수정
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True, 
                range=[0, 10], 
                gridcolor='#eee', 
                linecolor='#eee',
                tickfont=dict(size=10)
            )
        ),
        showlegend=False,
        margin=dict(t=30, b=30, l=40, r=40),
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    return fig

# --- [함수] 결과 카드 보여주기 (재사용) ---
def show_recommendation_card(title, item, mbti_code):
    prod = item['data']
    st.markdown(f"#### {title}")
    st.markdown(f"### 🏆 {prod['name']}")
    st.caption(f"Brand: {prod['brand']} | Price: {format(prod['price'], ',')}원")
    
    # 주요 스펙 표시
    c1, c2 = st.columns(2)
    c1.metric("적합도", f"{item['final_score']}점")
    c2.metric("건조감 방어", f"{prod['dry']}/10")
    
    # 차트
    fig = make_radar_chart(prod['name'], item['chart_scores'])
    st.plotly_chart(fig, use_container_width=True)
    
    # 추천 멘트
    st.info(f"**추천 포인트:**\n{mbti_code} 성향인 고객님께 최적화된 재질입니다.")

# --- [메인] 분석 로직 ---
if analyze_btn:
    base_path = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_path, 'data', 'lens_db_v1.xlsx')
    
    try:
        df = pd.read_excel(file_path)
        
        user_profile = {
            'sph': sph, 'cyl': cyl,
            'dry_sensitivity': dry_sensitivity,
            'is_beginner': is_beginner,
            'price_pref': price_pref.split()[0],
            'digital_time': digital_time
        }
        
        # 1. 모든 제품 점수 계산
        results_all = []
        for index, product in df.iterrows():
            # 도수 모름 모드일 땐 가용성 체크 패스
            is_possible = True if dont_know else logic.check_availability(sph, cyl, product)[0]
            
            if is_possible:
                score = logic.calculate_score(user_profile, product)
                # 점수 환산
                s_dry = product['dry'] 
                s_handling = product['handling']
                s_dkt = min(product['dkt'] / 16.0, 10)
                s_price = max(0, (80000 - product['price']) / 8000 * 1.5)
                s_price = min(s_price, 10)
                s_fit = min(score / 20.0, 10)

                results_all.append({
                    "data": product,
                    "final_score": score,
                    "chart_scores": [s_dry, s_handling, s_dkt, s_price, s_fit]
                })

        mbti = logic.get_eye_mbti(user_profile)
        st.success(f"분석 완료! 고객님의 생활 패턴 유형은 **[{mbti}]** 입니다.")

        # --- [분기] 도수 모름 vs 도수 앎 ---
        if dont_know:
            st.markdown("""
            <div class="warning-box">
                <b>📢 시나리오별 추천 결과</b><br>
                고객님의 도수를 모르기 때문에, <b>근시일 경우</b>와 <b>난시일 경우</b>를 나누어 추천해 드립니다.<br>
                정확한 도수는 검안 후 결정됩니다.
            </div>
            <br>
            """, unsafe_allow_html=True)
            
            # 리스트 분리
            myopia_list = [r for r in results_all if 'toric' not in str(r['data']['category']).lower()]
            toric_list = [r for r in results_all if 'toric' in str(r['data']['category']).lower()]
            
            myopia_list.sort(key=lambda x: x['final_score'], reverse=True)
            toric_list.sort(key=lambda x: x['final_score'], reverse=True)
            
            col_myopia, col_toric = st.columns(2)
            
            with col_myopia:
                st.markdown("### 🅰️ 근시만 있다면")
                if myopia_list:
                    show_recommendation_card("Best for Myopia", myopia_list[0], mbti)
                else:
                    st.error("추천 제품 없음")
                    
            with col_toric:
                st.markdown("### 🅱️ 난시도 있다면")
                if toric_list:
                    show_recommendation_card("Best for Astigmatism", toric_list[0], mbti)
                else:
                    st.error("추천 제품 없음")
                    
        else:
            # 기존 로직 (도수 알 때)
            sorted_recs = sorted(results_all, key=lambda x: x['final_score'], reverse=True)
            
            if sorted_recs:
                top_pick = sorted_recs[0]
                prod = top_pick['data']
                
                c1, c2 = st.columns([1, 1.5])
                with c1:
                    st.markdown(f"### 🏆 BEST RECOMMENDATION")
                    st.markdown(f"## {prod['name']}")
                    st.caption(f"Brand: {prod['brand']} | Price: {format(prod['price'], ',')}원")
                    st.metric("종합 적합도", f"{top_pick['final_score']} pts")
                    st.info(f"**추천 사유:**\n* 건조감 방어: {prod['dry']}/10\n* [{mbti}] 최적화")
                with c2:
                    fig = make_radar_chart(prod['name'], top_pick['chart_scores'])
                    st.plotly_chart(fig, use_container_width=True)
                
                st.divider()
                st.markdown("#### 📋 Top 3 Candidates Comparison")
                comp_data = []
                for i, item in enumerate(sorted_recs[:3]):
                    p = item['data']
                    comp_data.append({
                        "순위": f"{i+1}위",
                        "제품명": p['name'],
                        "점수": f"{item['final_score']}점",
                        "가격": f"{format(p['price'], ',')}원",
                        "구분": p['category']
                    })
                st.dataframe(pd.DataFrame(comp_data).set_index("순위"))
            else:
                st.error("조건에 맞는 렌즈가 없습니다.")

    except Exception as e:
        st.error(f"오류 발생: {e}")