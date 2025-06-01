import streamlit as st
import time
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT — AI Powered Kashmiri", layout="centered")

# ----------- CSS: Hide Streamlit assistant avatar + theme fix ----------- #
st.markdown("""
    <style>
    [data-testid="stChatMessage"] img {
        display: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------ SESSION STATE INIT ------------------ #
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Bol kya chahiye bhai 👇 (but make it quick, I'm busy af)"}
    ]
if "is_del" not in st.session_state:
    st.session_state.is_del = False

# ------------------ DETECT "I am Del" ------------------ #
def detect_del_identity(text):
    text = text.lower()
    return "del" in text and any(phrase in text for phrase in ["i am", "i'm", "me", "mai", "main"])

# ------------------ APPLY WHITE THEME ------------------ #
if st.session_state.is_del:
    st.markdown("""
        <style>
        .stApp {
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        .stChatMessage, .stTextInput, .stTextArea {
            border: 1px solid #222 !important;
            border-radius: 6px;
        }
        .css-1cpxqw2, .stTextInput>div>div>input {
            background-color: #f6f6f6 !important;
            color: black !important;
            border: 1px solid #222 !important;
        }
        </style>
    """, unsafe_allow_html=True)

# ------------------ HEADER ------------------ #
st.markdown("## 🧠 DelGPT — AI Powered Kashmiri Engineer")
st.caption("Built on Gemini. Expect Hinglish, sarcasm, tech gyaan, and mood swings.")

# ------------------ SHOW CHAT HISTORY ------------------ #
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            st.markdown(f"""
                <div style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px;">
                    <img src="del_avatar.png" style="width: 40px; height: 40px; border-radius: 50%;" />
                    <div style="flex: 1;">{msg["content"]}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(msg["content"])

# ------------------ USER INPUT ------------------ #
if user_input := st.chat_input("Message DelGPT..."):

    # Check for identity claim
    if not st.session_state.is_del and detect_del_identity(user_input):
        st.session_state.is_del = True

    # Display + save user message
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Construct prompt
    prompt = get_del_prompt(user_input)

    # Show DelGPT response
    with st.chat_message("assistant"):
        st.markdown("""
            <div style="display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px;">
                <img src="del_avatar.png" style="width: 40px; height: 40px; border-radius: 50%;" />
                <div id="del-output" style="flex: 1;">
        """, unsafe_allow_html=True)

        message_placeholder = st.empty()
        full_response = ""

        try:
            del_response = get_gemini_response(prompt)
        except Exception as e:
            del_response = f"❌ Error aagya bhai — {str(e)}"

        for word in del_response.split():
            full_response += word + " "
            time.sleep(0.03)
            message_placeholder.markdown(full_response + "▌")

        message_placeholder.markdown(full_response)
        st.markdown("</div></div>", unsafe_allow_html=True)

    st.session_state.messages.append({"role": "assistant", "content": full_response})
