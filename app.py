import streamlit as st
import time
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT — AI Powered Kashmiri", layout="centered")

st.markdown("## 🧠 DelGPT — AI Powered Kashmiri Engineer")
st.caption("Streamlit chat powered by Gemini 2.0 Flash. Expect sarcasm, Hinglish, and serious backend energy.")

# Init session
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bol kya chahiye bhai 👇 (but make it quick, I'm busy af)"}
    ]
if "is_del" not in st.session_state:
    st.session_state.is_del = False

# Show message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input handler
if user_input := st.chat_input("Ask something tech... or try your luck 🤔"):
    # Check if user claimed to be Del
    if not st.session_state.is_del and any(
        trigger in user_input.lower()
        for trigger in ["i am del", "i'm del", "main del hoon", "me del", "mai del"]
    ):
        st.session_state.is_del = True
        with st.chat_message("assistant"):
            st.markdown("Acha tu Del hai? Then shut down and restart the server bsdk.")

    # Append user msg
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Prepare DelGPT response
    prompt = get_del_prompt(user_input)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        try:
            del_response = get_gemini_response(prompt)
        except Exception as e:
            del_response = "Kuch error aagya bhai, khud dekh le logs mein. " + str(e)

        # Simulate typing effect
        for word in del_response.split():
            full_response += word + " "
            time.sleep(0.04)
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)

    # Save assistant response
    st.session_state.messages.append({"role": "assistant", "content": full_response})
