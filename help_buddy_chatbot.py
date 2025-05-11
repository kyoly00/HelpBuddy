import os
from typing import List
import urllib.request
import json

from openai import OpenAI
from typing_extensions import TypedDict

import solara
import solara.lab


# papago api를 통한 번역 함수
def translate_text(text, from_lan = 'ko',to_lang= "en", honorific = "N"):
    if from_lan == "ko" and to_lang == "ko":
        translated_text = text
    else:
        client_id = os.getenv("CLIENT_ID")  # NAVER Client ID
        client_secret = os.getenv("CLIENT_SECRET")  # NAVER Client Secret
        encText = urllib.parse.quote(text)
        from_lan = from_lan
        to_lang = to_lang
        data = f"source={from_lan}&target={to_lang}&text={encText}&honorific={honorific}"
        url = "https://naveropenapi.apigw.ntruss.com/nmt/v1/translation"
        request = urllib.request.Request(url)
        request.add_header("X-NCP-APIGW-API-KEY-ID",client_id)
        request.add_header("X-NCP-APIGW-API-KEY",client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        response_body = response.read()
        txt_return = response_body.decode('utf-8')
        txt_return_1 = json.loads(txt_return)
        translated_text = txt_return_1['message']['result']['translatedText']
        translated_text

    return translated_text

def trans_lan(lan):
    if lan == "ko": return "한국어"
    elif lan == "en": return "영어"
    elif lan == "ja": return "일본어"
    elif lan == "zh-CN": return "중국어 간체"
    elif lan == "zh-TW": return "중국어 번체"
    elif lan == "vi": return "베트남어"
    elif lan == "th": return "태국어"
    elif lan == "id": return "인도네시아어"


# OpenAI API를 위한 메시지 저장 클래스
class MessageDict(TypedDict):
    role: str
    content: str

# 시스템 변수 사용하도록 변경 필요
if os.getenv("OPENAI_API_KEY") is None and "OPENAI_API_KEY" not in os.environ:
    openai = None
else:
    openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

messages: solara.Reactive[List[MessageDict]] = solara.reactive([])

def no_api_key_message():
    messages.value = [
        {
            "role": "assistant",
            "content": "No OpenAI API key found. Please set your OpenAI API key in the environment variable `OPENAI_API_KEY`.",
        },
    ]
    
# OpenAI API를 통해 생성된 답변을 messages에 저장하는 함수
def add_chunk_to_ai_message(chunk: str):
    messages.value = [
        *messages.value[:-1],
        {
            "role": "assistant",
            "content": messages.value[-1]["content"] + chunk,
        },
    ]

# 사용자 정보 변수화
Languages = ["en", "ko","ja","zh-CN","zh-TW","vi","th","id"]
Language = solara.reactive("ko")

# 언어별 메뉴 목록 dict
manu_dict = {
    "ko": {
        'Sexs': ["남자", "여자", "밝히고 싶지 않음"],
        'Works': ["건설", "제조", "농업"],
        'Nations': ["미국", "일본", "중국", "베트남", "인도네시아"],
        "Visas": ["E9", "E11"],
    },
    "en": {
        'Sexs': ["Male", "Female", "Prefer not to say"],
        'Works': ["Construction", "Manufacturing", "Agriculture"],
        'Nations': ["USA", "Japan", "China", "Vietnam", "Indonesia"],
        "Visas": ["E9", "E11"],
    },
    "ja": {
        'Sexs': ["男性", "女性", "答えたくない"],
        'Works': ["建設", "製造", "農業"],
        'Nations': ["アメリカ", "日本", "中国", "ベトナム", "インドネシア"],
        "Visas": ["E9", "E11"],
    },
    "zh-CN": {
        'Sexs': ["男", "女", "不愿透露"],
        'Works': ["建筑", "制造", "农业"],
        'Nations': ["美国", "日本", "中国", "越南", "印度尼西亚"],
        "Visas": ["E9", "E11"],
    },
    "zh-TW": {
        'Sexs': ["男", "女", "不願透露"],
        'Works': ["建築", "製造", "農業"],
        'Nations': ["美國", "日本", "中國", "越南", "印尼"],
        "Visas": ["E9", "E11"],
    },
    "vi": {
        'Sexs': ["Nam", "Nữ", "Không muốn tiết lộ"],
        'Works': ["Xây dựng", "Sản xuất", "Nông nghiệp"],
        'Nations': ["Mỹ", "Nhật Bản", "Trung Quốc", "Việt Nam", "Indonesia"],
        "Visas": ["E9", "E11"],
    },
    "th": {
        'Sexs': ["ชาย", "หญิง", "ไม่ต้องการระบุ"],
        'Works': ["ก่อสร้าง", "การผลิต", "เกษตรกรรม"],
        'Nations': ["สหรัฐอเมริกา", "ญี่ปุ่น", "จีน", "เวียดนาม", "อินโดนีเซีย"],
        "Visas": ["E9", "E11"]
    },
    "id": {
        'Sexs': ["Pria", "Wanita", "Tidak ingin menyebutkan"],
        'Works': ["Konstruksi", "Manufaktur", "Pertanian"],
        'Nations': ["Amerika Serikat", "Jepang", "Cina", "Vietnam", "Indonesia"],
        "Visas": ["E9", "E11"]
    }
}

manu_info_dict = {
    "ko": ["나이를 입력하세요", "성별", "직종", "국적", "비자"],
    "en": ["Enter age", "Gender", "Occupation", "Nationality", "Visa"],
    "ja": ["年齢を入力してください", "性別", "職種", "国籍", "ビザ"],
    "zh-CN": ["请输入年龄", "性别", "职业", "国籍", "签证"],
    "zh-TW": ["請輸入年齡", "性別", "職業", "國籍", "簽證"],
    "vi": ["Nhập tuổi", "Giới tính", "Nghề nghiệp", "Quốc tịch", "Thị thực"],
    "th": ["กรอกอายุ", "เพศ", "อาชีพ", "สัญชาติ", "วีซ่า"],
    "id": ["Masukkan usia", "Jenis kelamin", "Pekerjaan", "Kewarganegaraan", "Visa"]
}

age = solara.reactive(int(0))
sex = '남자'
work = '건설'
nation = '미국'
visa = 'E9'
region = solara.reactive(str("서울시 강남구"))

@solara.component
def Home():
    with solara.AppBar():
        solara.AppBarTitle("Help Buddy")  # Set the app title here
    
    with solara.Card():
        with solara.Row():
            solara.Select(label="Language", value=Language, values=Languages)

    if Language.value in Languages:
        try:
            Sexs = manu_dict[Language.value]['Sexs'] 
            sex = solara.reactive(manu_dict[Language.value]['Sexs'][0])

            Works = manu_dict[Language.value]['Works'] 
            work = solara.reactive(manu_dict[Language.value]['Works'][0])

            Nations = manu_dict[Language.value]['Nations'] 
            nation = solara.reactive(manu_dict[Language.value]['Nations'][0])

            Visas =manu_dict[Language.value]['Visas'] 
            visa = solara.reactive("E9")

            with solara.Card():
                with solara.Column(style={"align-items": "left"}):
                    with solara.Row():
                        solara.InputInt(label=f"{manu_info_dict[Language.value][0]}", value=age)

                    with solara.Row():
                        solara.Select(label=f"{manu_info_dict[Language.value][1]}", value=sex, values=Sexs)

                    with solara.Row():
                        solara.Select(label=f"{manu_info_dict[Language.value][2]}", value=work, values=Works)

                    with solara.Row():
                        solara.Select(label=f"{manu_info_dict[Language.value][3]}", value=nation, values=Nations)

                    with solara.Row():
                        solara.Select(label=f"{manu_info_dict[Language.value][4]}", value=visa, values=Visas)
            with solara.Link("/Chat", style={"width": "100%"}):
                solara.Button("Start the Chat", style={"width": "100%","background-color":"rgb(25,118,210)","color":"rgb(255,255,255)"})
        except:
            with solara.Card():
                with solara.Row():
                    solara.Text("Chose your language")



    else:
        with solara.Card():
            with solara.Row():
                solara.Text("Chose your language")

@solara.component
def Page():
    with solara.AppBar():
        solara.AppBarTitle("Help Buddy")  # Set the app title here

    with solara.Sidebar():
        solara.Markdown("# Help Buddy")  # Sidebar title
        with solara.Column(style={"min-height": "50vh"}):
            solara.Button(label="Visa", style={"height": "50px"})
            solara.Button(label="Wage", style={"height": "50px"})
            solara.Button(label="Industrial accident", style={"height": "50px"})
        
    user_message_count = len([m for m in messages.value if m["role"] == "user"])

    # 사용자가 입력한 메시지를 OpenAI에게 전송가능한 형태로 저장하는 함수(사용자 화면에 띄울 메시지)
    def send(message):
        messages.value = [
            *messages.value,
            {"role": "user", "content": message},
        ]


    def call_openai():
        if user_message_count == 0:
            return
        if openai is None:
            no_api_key_message()
            return
        prefix = f"나는 {nation}에서 {visa}로 한국에 왔어. 현재 {region}에서 {work}업에 종사 중인 {age}살인 {sex}야.\n"
        suffix = f"\n너가 fine tuning 시에 학습한 질문이면 학습한 데이터를 바탕으로 답변해줘."

        new_messages = []
        for msg in messages.value:
            if msg["role"] == "user":
                content = msg["content"]
                if Language.value != "ko":
                    content = translate_text(content, from_lan=Language.value, to_lang="ko")
                new_messages.append({"role": msg["role"], "content": content})
            else:
                new_messages.append(msg)

        new_messages = [{"role": "user", "content": prefix + new_messages[0]["content"] + suffix}] + new_messages[1:]

        response = openai.chat.completions.create(
            # gpt-3.5-turbo 모델을 사전에 생성한 예상 질문-답변 데이터를 이용해 fine-tuning한 모델 사용
            model = "ft:gpt-3.5-turbo-0125:personal:chatbot:9muZnWaD:ckpt-step-406",
            messages=new_messages,  # type: ignore
            stream=True,
            temperature=0.3,
            max_tokens=2048,
            top_p=0.3
        )
        
        full_response = ""
        for chunk in response:
            if chunk.choices[0].finish_reason == "stop":  # type: ignore
                break
            # 기존에 add_chunk_to_ai_message함수로 chunk(한 단어씩)받아 바로바로 출력하던 거에서 chunk모으는 걸로
            full_response += chunk.choices[0].delta.content  # type: ignore
        
        # chunk 모두 모은 전체 답변을 api를 통해 번역하여 제공
        messages.value = [*messages.value, {"role": "assistant", "content": translate_text(full_response, from_lan = "ko", to_lang= Language.value, honorific="Y")}]
    
    task = solara.lab.use_task(call_openai, dependencies=[user_message_count])  # type: ignore

    with solara.Column(
        style={"width": "auto", "height": "auto"},
    ):
        with solara.lab.ChatBox():
            for item in messages.value:
                with solara.lab.ChatMessage(
                    user=item["role"] == "user",
                    avatar=False,
                    name="ChatGPT" if item["role"] == "assistant" else "User",
                    color="rgba(0,0,0, 0.06)" if item["role"] == "assistant" else "#ff991f",
                    avatar_background_color="primary" if item["role"] == "assistant" else None,
                    border_radius="20px",
                ):
                    solara.Markdown(item["content"])
        if task.pending:
            solara.Text("I'm thinking...", style={"font-size": "1rem", "padding-left": "20px"})
        solara.lab.ChatInput(send_callback=send, disabled=task.pending)

@solara.component
def Layout(children):
    route, routes = solara.use_route()
    return solara.AppLayout(children=children, color="orange")  # if dark_effective else "primary")


routes = [
    solara.Route(path="/", component=Home, label="HOME"),
    solara.Route(path="Chat", component=Page, label="CHAT"),    
]