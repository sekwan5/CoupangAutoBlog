# import time
# import pyperclip
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.chrome.options import Options
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys

# # 네이버 로그인 정보 (테스트용 하드코딩)
# NAVER_ID = "november_07"
# NAVER_PW = "goarns=00"
# NAVER_BLOG_URL = "https://blog.naver.com/november_07"

# # ChromeDriver 설정
# chrome_options = Options()
# chrome_options.add_argument("--no-sandbox")
# chrome_options.add_argument("--disable-dev-shm-usage")
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 자동화 탐지 방지
# chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# # 웹 드라이버 실행
# service = Service(ChromeDriverManager().install())
# driver = webdriver.Chrome(service=service, options=chrome_options)

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

# def naver_login():
#     """네이버 로그인 (로그인이 필요한 경우에만 실행)"""
#     driver.get("https://nid.naver.com/nidlogin.login")
#     time.sleep(2)

#     # 아이디 입력 (pyperclip 사용)
#     id_input = driver.find_element(By.ID, "id")
#     pyperclip.copy(NAVER_ID)
#     id_input.send_keys(Keys.CONTROL, "v")
#     time.sleep(1)

#     # 비밀번호 입력 (pyperclip 사용)
#     pw_input = driver.find_element(By.ID, "pw")
#     pyperclip.copy(NAVER_PW)
#     pw_input.send_keys(Keys.CONTROL, "v")
#     time.sleep(1)

#     # 로그인 상태 유지 체크박스 클릭 (예외처리 추가)
#     try:
#         keep_checkbox = driver.find_element(By.ID, "keep")
#         is_checked = keep_checkbox.get_attribute("value") == "on"  # 체크 여부 확인

#         if not is_checked:  # 체크되어 있지 않다면 클릭
#             keep_checkbox_label = driver.find_element(By.CSS_SELECTOR, "label[for='keep']")
#             keep_checkbox_label.click()
#             time.sleep(1)
#             print("✅ 로그인 상태 유지 체크 완료!")
#         else:
#             print("✅ 로그인 상태 유지가 이미 체크되어 있음")

#     except Exception as e:
#         print(f"⚠️ 로그인 상태 유지 체크 실패: {e}")


#     # 로그인 버튼 클릭
#     # login_btn = driver.find_element(By.ID, "log.login")
#     # login_btn.click()
#     # time.sleep(5)  # 로그인 후 페이지 이동 대기

#     print("✅ 네이버 로그인 완료!")

# def go_to_blog_write():
#     """네이버 블로그 글쓰기 페이지로 이동"""
#     driver.get(f"{NAVER_BLOG_URL}?Redirect=Write&")
#     time.sleep(3)
#     print("✅ 블로그 글쓰기 페이지 이동 완료!")

# # 실행
# if __name__ == "__main__":
#     if not is_logged_in():  # 로그인되지 않은 경우에만 로그인 실행
#         naver_login()
    
#     # go_to_blog_write()  # 블로그 글쓰기 페이지로 이동

#     # 프로그램 종료 방지 (사용자가 Enter를 누를 때까지 대기)
#     input("프로그램을 종료하려면 Enter를 누르세요...")
