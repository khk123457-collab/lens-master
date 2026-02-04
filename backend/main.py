from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import os
from . import logic # 우리가 만든 뇌

app = FastAPI()

# 1. 서버가 켜질 때 엑셀 파일 한번 읽어두기
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_path, 'data', 'lens_db_v1.xlsx')
df = pd.read_excel(file_path)

# 2. 주문서 양식 만들기 (앱에서 보낼 데이터)
class UserRequest(BaseModel):
    sph: float
    cyl: float
    dry_sensitivity: int
    is_beginner: bool
    price_pref: str
    digital_time: int

@app.get("/")
def read_root():
    return {"message": "렌즈마스터 AI 서버가 정상 작동 중입니다!"}

@app.post("/recommend")
def recommend_lens(user: UserRequest):
    """
    앱에서 고객 정보를 보내면 -> 추천 렌즈 리스트를 돌려주는 창구
    """
    user_dict = user.dict() # 받은 정보를 딕셔너리로 변환
    results = []

    # 뇌(logic)를 돌려서 추천 제품 찾기
    for index, product in df.iterrows():
        is_possible, msg = logic.check_availability(user.sph, user.cyl, product)
        if is_possible:
            score = logic.calculate_score(user_dict, product)
            results.append({
                "brand": product['brand'],
                "name": product['name'],
                "score": score,
                "price": product['price']
            })
    
    # 점수 높은 순 정렬
    sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    # MBTI 분석 결과도 같이 보내주기
    mbti_result = logic.get_eye_mbti(user_dict)
    
    return {
        "mbti": mbti_result,
        "top_3": sorted_results[:3]
    }