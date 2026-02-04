import pandas as pd
import os

# 1. 엑셀 파일 위치 찾기 (자동으로 경로 추적)
# 현재 파일(test_db.py)이 있는 폴더의 -> 상위 폴더(lens_master) -> data 폴더 -> 엑셀 파일
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(base_path, 'data', 'lens_db_v1.xlsx')

print(f"📂 파일 찾는 중... 위치: {file_path}")

# 2. 엑셀 읽기 시도
try:
    # 엑셀 파일 읽기
    df = pd.read_excel(file_path)
    
    print("\n" + "="*50)
    print("🎉 대성공! 엑셀 파일을 완벽하게 읽었습니다!")
    print("="*50)
    print(f"📊 총 {len(df)}개의 렌즈 데이터를 가져왔습니다.\n")
    
    print("[데이터 미리보기 (상위 5개)]")
    # 브랜드, 이름, 가격 컬럼만 뽑아서 보여주기
    print(df[['brand', 'name', 'price']].head()) 
    print("="*50)

except Exception as e:
    print(f"\n❌ 오류 발생: {e}")
    print("👉 'data' 폴더 안에 'lens_db_v1.xlsx' 파일이 있는지, 오타는 없는지 확인해주세요!")