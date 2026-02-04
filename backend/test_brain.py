import pandas as pd
import os
import logic # 방금 만든 뇌를 불러옵니다!

# 1. 엑셀 데이터 불러오기 (아까 했던 거)
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_path, 'data', 'lens_db_v1.xlsx')
df = pd.read_excel(file_path)

# 2. 가상의 고객 설정 (김철수님)
user = {
    'sph': -5.00,       # 근시
    'cyl': -1.25,       # 난시
    'dry_sensitivity': 5, # 건조감 예민도 (매우 예민)
    'is_beginner': False, # 렌즈 낄 줄 암
    'price_pref': 'performance', # 성능 우선
    'digital_time': 8    # 하루 8시간 컴퓨터 봄
}

print(f"👨‍⚕️ 고객 진단 시작: 도수 {user['sph']} {user['cyl']}, 건조감 {user['dry_sensitivity']}점")
print("-" * 60)

# 3. 모든 렌즈 하나씩 검사하기
recommendations = []

# 엑셀에 있는 렌즈를 한 줄씩 꺼내서 product 변수에 담음
for index, product in df.iterrows():
    
    # A. 도수가 맞는지 체크 (Availability Check)
    is_possible, message = logic.check_availability(user['sph'], user['cyl'], product)
    
    if not is_possible:
        # 도수가 안 맞으면 건너뜀 (출력 생략 가능하지만 확인용으로 출력)
        print(f"❌ [탈락] {product['name']}: {message}")
        continue
        
    # B. 점수 매기기 (Scoring)
    final_score = logic.calculate_score(user, product)
    
    # 추천 리스트에 추가
    recommendations.append({
        'name': product['name'],
        'score': final_score,
        'price': product['price']
    })

# 4. 점수 높은 순서대로 1, 2, 3등 뽑기
sorted_recs = sorted(recommendations, key=lambda x: x['score'], reverse=True)

print("-" * 60)
print(f"🎯 진단 결과 (MBTI 유형: {logic.get_eye_mbti(user)})")
print("-" * 60)
for i, rec in enumerate(sorted_recs[:3]): # 상위 3개만
    print(f"{i+1}위: {rec['name']} (점수: {rec['score']}점)")