import openai
import json
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_review(product_name):
    """GPT를 이용하여 블로그 리뷰를 JSON 형식으로 생성하는 함수 (구매 유도 섹션 제외, 1500자 이상, 전체 마크다운 적용)"""

    prompt = f"""
    당신은 블로그 리뷰 작성 전문가입니다. 아래의 가이드를 철저히 따르면서 {product_name}에 대한 블로그 리뷰를 JSON 형식으로 작성하세요.
    
    ## 작성 지침
    - **총 글자 수**: 1500자 이상 유지
    - **마크다운 형식 전체 적용**
    
    ## 출력 형식 (JSON)
    {{
        "title": "# {product_name} - 최고의 선택!",
        "introduction": "## 🔍 서론\\n\\n{product_name}은 이런 문제를 해결해줍니다...",
        "product_analysis": {{
            "product_name": "{product_name}",
            "key_features": [
                "1️⃣ **주요 특징 1** – 상세 설명",
                "2️⃣ **주요 특징 2** – 상세 설명",
                "3️⃣ **주요 특징 3** – 상세 설명"
            ],
            "target_audience": "이 제품을 구매할 주요 고객층",
            "competitor_comparison": "### 🆚 경쟁 제품과의 차이점\\n\\n이 제품은 경쟁 제품 대비 다음과 같은 차별점을 가집니다..."
        }},
        "product_description": "**✅ 이 제품이 특별한 이유!**\\n\\n1️⃣ **핵심 장점 1** – 상세 설명\\n2️⃣ **핵심 장점 2** – 상세 설명",
        "faq": [
            {{"question": "## ❓ FAQ 질문1", "answer": "✅ FAQ 답변1"}},
            {{"question": "## ❓ FAQ 질문2", "answer": "✅ FAQ 답변2"}},
            {{"question": "## ❓ FAQ 질문3", "answer": "✅ FAQ 답변3"}}
        ],
        "tags": ["#{product_name}", "#필수템", "#인기상품"],
    }}

    ## 1. 제목 생성 (마크다운 적용)
    - `# {product_name} - 최고의 선택!`
    - 클릭 유도 요소 포함

    ## 2. 서론 작성 (전체 글의 15%)
    - 고객의 페인포인트 언급
    - {product_name}이 해결할 수 있는 문제 제시
    - 신뢰도 요소 포함 (인증, 수상내역 등)
    - 읽어야 할 이유 명확히 제시

    ## 3. 상품 분석 및 키워드 도출
    - 주요 특징 3-5가지 도출
    - 타겟 고객층 분석
    - 경쟁 제품과의 차별점 설명

    ## 4. 상품 소개 및 장점 작성 (전체 글의 70%)
    - {product_name}의 제품 스펙 및 특징 상세 소개
    - 사용 사례 및 활용 방법
    - 실제 사용자 후기 포함
    - 가격 대비 가치 강조

    ## 5. FAQ 섹션
    - {product_name}에 대한 주요 질문 5-7개
    - 배송/교환/환불 정책 설명
    - 사용 시 주의사항 및 관리법

    ## 6. 관련 태그 생성
    - {product_name} 관련 키워드 및 카테고리 태그 5개 생성

    ## 7. 전체 마크다운 적용
    - 제목: `#`, `##`, `###`
    - 리스트: `-`, `1.`, `2.`, `3.`
    - 강조: `*텍스트*`, `**강조 텍스트**`
    - 링크: `[텍스트](URL)`

    위 JSON 형식을 유지하면서 {product_name}에 대한 상세 리뷰를 작성하세요.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "당신은 블로그 리뷰를 작성하는 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
    )

    # 응답을 JSON 형식으로 변환
    review_content = response["choices"][0]["message"]["content"]
    try:
        review_json = json.loads(review_content)  # JSON 변환
    except json.JSONDecodeError:
        review_json = {"error": "JSON 변환 실패", "content": review_content}  # 오류 발생 시 원본 반환

    return review_json
