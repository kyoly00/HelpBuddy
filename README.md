# Help Buddy 🤝 - 외국인 노동자 지원 챗봇

**Help Buddy**는 외국인 노동자가 겪는 법적·행정적 어려움을 도와주는 Solara 기반 웹 챗봇입니다.  
사용자의 언어, 성별, 국적, 직종, 비자 정보 등을 입력받아 맞춤형 법률 및 노동 정보를 제공합니다.

---

## 💡 주요 기능

- 🗣️ **다국어 지원**: 외국인 사용자를 위한 다국어 입력 시스템 (`Language = ko`, 베트남어 등 지원)
- 📋 **개인 정보 기반 추천**: 연령, 성별, 국적, 비자, 거주지 정보를 바탕으로 적절한 정보 제공
- 💬 **법률 상담 챗봇**: 임금 체불, 산업 재해, 불법 해고 등 고용 관련 주요 문제에 대한 설명 제공
- ☎️ **상담처 안내**: 고용노동부, 한국노동법률원 등의 연락처 제공

---

## 🧠 사용 예시
### 1. 언어 선택
<img src="https://github.com/user-attachments/assets/f6a422e7-ed4a-4afc-8159-71df341b90d6" width=300px/>


### 2. 기본 개인 정보 선택
<img src="https://github.com/user-attachments/assets/32d2e0f6-7ce4-411e-a5c3-7bb180d6e65e" width=300px/>


### 3. 챗봇에게 질문할 카테고리 선택
<img src="https://github.com/user-attachments/assets/bf0319f1-db72-4208-8c72-41e2c0473402" width=300px/>


### 4. 챗봇에게 질문                                                                    
<table>
  <tr>
    <td><img src="https://github.com/user-attachments/assets/2eb5208e-956d-465d-9514-a126fd7dd3e6" width=300px height=500px/></td>
    <td><img src="https://github.com/user-attachments/assets/37a84726-addd-48af-81c6-bea6191e7c41" width=300px height=500px/></td>
  </tr>
</table>

---

## 🛠️ 설치 및 실행

```bash
# 1. 가상환경 생성 및 패키지 설치
conda create -n helpbuddy_env python=3.10
conda activate helpbuddy_env
pip install solara openai pandas

# 2. .env파일에 API_KEY 등록
  한국어 번역을 위한 NAVER_API와 chatbot 이용을 위한 OPENAI_API_KEY 입력
  입력 예시:
  CLIENT_ID="YOUR_NAVER_API_CLIENT_ID"
  CLIENT_SECRET="YOUR_NAVER_API_CLIENT_SECRET"
  OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
 
# 3. 실행
solara run help_buddy_chatbot.py
