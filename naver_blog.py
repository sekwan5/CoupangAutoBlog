import time
import pyperclip
import os
import autoit
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# 네이버 로그인 정보 (테스트용 하드코딩)

# def is_logged_in():
#     """현재 로그인 상태인지 확인"""
#     driver.get(NAVER_BLOG_URL)
#     time.sleep(2)
    
#     try:
#         # 로그인된 경우 블로그 닉네임이 보임
#         driver.find_element(By.CLASS_NAME, "gnb_my_namebox")
#         print("✅ 이미 로그인되어 있음!")
#         return True
#     except:
#         print("⚠️ 로그인 필요")
#         return False

def naver_login(driver,id,pw):
    driver.get("https://nid.naver.com/nidlogin.login")
    time.sleep(2)

    # 아이디 입력 (pyperclip 사용)
    id_input = driver.find_element(By.ID, "id")
    pyperclip.copy(id)
    id_input.send_keys(Keys.CONTROL, "v")
    time.sleep(1)

    # 비밀번호 입력 (pyperclip 사용)
    pw_input = driver.find_element(By.ID, "pw")
    pyperclip.copy(pw)
    pw_input.send_keys(Keys.CONTROL, "v")
    time.sleep(1)

    # 로그인 상태 유지 체크박스 클릭 (예외처리 추가)
    # try:
    #     keep_checkbox = driver.find_element(By.ID, "keep")
    #     is_checked = keep_checkbox.get_attribute("value") == "on"  # 체크 여부 확인

    #     if not is_checked:  # 체크되어 있지 않다면 클릭
    #         keep_checkbox_label = driver.find_element(By.CSS_SELECTOR, "label[for='keep']")
    #         keep_checkbox_label.click()
    #         time.sleep(1)
    #         print("✅ 로그인 상태 유지 체크 완료!")
    #     else:
    #         print("✅ 로그인 상태 유지가 이미 체크되어 있음")

    # except Exception as e:
    #     print(f"⚠️ 로그인 상태 유지 체크 실패: {e}")


    # 로그인 버튼 클릭
    login_btn = driver.find_element(By.ID, "log.login")
    login_btn.click()
    time.sleep(5)  # 로그인 후 페이지 이동 대기

    # print("✅ 네이버 로그인 완료!")

from selenium.webdriver.common.action_chains import ActionChains

def go_to_blog_write(driver, id_, content,data):
    """네이버 블로그 글쓰기 페이지 이동 및 자동 작성"""
    driver.get(f"https://blog.naver.com/{id_}?Redirect=Write")
    time.sleep(4)

    try:
        frame = driver.find_element(By.ID, "mainFrame")
        driver.switch_to.frame(frame)
        print("✅ 블로그 글쓰기 페이지 프레임 전환 완료")
        time.sleep(3)
    except:
        print("⚠️ 블로그 글쓰기 프레임을 찾을 수 없음")
        return

    # 작성 중인 글 팝업 닫기
    try:
        cancel_button = driver.find_element(By.CSS_SELECTOR, "button.se-popup-button-cancel")
        cancel_button.click()
        time.sleep(1)
        print("✅ 작성 중이던 글 취소 완료")
    except:
        print("ℹ️ 작성 중인 글 팝업 없음")

    # 도움말 팝업 닫기
    try:
        help_close_button = driver.find_element(By.CSS_SELECTOR, ".se-help-panel-close-button")
        help_close_button.click()
        print("✅ 도움말 팝업 닫기 완료")
    except:
        print("ℹ️ 도움말 팝업 없음")

    # 제목 입력
    try:
        title_element = driver.find_element(By.CSS_SELECTOR, "div.se-module-text.se-title-text span")
        action = ActionChains(driver)
        action.move_to_element(title_element).click().send_keys(content["title"]).perform()
        print("✅ 제목 작성 완료")
        time.sleep(1)
    except Exception as e:
        print(f"⚠️ 제목 입력 실패: {e}")

    # 본문 입력
    try:
        content_element = driver.find_element(By.CSS_SELECTOR, "span.se-placeholder.__se_placeholder.se-fs15")
        action.move_to_element(content_element).click().send_keys(content["content"]).perform()
        print("✅ 본문 작성 완료")
        time.sleep(1)
    except Exception as e:
        print(f"⚠️ 본문 입력 실패: {e}")

    img_path = data["main_img_path"]  # 절대 경로 변환
    print(f"🔍 변환된 절대 경로: {img_path}")

    # 이미지 업로드
    upload_image(driver, img_path)

    # 발행 버튼 클릭
    try:
        send = driver.find_elements(By.TAG_NAME, "button")[3]
        send.click()
        time.sleep(1)
            
        select_category(driver, "python")

        post = driver.find_elements(By.TAG_NAME, "button")[9]
        post.click()
        print("✅ 블로그 포스팅 완료!")
    except Exception as e:
        print(f"⚠️ 블로그 발행 실패: {e}")


def upload_image(driver, img_path):
    """이미지 업로드 함수"""
    if os.path.exists(img_path):
        try:
            upload_button = driver.find_element(By.CSS_SELECTOR, "button.se-image-toolbar-button")
            upload_button.click()
            time.sleep(2)

            # AutoIt을 사용하여 파일 선택 창에 이미지 경로 입력
            autoit.win_wait_active("열기", 5)  # 파일 선택 창 활성화 대기 (최대 5초)
            autoit.control_set_text("열기", "Edit1", img_path)  # 파일 경로 입력
            autoit.control_send("열기", "Edit1", "{ENTER}")  # 엔터 키 입력 (파일 선택 후 업로드)
            print("✅ 이미지 업로드 완료")
            return True
        except Exception as e:
            print(f"⚠️ 이미지 업로드 실패: {e}")
            return False
    else:
        print(f"⚠️ 이미지 파일이 존재하지 않습니다: {img_path}")
        return False
    
def select_category(driver, category_name):
    """네이버 블로그에서 원하는 카테고리 선택"""
    try:
        # 카테고리 선택 버튼 클릭
        category_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, '카테고리 목록 버튼')]"))
        )
        category_button.click()
        time.sleep(2)

        # 원하는 카테고리 선택
        category_list = driver.find_elements(By.XPATH, "//span[@data-testid[contains(., 'categoryItemText')]]")
        for category in category_list:
            if category.text.strip() == category_name:
                category.click()
                print(f"✅ 카테고리 '{category_name}' 선택 완료")
                break
        time.sleep(1)

    except Exception as e:
        print(f"⚠️ 카테고리 선택 실패: {e}")





# 실행
# if __name__ == "__main__":
#     if not is_logged_in():  # 로그인되지 않은 경우에만 로그인 실행
#         naver_login()
    
#     # go_to_blog_write()  # 블로그 글쓰기 페이지로 이동

#     # 프로그램 종료 방지 (사용자가 Enter를 누를 때까지 대기)
#     input("프로그램을 종료하려면 Enter를 누르세요...")
