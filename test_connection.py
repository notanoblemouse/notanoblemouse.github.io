import os
from dotenv import load_dotenv
import cloudinary

# .env 파일 로드
load_dotenv()

# 환경 변수 확인
cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
api_key = os.getenv('CLOUDINARY_API_KEY')
api_secret = os.getenv('CLOUDINARY_API_SECRET')

if not cloud_name or not api_key or not api_secret:
    print("❌ 에러: .env 파일에서 정보를 읽어오지 못했습니다. 파일명과 내용을 확인하세요.")
else:
    print(f"✅ 연결 시도 중: {cloud_name}")
    
    try:
        cloudinary.config(
            cloud_name=cloud_name,
            api_key=api_key,
            api_secret=api_secret
        )
        print("🚀 성공: Cloudinary 설정이 완료되었습니다!")
    except Exception as e:
        print(f"❌ 실패: {e}")