import streamlit as st
import time
import os
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT — AI Powered Kashmiri", layout="centered")

# Session State
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bol kya chahiye bhai 👇 (but make it quick, I'm busy af)"}]
if "is_del" not in st.session_state:
    st.session_state.is_del = False

# Identity Detection
def detect_del_identity(text):
    text = text.lower()
    return "del" in text and any(x in text for x in ["i am", "i'm", "mai", "main", "me"])

# Apply White Theme
if st.session_state.is_del:
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# Header
st.markdown("## 🧠 DelGPT — AI Powered Kashmiri Engineer")
st.caption("Built on Gemini. Expect Hinglish, sarcasm, tech gyaan, and mood swings.")

# Show past messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        content = msg["content"]
        if "```" in content:
            parts = content.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part.strip():
                        st.markdown(part.strip())
                else:
                    lang = ""
                    if part.strip().startswith(("python", "js", "javascript", "html", "bash")):
                        lang, code = part.strip().split("\n", 1)
                        st.code(code, language=lang.strip())
                    else:
                        st.code(part.strip())
        else:
            st.markdown(content)

# Chat input
if user_input := st.chat_input("Message DelGPT..."):

    if not st.session_state.is_del and detect_del_identity(user_input):
        st.session_state.is_del = True

    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Build conversation context
    conversation = ""
    for msg in st.session_state.messages:
        role = "User" if msg["role"] == "user" else "Del"
        conversation += f"{role}: {msg['content']}\n"

    prompt = get_del_prompt(conversation)

    # Assistant response
    with st.chat_message("assistant"):
        container = st.container()
        typing_response = ""
        full_response = ""

        try:
            del_response = get_gemini_response(prompt)

            if ("def " in del_response or "print(" in del_response) and "```" not in del_response:
                del_response = f"```python\n{del_response.strip()}\n```"

        except Exception as e:
            del_response = f"❌ Error aagya bhai — {str(e)}"

        for char in del_response:
            typing_response += char
            time.sleep(0.005)
            container.markdown(typing_response + "▌")

        container.empty()  # Clear the temporary animated text

        # Final render — persistent
        if "```" in del_response:
            parts = del_response.split("```")
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    if part.strip():
                        container.markdown(part.strip())
                else:
                    lang = ""
                    if part.strip().startswith(("python", "js", "javascript", "html", "bash")):
                        lang, code = part.strip().split("\n", 1)
                        container.code(code, language=lang.strip())
                    else:
                        container.code(part.strip())
        else:
            container.markdown(del_response)

    st.session_state.messages.append({"role": "assistant", "content": del_response})
