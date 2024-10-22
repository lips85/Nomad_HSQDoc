import re
import os
import streamlit as st

from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain.vectorstores.faiss import FAISS
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
import requests

# 파일 분리 (상수들)
from utils.constant.constant import OPENAI_MODEL, API_KEY_PATTERN, MODEL_PATTERN

# 파일 분리 (함수들)
from utils.functions.save_env import SaveEnv
from utils.functions.debug import Debug
from utils.functions.chat import ChatMemory, ChatCallbackHandler

# 디버그용
from dotenv import load_dotenv

load_dotenv()

# backend urls

USERS_URL = "http://127.0.0.1:8000/api/v1/users/"
CONVERSATIONS_URL = "http://127.0.0.1:8000/api/v1/conversations/"
MESSAGES_URL = "http://127.0.0.1:8000/api/v1/messages/"


# front 손보기
for key, default in [
    # jwt token을 담기 위한 session state
    ("jwt", None),
    # 로그인 했는지를 나타내는 session state
    ("is_login", False),
    # 현재 유저가 보고 있는 대화방의 대화 기록 url을 나타내는 session state
    ("messages_url", None),
    # 현재 유저가 보고 있는 대화방의 url을 나타내는 session state
    ("conversation_url", None),
    # langchain
    ("messages", {}),
    ("api_key", None),
    ("api_key_check", False),
    ("openai_model", "선택해주세요"),
    ("openai_model_check", False),
    ("file_check", False),
]:
    if key not in st.session_state:
        st.session_state[key] = default


def clear_session_keys():
    keys = list(st.session_state.keys())
    for key in keys:
        st.session_state.pop(key)


st.set_page_config(
    page_title="HSQDoc",
    page_icon="📃",
    layout="wide",
)

st.title("Welcome to HSQDoc!")

if st.session_state["is_login"]:
    st.subheader("Create a Conversation or Choose a Existing Conversation to Start")


class FileController:
    # 파일 임베딩 함수
    @staticmethod
    @st.cache_resource(show_spinner="Embedding file...")
    def embed_file(file):
        os.makedirs("./.cache/files", exist_ok=True)
        file_path = f"./.cache/files/{file.name}"
        with open(file_path, "wb") as f:
            f.write(file.read())

        cache_dir = LocalFileStore(f"./.cache/embeddings/open_ai/{file.name}")
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            separators=["\n\n", ".", "?", "!"],
            chunk_size=1000,
            chunk_overlap=100,
        )
        loader = UnstructuredFileLoader(file_path)
        docs = loader.load_and_split(text_splitter=splitter)
        embeddings = OpenAIEmbeddings(openai_api_key=st.session_state["api_key"])
        cached_embeddings = CacheBackedEmbeddings.from_bytes_store(
            embeddings, cache_dir
        )
        vectorstore = FAISS.from_documents(docs, cached_embeddings)
        return vectorstore.as_retriever()

    # 문서 포맷팅 함수
    @staticmethod
    def format_docs(docs):
        return "\n\n".join(document.page_content for document in docs)


# 사이드바 설정


if st.session_state["jwt"] is None:
    mode = st.selectbox("Login or Register", ["Login", "Register"])
    if mode == "Login":
        with st.form(key="login"):

            username = st.text_input(
                "Username",
            )
            password = st.text_input(
                "Password",
                type="password",
            )

            login_request = st.form_submit_button(
                "Login",
                disabled=st.session_state.is_login,
            )

            if login_request:
                login_data = {
                    "username": username,
                    "password": password,
                }
                response = requests.post(USERS_URL + "login/", json=login_data)
                if response.status_code == 200:
                    st.session_state.is_login = True
                    token = response.json()["token"]
                    st.session_state.jwt = token
                    # 로그인 후 rerun 하는걸로 form 안 보이게 하기
                    # 그대신 rerun하면 st.success가 안 보이게 된다: 생기자마자 rerun으로 사라지기 때문
                    # st.success("Welcome! You are logged in!")
                    st.rerun()
                elif response.status_code == 400:
                    error_message = response.json()["error"]
                    st.error(error_message)
    elif mode == "Register":
        with st.form(key="register", clear_on_submit=True):
            first_name = st.text_input(
                "Enter Your First Name",
            )
            last_name = st.text_input(
                "Enter Your Last Name",
            )
            email = st.text_input(
                "Enter Your Email",
            )
            gender = st.selectbox(
                "Choose Your Gender",
                ["male", "female"],
            )

            username = st.text_input(
                "Enter Your Username, This is Required",
            )
            password = st.text_input(
                "Enter Your Password, This is Required",
                type="password",
            )
            check_password = st.text_input(
                "Reenter Your Password",
                type="password",
            )
            register_request = st.form_submit_button(
                "Register",
            )
            validate_password = password == check_password
            if not validate_password:
                st.error("Password is Different")

            if register_request and validate_password:
                register_data = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "gender": gender,
                    "username": username,
                    "password": password,
                }
                response = requests.post(USERS_URL, json=register_data)
                if response.status_code == 200:
                    st.success("Register Success! Now You can LogIn")
                else:
                    if response.json()["error"]:
                        st.error(response.json()["error"])
                    else:
                        st.error("Register Fail")
