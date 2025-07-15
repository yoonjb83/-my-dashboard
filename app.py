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

uploaded_file = st.file_uploader("엑셀 파일 업로드", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file, header=1)
    os.makedirs("data", exist_ok=True)
    with open("data/data.xlsx", "wb") as f:
        f.write(uploaded_file.read())
elif os.path.exists("data/data.xlsx"):
    df = pd.read_excel("data/data.xlsx")
else:
    st.info("엑셀 파일을 업로드해주세요")
    st.stop()

st.subheader("데이터 미리보기")
st.dataframe(df)

numerical_cols = df.select_dtypes(include='number').columns
if len(numerical_cols) > 0:
    col = st.selectbox("그래프로 볼 컬럼 선택", numerical_cols)
    fig = px.line(df, y=col, title=f"{col} 변화 추이")
    st.plotly_chart(fig)
else:
    st.warning("숫자형 데이터가 없습니다.")
