import streamlit as st
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT")

# Initialize states
if "messages" not in st.session_state:
    st.session_state.messages = []
if "is_del" not in st.session_state:
    st.session_state.is_del = False
if "input" not in st.session_state:
    st.session_state.input = ""

# Check trigger phrase to activate white mode
def check_if_del(text):
    triggers = ["i am del", "i'm del", "main del hoon", "me del", "mai del"]
    return any(trigger in text.lower() for trigger in triggers)

# Theme override if Del mode is on
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

st.title("💬 DelGPT — Your Kashmiri AI-powered Assistant")

# Clear chat
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.input = ""
    st.rerun()

# Show chat
for msg in st.session_state.messages:
    name = "You" if msg["role"] == "user" else "DelGPT"
    st.markdown(f"**{name}:** {msg['content']}")

# Input box
user_input = st.text_input("Message DelGPT:", key="input")

# Handle input once only
if user_input and st.session_state.input != user_input:
    st.session_state.input = user_input  # Store to avoid rerun loop

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
