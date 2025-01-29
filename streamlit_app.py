import streamlit as st
from user import User
from ux_writer import TopSizeChooser, LowerSizeChooser
import pandas as pd

openai_api_key = st.text_input("OpenAI API Key", type="password")
st.title("👕 Size chooser")
st.write(
    "옷 사이즈를 골라드려요!"
)

age = st.number_input("나이를 입력하세요", min_value=0, value=40)
body_shape = st.selectbox("자신과 가까운 체형을 선택하세요", options=["슬림", "평균", "듬직", "근육질"])
user_height = st.number_input("키를 입력하세요 (cm)", min_value=0, value=170)
user_weight = st.number_input("몸무게를 입력하세요 (kg)", min_value=0, value=70)
upper_size = st.select_slider("평소 입는 상의 사이즈를 선택하세요", options=["85", "90", "95", "100", "105", "110", "115"])
lower_size = st.select_slider("평소 입는 하의 사이즈를 선택하세요", options=["25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36"])
gender = st.radio("성별을 선택하세요", options=["남", "여"])

user = User(age=age, height=user_height, weight=user_weight, gender=gender, upper_size=upper_size, lower_size=lower_size, body_shape=body_shape)


col1, col2 = st.columns(2, vertical_alignment="bottom")
with col1:
    category = st.selectbox(
        "카테고리를 선택하세요",
        ["상의", "하의", "아우터"],
        index=0
    )
with col2:
    product_url = st.text_input("상품 링크를 입력하세요", "")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")

else:
    if category == "상의":
        chooser = TopSizeChooser(openai_api_key)
    elif category == "하의":
        chooser = LowerSizeChooser(openai_api_key)
    else:
        st.error("준비 중인 기능입니다.")

    # Text input
    txt_input = st.text_area('Enter your text', '', height=200)

    submitted = st.button('Check')

    if submitted and openai_api_key.startswith('sk-'):
        score1, score2 = st.columns(2)
        with st.spinner('Get size information...'):
            size_info = chooser.get_size_info(product_url)
            df = pd.DataFrame([size_info])
            st.table(df)

        with st.spinner('Choose size...'):
            result = chooser.choose_size(user, size_info)
            st.info(result)