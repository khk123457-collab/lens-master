import pandas as pd

def check_availability(user_sph, user_cyl, product):
    """
    [기능 1] 재고/범위 체크 (Availability Check)
    사용자의 도수가 해당 제품의 생산 범위(Range) 안에 있는지 검사
    """
    # 1. 근시 도수(SPH) 체크
    # 엑셀의 sph_min ~ sph_max 사이에 내 도수가 있어야 함
    if not (product['sph_min'] <= user_sph <= product['sph_max']):
        return False, "도수 범위 초과"

    # 2. 난시 도수(CYL) 체크
    if user_cyl < 0: # 난시가 있는 사용자라면
        # 엑셀에 적힌 난시 도수 목록을 가져옴 (예: "-0.75,-1.25,-1.75")
        cyl_data = str(product['cyl_list'])
        
        # 난시용 제품이 아니면(비어있으면) 탈락
        if pd.isna(product['cyl_list']) or cyl_data.strip() == '':
            return False, "난시 미지원 제품"
            
        # 텍스트로 된 목록을 숫자로 쪼개서 리스트로 만듦
        available_cyls = [float(c) for c in cyl_data.split(',')]
        
        # 내 난시 도수가 목록에 없으면 탈락
        if user_cyl not in available_cyls:
            return False, "해당 난시 도수 미생산"

    return True, "착용 가능"

def calculate_score(user_profile, product):
    """
    [기능 2] Vision MBTI 점수 계산기
    사용자 성향(건조감, 핸들링 등)과 제품 스펙을 매칭하여 점수 산출
    """
    score = 70 # 기본 점수 70점부터 시작

    # 1. 건조감 가중치 계산 (사용자가 예민할수록 건조감 점수 비중 UP)
    # dry_sensitivity는 1~5점
    dry_weight = user_profile['dry_sensitivity'] * 2.0 
    score += product['dry'] * dry_weight

    # 2. 초보자 핸들링 보정
    if user_profile['is_beginner']:
        # 핸들링 점수가 5점 미만인 렌즈(흐물거리는 것)는 감점
        if product['handling'] < 5.0:
            score -= 30 
        else:
            score += product['handling'] * 3

    # 3. 가격 가중치 (가성비 선호 시)
    if user_profile['price_pref'] == 'value':
        # 5만원보다 싸면 가점, 비싸면 감점
        price_diff = 50000 - product['price']
        score += price_diff * 0.001 

    return round(score, 1)

def get_eye_mbti(user_profile):
    """
    [기능 3] MBTI 코드 생성기 (ISTJ 등)
    """
    code = ""
    # E(야외) vs I(실내)
    code += "I" if user_profile['digital_time'] > 6 else "E"
    # S(예민) vs N(둔감)
    code += "S" if user_profile['dry_sensitivity'] >= 3 else "N"
    # T(성능) vs F(가성비)
    code += "T" if user_profile['price_pref'] == 'performance' else "F"
    # J(초보) vs P(고수)
    code += "J" if user_profile['is_beginner'] else "P"
    
    return code