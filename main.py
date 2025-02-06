# from coupang_scraper import scrape_product
# # from gpt_review import generate_review
# # from naver_blog import post_to_naver_blog

# def main():
#     # 쿠팡 상품 URL 입력
#     product_url = "https://www.coupang.com/vp/products/7566747125"

#     # 1️⃣ 쿠팡 상품 크롤링
#     product_data = scrape_product(product_url)
#     print("✅ 상품 크롤링 완료:", product_data)

#     # 상품명 가져오기 (예외 처리)
#     product_name = product_data.get("상품명", None)
#     if not product_name:
#         print("⚠️ 상품명을 찾을 수 없음, 리뷰 생성 불가")
#     # 2️⃣ GPT 리뷰 생성
#     # review_content = generate_review(product_name)
#     # if "error" in review_content:
#     #     print("⚠️ GPT 리뷰 생성 실패:", review_content["error"])
#     #     return
#     # print("✅ GPT 리뷰 생성 완료")

#     # 3️⃣ 네이버 블로그 포스팅
#     # post_result = post_to_naver_blog(product_data, review_content)
#     # if post_result:
#     #     print("✅ 블로그 포스팅 완료:", post_result)
#     # else:
#     #     print("⚠️ 블로그 포스팅 실패")

# if __name__ == "__main__":
#     main()
