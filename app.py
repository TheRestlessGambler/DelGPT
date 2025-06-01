import streamlit as st
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT", layout="centered")
st.title("💬 DelGPT — Your Tech Bro with Attitude")

# Optional top avatar
st.image("del_avatar.png", width=100, caption="Del (Vinayak)")

# Chat container styling
st.markdown("""
    <style>
    .chat-container {
        max-height: 550px;
        overflow-y: auto;
        padding-right: 10px;
        margin-bottom: 20px;
    }
    .msg-block {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 1rem;
    }
    .msg-text {
        background-color: #f1f3f6;
        padding: 0.75rem 1rem;
        border-radius: 1rem;
        max-width: 75%;
        font-size: 0.95rem;
    }
    .bot {
        background-color: #e0ecff;
    }
    .avatar {
        border-radius: 50%;
        width: 40px;
        height: 40px;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

# Init session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Optional: Clear chat
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.experimental_rerun()

# Chat history
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    role = msg["role"]
    content = msg["content"]

    if role == "user":
        st.markdown(f"""
            <div class="msg-block">
                <img src="https://avatars.githubusercontent.com/u/1" class="avatar"/>
                <div class="msg-text">{content}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div class="msg-block">
                <img src="del_avatar.png" class="avatar"/>
                <div class="msg-text bot">{content}</div>
            </div>
        """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# User input
user_input = st.text_input("You:", key="input", placeholder="Type a message and press Enter...")

if user_input:
    try:
        prompt = get_del_prompt(user_input)
        response = get_gemini_response(prompt)

        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "bot", "content": response})

        st.experimental_rerun()

    except Exception as e:
        st.error("❌ Error occurred:")
        st.code(str(e), language="python")