else:
    conversations_data = requests.get(
        CONVERSATIONS_URL,
        headers={"jwt": st.session_state.jwt},
    )
    if conversations_data.status_code == 200:
        conversations = conversations_data.json()
        conversations_options = ["Create Conversation"]
        for conversation in conversations:
            conversations_options.append(conversation["title"])
        chosen_option = st.selectbox(
            "Create or Choose a Conversation", conversations_options
        )
        if chosen_option == "Create Conversation":
            with st.form(key="create_conversation", clear_on_submit=True):
                new_title = st.text_input(
                    "Write a Title for Your Conversation With AI",
                )
                create_conversation_request = st.form_submit_button(
                    "Create Conversation",
                )

                if create_conversation_request:
                    response = requests.post(
                        CONVERSATIONS_URL,
                        headers={"jwt": st.session_state.jwt},
                        json={
                            "title": new_title,
                        },
                    )
                    if response.status_code != 200:
                        error_message = response.json()["error"]
                        st.error(error_message)
                    else:
                        st.rerun()

        else:
            chosen_conversation_index = conversations_options.index(chosen_option) - 1
            chosen_conversation_id = conversations[int(chosen_conversation_index)]["id"]
            st.session_state["messages_url"] = (
                MESSAGES_URL + str(chosen_conversation_id) + "/"
            )
            st.session_state["conversation_url"] = (
                CONVERSATIONS_URL + str(chosen_conversation_id) + "/"
            )

            if (
                st.session_state["messages_url"]
                not in st.session_state["messages"].keys()
            ):
                st.session_state["messages"][st.session_state["messages_url"]] = []
                messages_data = requests.get(
                    st.session_state["messages_url"],
                    headers={"jwt": st.session_state.jwt},
                )
                if messages_data.status_code == 200:
                    messages = messages_data.json()
                    for message in messages:
                        ChatMemory.save_message(
                            message["message_content"],
                            message["message_role"],
                        )
                else:
                    st.error("Please Choose Proper Conversation")

    else:
        st.error("Please log in")
    with st.sidebar:
        if chosen_option != "Create Conversation":
            with st.form(key="update_or_delete_conversation", clear_on_submit=True):
                st.write("Update or Delete Conversation")
                updated_title = st.text_input("Write a New Conversation Title")
                update_request = st.form_submit_button("Update Title")
                delete_request = st.form_submit_button("Delete Conversation")

                if update_request:
                    response = requests.put(
                        st.session_state["conversation_url"],
                        headers={"jwt": st.session_state.jwt},
                        json={
                            "title": updated_title,
                        },
                    )
                    if response.status_code != 200:
                        st.error("Update Failed. Try Again")
                    else:
                        st.rerun()

                if delete_request:
                    response = requests.delete(
                        st.session_state["conversation_url"],
                        headers={"jwt": st.session_state.jwt},
                    )
                    if response.status_code != 204:
                        st.error("Delete Failed. Try Again")
                    else:
                        st.rerun()

            st.divider()
        with st.form(key="upload_file"):
            uploaded_file = st.file_uploader(
                "Upload a .txt .pdf or .docx file",
                type=["pdf", "txt", "docx"],
                # on_change=SaveEnv.save_file,
                key="file",
            )
            upload_request = st.form_submit_button("Upload file")
            if upload_request:
                # 파일을 장고에 저장
                # response = requests.put(
                #     st.session_state["conversation_url"],
                #     headers={"jwt": st.session_state.jwt},
                #     data={
                #         "file": uploaded_file,
                #     },
                # )
                # if response.status_code ==
                # print(response.status_code)
                # print(response.json())
                # print(uploaded_file.getvalue())
                print(uploaded_file._file_urls)
                # print(uploaded_file.)
            if st.session_state["file_check"]:
                st.success("😄문서가 업로드되었습니다.😄")
            else:
                st.warning("문서를 업로드해주세요.")
        st.divider()
        st.text_input(
            "API_KEY 입력",
            placeholder="sk-...",
            on_change=SaveEnv.save_api_key,
            key="api_key",
        )

        if st.session_state["api_key_check"]:
            st.success("😄API_KEY가 저장되었습니다.😄")
        else:
            st.warning("API_KEY를 넣어주세요.")

        st.button(
            "hary의 API_KEY (디버그용)",
            on_click=Debug.my_api_key,
            key="my_key_button",
        )
        st.divider()
        st.selectbox(
            "OpenAI Model을 골라주세요.",
            options=OPENAI_MODEL,
            on_change=SaveEnv.save_openai_model,
            key="openai_model",
        )

        if st.session_state["openai_model_check"]:
            st.success("😄모델이 선택되었습니다.😄")
        else:
            st.warning("모델을 선택해주세요.")
        st.divider()
        st.write(
            """
            Made by hary, seedjin298.
            
            Github
            https://github.com/lips85/Nomad_HSQDoc
            """
        )
        st.divider()
        st.write("Click to LogOut")
        logout_request = st.button(
            "LogOut",
            disabled=not st.session_state.is_login,
        )
        if logout_request:
            response = requests.post(
                USERS_URL + "logout/",
                headers={"jwt": st.session_state.jwt},
            )
            if response.status_code == 200:
                clear_session_keys()
                # 로그아웃 후 rerun -> 바로 로그인 form이 나타남
                # st.success("LogOut Success!")
                st.rerun()
            else:
                st.error("Failed to LogOut")

