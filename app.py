import streamlit as st
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT")
st.title("💬 DelGPT — AI-powered Kashmiri")

user_input = st.text_input("You:", key="input")

if user_input:
    try:
        prompt = get_del_prompt(user_input)
        response = get_gemini_response(prompt)
        st.markdown(f"**DelGPT**: {response}")
    except Exception as e:
        st.error("❌ Error occurred:")
        st.code(str(e), language="python")
