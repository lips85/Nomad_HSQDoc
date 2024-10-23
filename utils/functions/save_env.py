import re
import requests
import streamlit as st
from utils.constant.constant import API_KEY_PATTERN

USER_PROFILE_URL = "http://127.0.0.1:8000/api/v1/users/profile/"


class SaveEnv:
    @staticmethod
    def save_api_key():
        st.session_state["api_key_check"] = bool(
            re.match(API_KEY_PATTERN, st.session_state["api_key"])
        )
        if st.session_state["api_key_check"]:
            response = requests.put(
                USER_PROFILE_URL,
                headers={"jwt": st.session_state.jwt},
                json={
                    "api_key": st.session_state["api_key"],
                },
            )
            print(response)
            if response.status_code == 200:
                print("success")

    @staticmethod
    def save_file():
        st.session_state["file_check"] = st.session_state.file is not None

    @staticmethod
    def save_openai_model():
        st.session_state["openai_model_check"] = (
            st.session_state["openai_model"] != "선택해주세요"
        )

    @staticmethod
    def save_url():
        if st.session_state["url"]:
            st.session_state["url_check"] = True
            st.session_state["url_name"] = (
                st.session_state["url"].split("://")[1].replace("/", "_")
            )
        else:
            st.session_state["url_check"] = False
            st.session_state["url_name"] = None
