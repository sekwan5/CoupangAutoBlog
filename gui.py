import sys
import os
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QRadioButton, QButtonGroup, QSpinBox
)
from PyQt5.QtCore import Qt
from coupang_scraper import scrape_product,login_coupang_partners,generate_coupang_partner_link
from config import get_driver
LOGIN_DATA_FILE = "login_data.json"  # 로그인 정보를 저장할 JSON 파일


class CoupangAutoBlogGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_login_info()  # 프로그램 실행 시 로그인 정보 불러오기

    def initUI(self):
        self.setWindowTitle("Coupang Auto Blog")
        self.setGeometry(100, 100, 750, 450)  # 창 크기 조정

        # 메인 레이아웃 (좌측 로그인 + 우측 옵션 선택)
        main_layout = QHBoxLayout()

        # 📌 왼쪽 패널 (로그인 정보 + GPT API + 카테고리)
        left_layout = QVBoxLayout()

        # 네이버 로그인 정보
        self.naver_label = QLabel("네이버 로그인 정보")
        self.naver_id_input = QLineEdit(self)
        self.naver_id_input.setPlaceholderText("네이버 아이디 입력")
        self.naver_pw_input = QLineEdit(self)
        self.naver_pw_input.setPlaceholderText("네이버 비밀번호 입력")
        self.naver_pw_input.setEchoMode(QLineEdit.Password)  # 비밀번호 숨김

        left_layout.addWidget(self.naver_label)
        left_layout.addWidget(self.naver_id_input)
        left_layout.addWidget(self.naver_pw_input)

        # 쿠팡 로그인 정보
        self.coupang_label = QLabel("쿠팡 로그인 정보")
        self.coupang_id_input = QLineEdit(self)
        self.coupang_id_input.setPlaceholderText("쿠팡 아이디 입력")
        self.coupang_pw_input = QLineEdit(self)
        self.coupang_pw_input.setPlaceholderText("쿠팡 비밀번호 입력")
        self.coupang_pw_input.setEchoMode(QLineEdit.Password)

        left_layout.addWidget(self.coupang_label)
        left_layout.addWidget(self.coupang_id_input)
        left_layout.addWidget(self.coupang_pw_input)

        # GPT API 키 입력
        self.gpt_label = QLabel("GPT API 키")
        self.gpt_api_key_input = QLineEdit(self)
        self.gpt_api_key_input.setPlaceholderText("GPT API 키 입력")
        left_layout.addWidget(self.gpt_label)
        left_layout.addWidget(self.gpt_api_key_input)

        # 블로그 포스팅 카테고리 선택
        self.category_label = QLabel("블로그 포스팅 카테고리")
        self.category_input = QLineEdit(self)
        self.category_input.setPlaceholderText("카테고리 입력 (예: 가전제품 리뷰)")
        left_layout.addWidget(self.category_label)
        left_layout.addWidget(self.category_input)

        # 정보 저장 버튼
        self.save_button = QPushButton("정보 저장", self)
        self.save_button.clicked.connect(self.save_login_info)
        left_layout.addWidget(self.save_button)

        main_layout.addLayout(left_layout)

        # 📌 오른쪽 패널 (스크래핑 옵션)
        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop)  # 👉 위쪽으로 정렬
        right_layout.setSpacing(6)  # 👉 간격 최소화

        # 하나만 vs 여러 개 선택 (라디오 버튼을 수평 정렬)
        radio_layout = QHBoxLayout()
        self.single_radio = QRadioButton("지정 상품 포스팅")
        self.multi_radio = QRadioButton("키워드 상품 포스팅(여러개)")
        self.radio_group = QButtonGroup(self)
        self.radio_group.addButton(self.single_radio)
        self.radio_group.addButton(self.multi_radio)
        self.single_radio.setChecked(True)  # 기본 선택

        radio_layout.addWidget(self.single_radio)
        radio_layout.addWidget(self.multi_radio)
        right_layout.addLayout(radio_layout)

        # 상품 URL 입력 필드 (하나만 선택 시)
        self.url_input = QLineEdit(self)
        self.url_input.setPlaceholderText("쿠팡 상품 URL 입력")
        right_layout.addWidget(self.url_input)

        # 키워드 입력 필드 (여러 개 선택 시)
        self.keyword_input = QLineEdit(self)
        self.keyword_input.setPlaceholderText("키워드 입력")
        self.keyword_input.setEnabled(False)  # 기본적으로 비활성화
        right_layout.addWidget(self.keyword_input)

        # 몇 개의 포스팅을 생성할지 선택 (여러 개 선택 시 활성화)
        self.post_count_label = QLabel("상품 개수 선택(검색시 상위노출)")
        self.post_count_spinbox = QSpinBox(self)
        self.post_count_spinbox.setMinimum(1)
        self.post_count_spinbox.setMaximum(10)
        self.post_count_spinbox.setEnabled(False)
        right_layout.addWidget(self.post_count_label)
        right_layout.addWidget(self.post_count_spinbox)

        # 선택 변경 시 동작
        self.single_radio.toggled.connect(self.toggle_input)

        main_layout.addLayout(right_layout)

        # 📌 하단 패널 (로그 & 실행 버튼)
        bottom_layout = QVBoxLayout()

        # 로그 출력 창 (읽기 전용)
        self.log_output = QTextEdit(self)
        self.log_output.setReadOnly(True)
        bottom_layout.addWidget(self.log_output)

        # 버튼 레이아웃 (가로 정렬)
        button_layout = QHBoxLayout()

        # 포스팅 시작 버튼
        self.start_button = QPushButton("포스팅 시작", self)
        self.start_button.clicked.connect(self.run_process)  # 기존 동작 연결
        button_layout.addWidget(self.start_button)

        # 프로그램 종료 버튼
        self.exit_button = QPushButton("프로그램 종료", self)
        self.exit_button.clicked.connect(self.close)  # 프로그램 종료
        button_layout.addWidget(self.exit_button)

        # 버튼 레이아웃을 하단 패널에 추가
        bottom_layout.addLayout(button_layout)

        # 전체 레이아웃 적용
        final_layout = QVBoxLayout()
        final_layout.addLayout(main_layout)
        final_layout.addLayout(bottom_layout)
        self.setLayout(final_layout)

    def toggle_input(self):
        """라디오 버튼 변경 시 입력 필드 활성화/비활성화"""
        if self.single_radio.isChecked():
            self.url_input.setEnabled(True)
            self.keyword_input.setEnabled(False)
            self.post_count_spinbox.setEnabled(False)
        else:
            self.url_input.setEnabled(False)
            self.keyword_input.setEnabled(True)
            self.post_count_spinbox.setEnabled(True)

    def save_login_info(self):
        """네이버 & 쿠팡 로그인 정보를 JSON 파일로 저장"""
        login_data = {
            "naver_id": self.naver_id_input.text().strip(),
            "naver_pw": self.naver_pw_input.text().strip(),
            "coupang_id": self.coupang_id_input.text().strip(),
            "coupang_pw": self.coupang_pw_input.text().strip(),
            "gpt_api_key": self.gpt_api_key_input.text().strip(),
            "category": self.category_input.text().strip(),
        }

        with open(LOGIN_DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(login_data, file, ensure_ascii=False, indent=4)

        self.log_output.append("✅ 로그인 정보가 저장되었습니다.")

    def load_login_info(self):
        """프로그램 실행 시 저장된 로그인 정보를 불러오기"""
        if os.path.exists(LOGIN_DATA_FILE):
            with open(LOGIN_DATA_FILE, "r", encoding="utf-8") as file:
                try:
                    data = json.load(file)
                    self.naver_id_input.setText(data.get("naver_id", ""))
                    self.naver_pw_input.setText(data.get("naver_pw", ""))
                    self.coupang_id_input.setText(data.get("coupang_id", ""))
                    self.coupang_pw_input.setText(data.get("coupang_pw", ""))
                    self.gpt_api_key_input.setText(data.get("gpt_api_key", ""))
                    self.category_input.setText(data.get("category", ""))
                    self.log_output.append("✅ 저장된 로그인 정보를 불러왔습니다.")
                except json.JSONDecodeError:
                    self.log_output.append("⚠️ 로그인 정보 JSON 파일이 손상되었습니다.")

    def run_process(self):
        """포스팅 시작 버튼 클릭 시 실행되는 함수"""
        self.log_output.append("🚀 포스팅을 시작합니다...")

        driver = get_driver()  # 이제 버튼을 눌렀을 때만 Selenium 실행

        # 쿠팡 상품 크롤링 실행 (하나만 입력)
        if self.single_radio.isChecked():
            product_url = self.url_input.text().strip()
            if not product_url:
                self.log_output.append("⚠️ 쿠팡 상품 URL을 입력하세요.")
                return

            self.log_output.append("🔍 쿠팡 상품 정보를 가져오는 중...")
            product_data = scrape_product(product_url)
            if product_data["상품명"] == "상품명을 찾을 수 없음":
                self.log_output.append("⚠️ 상품 정보를 가져오지 못했습니다. URL을 확인하세요.")
                return
            self.log_output.append(f"✅ 크롤링 완료: {product_data['상품명']}")

            if login_coupang_partners():
                partner_link = generate_coupang_partner_link(product_url)
                print("🔗 최종 생성된 쿠팡 파트너스 링크:", partner_link)

            # GPT 리뷰 생성
            # self.log_output.append("✍ GPT 리뷰 생성 중...")
            # review_content = generate_review(product_data["상품명"])
            # self.log_output.append("✅ 리뷰 생성 완료")

            # 네이버 블로그 포스팅
            # self.log_output.append("📝 네이버 블로그에 포스팅 중...")
            # post_result = post_to_naver_blog(product_data, review_content)
            # self.log_output.append(f"✅ 블로그 포스팅 완료: {post_result}")

        # 키워드로 여러 개 포스팅 실행
        else:
           

            self.log_output.append("🎉 모든 작업이 완료되었습니다.")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoupangAutoBlogGUI()
    window.show()
    sys.exit(app.exec())
