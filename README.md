### Lambda@Edge를 활용한 국가별 Path 분기

---

+ ### 전제 조건
  - Cloudfront의 Viewer Country Header를 활용
  - Orgin Request에서 작동
    
+ ### 사용 이유
  - 국가별 Edge Location에서 제공 되는 Header를 활용하여 국가 언어셋에 맞는 컨텐츠를 제공하기 위함
    
