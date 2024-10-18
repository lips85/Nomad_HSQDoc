import streamlit as st
import requests

URL = "http://127.0.0.1:8000/api/v1/users/"

# jwt token을 담기 위한 session state
if "jwt" not in st.session_state:
    st.session_state.jwt = None

# 로그인 했는지를 나타내는 session state
if "is_login" not in st.session_state:
    st.session_state.is_login = False

st.set_page_config(
    page_title="HSQDoc",
)

st.title("Welcome to HSQDoc!")

st.subheader("Login to use HSQDoc")


# def erase_jwt_token():
#     st.session_state.jwt = None


# def change_to_login():
#     st.session_state.is_login = True


# def change_to_logout():
#     st.session_state.is_login = False
#     erase_jwt_token()


mode = st.selectbox("Login or Register", ["Login", "Register"])

if not st.session_state["jwt"]:
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
                response = requests.post(URL + "login/", json=login_data)
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
    else:
        with st.form(key="register"):
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
                response = requests.post(URL, json=register_data)
                if response.status_code == 200:
                    st.success("Register Success! Now You can LogIn")
                else:
                    if response.json()["error"]:
                        st.error(response.json()["error"])
                    else:
                        st.error("Register Fail")
else:
    st.write("You are already logged in!")
    st.write("Click to LogOut")
    logout_request = st.button(
        "LogOut",
        disabled=not st.session_state.is_login,
    )
    if logout_request:
        response = requests.post(
            URL + "logout/",
            headers={"jwt": st.session_state.jwt},
        )
        if response.status_code == 200:
            st.session_state.is_login = False
            st.session_state.jwt = None
            # 로그아웃 후 rerun -> 바로 로그인 form이 나타남
            # st.success("LogOut Success!")
            st.rerun()
        else:
            st.error("Failed to LogOut")
