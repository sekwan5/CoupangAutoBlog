import os
import time
import json
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path
from datetime import datetime

# 저장할 폴더 설정 (절대 경로)
MAIN_IMAGE_DIR = "C:\\coupang\\images\\main"
REVIEW_IMAGE_DIR = "C:\\coupang\\images\\reviews"
JSON_DIR = "C:\\coupang\\data\\json"

# 폴더 생성
for directory in [MAIN_IMAGE_DIR, REVIEW_IMAGE_DIR, JSON_DIR]:
    Path(directory).mkdir(parents=True, exist_ok=True)

# 쿠팡 파트너스 로그인 정보
COUPANG_PARTNERS_ID = "november_07@naver.com"
COUPANG_PARTNERS_PW = "goarns=00"

def scrape_product(driver, url):
    """쿠팡 상품 정보를 크롤링"""
    driver.get(url)
    time.sleep(3)
    try:
        title_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.prod-buy-header__title"))
        )
        title = title_element.text.strip()
    except:
        title = "상품명을 찾을 수 없음"
    
    safe_title = title.replace(" ", "_")

    try:
        main_img_url = driver.find_element(By.CSS_SELECTOR, "img.prod-image__detail").get_attribute("src")
    except:
        main_img_url = None

    review_img_url = get_first_review_image(driver)

    current_date = datetime.now().strftime("%Y%m%d")
    main_img_path = save_image(main_img_url, MAIN_IMAGE_DIR, f"{current_date}_{safe_title}.jpg") if main_img_url else None
    review_img_path = save_image(review_img_url, REVIEW_IMAGE_DIR, f"{current_date}_{safe_title}.jpg") if review_img_url else None

    product_data = {
        "title": title,
        "safe_title": safe_title,
        "main_img_path": main_img_path,
        "review_img_path": review_img_path
    }

    json_file_path = os.path.join(JSON_DIR, f"{current_date}_{safe_title}.json")
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(product_data, f, ensure_ascii=False, indent=4)

    return product_data

def get_first_review_image(driver):
    """동영상이 아닌 첫 번째 정적 리뷰 이미지를 가져오기"""
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
        time.sleep(2)

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "ul.sdp-review__average__gallery__list"))
        )

        review_images = driver.find_elements(By.CSS_SELECTOR, "ul.sdp-review__average__gallery__list img.js_reviewListGalleryImage")

        for img in review_images:
            img_url = img.get_attribute("src")
            if "video.coupangcdn.com" not in img_url:
                return img_url  

    except Exception as e:
        print("리뷰 이미지 가져오기 실패:", e)
    
    return None

def save_image(url, folder, filename):
    """이미지를 다운로드하여 지정된 폴더에 저장"""
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        image_path = os.path.join(folder, filename)
        with open(image_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return image_path
    return None

def login_coupang_partners(driver,id,pw):
    """쿠팡 파트너스 로그인 (이미 로그인 상태이면 생략)"""
    driver.execute_script("window.open('https://partners.coupang.com', '_blank');")
    driver.switch_to.window(driver.window_handles[1])
    time.sleep(3)

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.header-user"))
        )
        print("✅ 이미 로그인되어 있음!")
        return True  

    except:
        print("⚠️ 로그인 필요 → 쿠팡 로그인 페이지로 이동")

    driver.get("https://login.coupang.com/login/login.pang?rtnUrl=https%3A%2F%2Fpartners.coupang.com%2Fapi%2Fv1%2Fpostlogin")
    time.sleep(3)

    try:
        id_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "login-email-input"))
        )
        pw_input = driver.find_element(By.ID, "login-password-input")
        login_btn = driver.find_element(By.CSS_SELECTOR, "button.login__button")

        id_input.send_keys(id)
        pw_input.send_keys(pw)
        login_btn.click()
        time.sleep(5)

        print("✅ 쿠팡 로그인 완료!")
        return True  

    except Exception as e:
        print("⚠️ 쿠팡 로그인 실패:", e)
        return False  

def generate_coupang_partner_link(driver, product_url):
    """쿠팡 파트너스에서 간편 링크 생성 및 단축 URL 가져오기"""
    print("🔗 간편 링크 생성 중...")
    driver.get("https://partners.coupang.com/#affiliate/ws/link-to-any-page")
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input#url"))
        )
        time.sleep(3)

        url_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "input#url"))
        )
        url_input.clear()
        url_input.send_keys(product_url)
        time.sleep(2)

        generate_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ant-btn-primary"))
        )
        generate_button.click()
        time.sleep(3)

        short_link_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.tracking-url-input.large[disabled]"))
        )
        return short_link_element.text.strip()

    except Exception as e:
        print("⚠️ 링크 생성 실패:", e)
        return None
