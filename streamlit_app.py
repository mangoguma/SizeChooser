import streamlit as st
from ux_writer import UXwriter
import pandas as pd
import json
from st_copy_to_clipboard import st_copy_to_clipboard


def boolean_to_emoji(value):
    return '✅' if value else '❌'


st.title("✍🏻 UX writer")
st.write(
    "SqueezeBits의 UX writer입니다."
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
col1, col2 = st.columns(2, vertical_alignment="bottom")
with col1:
    option = st.selectbox(
        "UX 라이팅 매뉴얼을 선택하세요",
        ["select", "Toss", "Squeezebits"],
        index=0
    )
with col2:
    is_English = st.toggle("Always answer in English")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")

elif option == "select":
    st.info("Please select your manual to continue.", icon="🧾")

else:
    if option == "Toss":
        from toss import TOSS
        writer = UXwriter(openai_api_key, TOSS, is_English)
    else:
        from sqzb import SQZB
        writer = UXwriter(openai_api_key, SQZB, is_English)

    # Text input
    txt_input = st.text_area('Enter your text', '', height=200)

    submitted = st.button('Check')

    if submitted and openai_api_key.startswith('sk-'):
        score1, score2 = st.columns(2)
        with st.spinner('Calculating...'):
            score = writer.get_score(txt_input)
            
            score_data = json.loads(score)
            core_values = score_data["Core_Values"]
            emoji_values = {k: boolean_to_emoji(v) for k, v in core_values.items()}

            df = pd.DataFrame([emoji_values])
            df.index = ['']

            split_index = (len(df.columns)+1) // 2
            with score1:
                st.table(df.iloc[:, :split_index].T)
            with score2:
                st.table(df.iloc[:,split_index:].T)

        with st.spinner('Generating...'):
            result = writer.edit(txt_input, score)
            st.info(result)
            st_copy_to_clipboard(result)