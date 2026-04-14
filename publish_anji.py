import os
import datetime
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

# 1. 환경 설정 로드
load_dotenv()
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def publish_cartoon():
    # 2. 정보 입력 받기
    title = input("만화 제목을 입력하세요: ")
    summary = input("짧은 줄거리를 입력하세요 (AI용 데이터): ")
    
    # raw_images 폴더에서 파일 목록 가져오기
    image_folder = "./raw_images"
    images = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    if not images:
        print("❌ raw_images 폴더에 이미지 파일이 없습니다!")
        return

    print(f"📸 총 {len(images)}개의 이미지를 발견했습니다. 업로드를 시작합니다...")

    uploaded_urls = []
    
    # 3. Cloudinary 업로드
    for img in sorted(images):
        file_path = os.path.join(image_folder, img)
        print(f"📤 {img} 업로드 중...")
        response = cloudinary.uploader.upload(file_path, folder="anji_blog")
        uploaded_urls.append(response['secure_url'])

   # 4. Jekyll 포스트 마크다운 파일 생성
    today = datetime.date.today().strftime("%Y-%m-%d")
    # 파일명 형식: 2026-04-14-제목.md
    safe_title = title.replace(" ", "-")
    file_name = f"_posts/{today}-{safe_title}.md"
    
    # 9컷 만화 형식을 고려한 본문 구성
    content = f"""---
layout: post
title: "{title}"
date: {today}
cover_image: "{uploaded_urls[0]}"
summary: "{summary}"
---

### {title}

"""
    # 업로드된 모든 이미지를 본문에 추가
    for url in uploaded_urls:
        content += f"![Anji Cartoon]({url})\n\n"

    # 파일 저장 (errors="ignore" 추가로 인코딩 에러 방지)
    with open(file_name, "w", encoding="utf-8", errors="ignore") as f:
        f.write(content)

    print(f"✅ 포스트 생성 완료: {file_name}")
    print("🚀 이제 'jekyll serve' 중인 브라우저를 확인하세요!")

if __name__ == "__main__":
    publish_cartoon()