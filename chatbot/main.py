# import openai
# from langchain.prompts import PromptTemplate, ChatPromptTemplate
# from langchain.prompts.chat import SystemMessagePromptTemplate, HumanMessagePromptTemplate
# from langchain.chains import LLMChain
# from langchain.chat_models import ChatOpenAI
#
#
# def get_data_loader() -> str:
#     # 1. 데이터 파일을 로딩하여 데이터를 생성한다
#     with open("project_data_카카오싱크.txt", "r") as f:
#         raw_data = f.read()
#
#     # 2. 수집된 데이터를 정형화 시킨다.
#     formatted_data = []
#     for data in raw_data.split("#"):
#         rows = [row.strip() for row in data.split("\n") if row.strip() != ""]
#         category = rows[0]
#
#         if category in ["기능 소개", "설정 안내"]:
#             keys = rows[2].split(" | ")
#             formatted_examples = [f"{key} : {value}"
#                                   for row in rows[3:]
#                                   for key, value in zip(keys, row.split(" | "))]
#             formatted_data.extend([*rows[:2], *formatted_examples])
#         else:
#             formatted_data.extend(rows)
#     return "\n\n".join(formatted_data)
#
#
# def answer_using_chatgpt(user_input: str):
#     llm = ChatOpenAI(
#         openai_api_key=open("../appkey.txt", "r").read(),
#         model_name="gpt-3.5-turbo"
#     )
#
#     prompt_template = ChatPromptTemplate.from_messages(
#         [
#             SystemMessagePromptTemplate.from_template(
#                 """
#                 assistant는 챗봇으로서 동작한다. 가이드를 참고하여 질문에 답변한다.
#
#                 가이드
#                 '''
#                 {guide}
#                 '''
#                 """
#             ),
#             HumanMessagePromptTemplate.from_template("{question}")
#         ]
#     )
#     chain = LLMChain(llm=llm, prompt=prompt_template)
#     answer = chain.run(
#         guide=get_data_loader(),
#         question=user_input
#     )
#     return answer
