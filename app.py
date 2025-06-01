import streamlit as st
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT")
st.title("💬 DelGPT — Your Tech Bro with Attitude")

# Optional: Top avatar
st.image("del_avatar.png", width=100, caption="Del (aka Vinayak)")

# Init session history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"👤 **You**: {msg['content']}")
    else:
        col1, col2 = st.columns([1, 9])
        with col1:
            st.image("del_avatar.png", width=40)
        with col2:
            st.markdown(f"**DelGPT**: {msg['content']}")

# Input box
user_input = st.text_input("You:", key="input", placeholder="Ask something...")

if user_input:
    prompt = get_del_prompt(user_input)
    try:
        response = get_gemini_response(prompt)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "bot", "content": response})

        st.experimental_rerun()

    except Exception as e:
        st.error("❌ Error occurred:")
        st.code(str(e), language="python")
