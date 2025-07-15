import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

# 로그인 정보 로드
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def login(username, password):
    users = load_users()
    return users.get(username) == password

# 로그인 UI
st.sidebar.title("로그인")
username = st.sidebar.text_input("아이디")
password = st.sidebar.text_input("비밀번호", type="password")
login_button = st.sidebar.button("로그인")

if login_button:
    if login(username, password):
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
    else:
        st.error("로그인 실패")

if not st.session_state.get("logged_in", False):
    st.warning("로그인 후 이용해주세요")
    st.stop()

st.title("📊 통계 대시보드")

# 엑셀 파일 업로드 또는 기존 파일 불러오기
uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, header=1)
        os.makedirs("data", exist_ok=True)
        with open("data/data.xlsx", "wb") as f:
            f.write(uploaded_file.read())
    except Exception as e:
        st.error(f"엑셀 파일을 읽는 도중 오류가 발생했습니다: {e}")
        st.stop()

elif os.path.exists("data/data.xlsx"):
    try:
        df = pd.read_excel("data/data.xlsx", header=1)
    except Exception as e:
        st.error("기존 data.xlsx 파일을
