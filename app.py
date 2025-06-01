import streamlit as st
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT")

# Initialize states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_del" not in st.session_state:
    st.session_state.is_del = False

# Light mode theme if user says "I'm Del"
def check_if_del(text):
    triggers = ["i am del", "i'm del", "main del hoon", "me del", "mai del"]
    return any(trigger in text.lower() for trigger in triggers)

# Apply white theme if del
if st.session_state.is_del:
    st.markdown("""
        <style>
        .stApp {
            background-color: white !important;
            color: black !important;
        }
        input, textarea {
            background-color: white !important;
            color: black !important;
        }
        .css-1cpxqw2 {
            background-color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("💬 DelGPT — Your Tech Bro with Attitude")

# Clear button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []

# Chat history
for msg in st.session_state.messages:
    name = "You" if msg["role"] == "user" else "DelGPT"
    st.markdown(f"**{name}:** {msg['content']}")

# Input
user_input = st.text_input("Message DelGPT:", key="input")

if user_input:
    if check_if_del(user_input):
        st.session_state.is_del = True

    try:
        prompt = get_del_prompt(user_input)
        response = get_gemini_response(prompt)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "bot", "content": response})

        st.rerun()

    except Exception as e:
        st.error("❌ Error occurred:")
        st.code(str(e), language="python")
