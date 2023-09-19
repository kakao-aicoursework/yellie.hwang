"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config

import pynecone as pc
from pynecone.base import Base

from langchain.prompts import ChatPromptTemplate
from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI


docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"


def get_data_loader() -> str:
    # 1. 데이터 파일을 로딩하여 데이터를 생성한다
    with open("project_data_카카오싱크.txt", "r") as f:
        raw_data = f.read()

    # 2. 수집된 데이터를 정형화 시킨다.
    formatted_data = []
    for data in raw_data.split("#"):
        rows = [row.strip() for row in data.split("\n") if row.strip() != ""]
        category = rows[0]

        if category in ["기능 소개", "설정 안내"]:
            keys = rows[2].split(" | ")
            formatted_examples = [f"{key} : {value}"
                                  for row in rows[3:]
                                  for key, value in zip(keys, row.split(" | "))]
            formatted_data.extend([*rows[:2], *formatted_examples])
        else:
            formatted_data.extend(rows)
    return "\n\n".join(formatted_data)


def answer_using_chatgpt(user_input: str):
    print("create llm ...")
    llm = ChatOpenAI(
        openai_api_key=open("../appkey.txt", "r").read(),
        model_name="gpt-3.5-turbo"
    )

    print("create prompt template ...")
    prompt_template = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate.from_template(
                f"""
                assistant는 챗봇으로서 동작한다. 가이드를 참고하여 질문에 답변한다.

                가이드
                '''
                {get_data_loader()}
                '''
                """
            ),
            HumanMessagePromptTemplate.from_template("{question}")
        ]
    )

    print("create chain and run ...")
    chain = LLMChain(llm=llm, prompt=prompt_template)
    answer = chain.run(
        question=user_input,
        verbose=True
    )
    return answer


class Message(Base):
    original_text: str
    text: str


class State(pc.State):
    """The app state."""

    text: str = ""
    messages: list[Message] = []

    @pc.var
    def output(self) -> str:
        if not self.text.strip():
            return "답변 대기 중 ..."
        return answer_using_chatgpt(self.text)

    def post(self):
        self.messages = [
            Message(
                original_text=self.text,
                text=self.output,
            )
        ] + self.messages


def header():
    """Basic instructions to get started."""
    return pc.box(
        pc.text("카카오 싱크 문의 챗봇 🗺", font_size="2rem"),
        pc.text(
            "카카오 싱크에 대해 궁금한 것을 물어보세요!",
            margin_top="0.5rem",
            color="#666",
        ),
    )


def text_box(text, is_answer):
    return pc.text(
        text,
        background_color="#fff" if is_answer else "#0A69DA",
        padding="1rem",
        border_radius="8px",
    )


def message(message):
    return pc.box(
        text_box(message.original_text, False),
        text_box(message.text, True),
        background_color="#f5f5f5",
        padding="1rem",
        border_radius="8px",
    )


def output():
    return pc.box(
        pc.text(State.output),
        padding="1rem",
        border="1px solid #eaeaef",
        margin_top="1rem",
        border_radius="8px",
        position="relative",
    )


def index() -> pc.Component:
    return pc.container(
        header(),
        pc.vstack(
            pc.foreach(State.messages, message),
            margin_top="2rem",
            spacing="1rem",
            align_items="left"
        ),
        output(),
        pc.input(
            placeholder="질문을 입력하세요!",
            on_blur=State.set_text,
            margin_top="1rem",
            border_color="#eaeaef"
        ),
        pc.button("Post", on_click=State.post, margin_top="1rem"),
    )


# Add state and page to the app.
app = pc.App(state=State)
app.add_page(index)
app.compile()