# 메인 로직
if (
    st.session_state["api_key_check"]
    and st.session_state["file_check"]
    and st.session_state["openai_model_check"]
):
    if chosen_option != "Create Conversation":
        llm = ChatOpenAI(
            temperature=0.1,
            streaming=True,
            callbacks=[ChatCallbackHandler()],
            model=st.session_state["openai_model"],
            openai_api_key=st.session_state["api_key"],
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """
                    You are an AI that reads documents for me. Please answer based on the document given below. 
                    If the information is not in the document, answer the question with "The required information is not in the document." Never make up answers.
                    Please answer in the questioner's language 
                    
                    Context : {context}
                    """,
                ),
                ("human", "{question}"),
            ]
        )

        retriever = (
            FileController.embed_file(st.session_state["file"])
            if st.session_state["file_check"]
            else None
        )
        if retriever:
            ChatMemory.send_message("I'm ready! Ask away!", "ai", save=False)
            ChatMemory.paint_history()
            message = st.chat_input("Ask anything about your file...")

            if message:
                if re.match(API_KEY_PATTERN, st.session_state["api_key"]) and re.match(
                    MODEL_PATTERN, st.session_state["openai_model"]
                ):
                    ChatMemory.send_message(message, "human")
                    chain = (
                        {
                            "context": retriever
                            | RunnableLambda(FileController.format_docs),
                            "question": RunnablePassthrough(),
                        }
                        | prompt
                        | llm
                    )
                    try:
                        with st.chat_message("ai"):
                            ai_answer = chain.invoke(message)
                            ChatMemory.save_message_db(ai_answer.content, "ai")
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
                        st.warning("OPENAI_API_KEY or 모델 선택을 다시 진행해주세요.")
                else:
                    ChatMemory.send_message(
                        "OPENAI_API_KEY or 모델 선택이 잘못되었습니다. 사이드바를 다시 확인하세요.",
                        "ai",
                    )
        else:
            st.session_state["messages"] = []
