import os
import datetime
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
from PIL import Image  # 이미지 처리를 위한 라이브러리

# 1. 환경 설정 로드
load_dotenv()
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def optimize_and_publish():
    title = input("만화 제목을 입력하세요: ")
    summary = input("AI용 요약을 입력하세요: ")
    
    image_folder = "./raw_images"
    # 처리할 확장자들
    valid_extensions = ('.png', '.jpg', '.jpeg', '.webp')
    images = [f for f in os.listdir(image_folder) if f.lower().endswith(valid_extensions)]
    
    if not images:
        print("❌ raw_images 폴더에 이미지 파일이 없습니다!")
        return

    uploaded_urls = []
    print(f"🚀 총 {len(images)}개의 이미지를 최적화 및 업로드합니다...")

    for img in sorted(images):
        file_path = os.path.join(image_folder, img)
        
        # --- [이미지 최적화 단계] ---
        # 파일명을 .webp로 변경 (예: page1.png -> page1.webp)
        webp_path = os.path.splitext(file_path)[0] + ".webp"
        
        with Image.open(file_path) as image:
            # 1. RGB 모드로 변환 (PNG의 투명도 등을 처리)
            image = image.convert("RGB")
            # 2. WebP로 저장 (quality=60~80 정도로 설정하여 용량 최적화)
            # 80 정도면 눈으로 보기에 차이가 거의 없으면서 용량은 획기적으로 줄어듭니다.
            image.save(webp_path, "WEBP", quality=80, optimize=True)
        
        print(f"📦 {img} -> WebP 변환 완료 (최적화)")
        
        # 3. Cloudinary 업로드 (변환된 webp 파일을 올림)
        response = cloudinary.uploader.upload(webp_path, folder="anji_blog")
        uploaded_urls.append(response['secure_url'])
        
        # 사용한 임시 webp 파일 삭제 (원본 raw_images 관리를 위해)
        if os.path.exists(webp_path) and webp_path != file_path:
            os.remove(webp_path)

    # 4. Jekyll 포스트 생성 (이전과 동일하지만 errors="ignore" 유지)
    today = datetime.date.today().strftime("%Y-%m-%d")
    safe_title = title.replace(" ", "-")
    file_name = f"_posts/{today}-{safe_title}.md"
    
    content = f"""---
layout: post
title: "{title}"
date: {today}
cover_image: "{uploaded_urls[0]}"
summary: "{summary}"
---

### {title}

"""
    for url in uploaded_urls:
        content += f"![Anji Cartoon]({url})\n\n"

    with open(file_name, "w", encoding="utf-8", errors="ignore") as f:
        f.write(content)

    print(f"✅ 포스트 생성 완료: {file_name}")
    print("✨ 이미지가 WebP로 최적화되어 업로드되었습니다.")

if __name__ == "__main__":
    optimize_and_publish()