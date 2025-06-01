import streamlit as st
from gemini_api import get_gemini_response
from del_persona import get_del_prompt

st.set_page_config(page_title="DelGPT")

# Check if user is Del
if "is_del" not in st.session_state:
    st.session_state.is_del = None

if st.session_state.is_del is None:
    st.subheader("Are you Del?")
    if st.button("Yes, I'm Del"):
        st.session_state.is_del = True
    elif st.button("No, I'm not Del"):
        st.session_state.is_del = False
    st.stop()

# Set theme based on identity
if st.session_state.is_del:
    st.markdown("""
        <style>
        body, .stApp {
            background-color: white !important;
            color: black !important;
        }
        </style>
    """, unsafe_allow_html=True)

st.title("💬 DelGPT — Your Tech Bro with Attitude")

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Clear chat button
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.rerun()


# Display chat history
for msg in st.session_state.messages:
    role = msg["role"]
    name = "You" if role == "user" else "DelGPT"
    st.markdown(f"**{name}:** {msg['content']}")

# Text input
user_input = st.text_input("Message DelGPT:", key="input")

if user_input:
    try:
        prompt = get_del_prompt(user_input)
        response = get_gemini_response(prompt)

        # Store chat
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.session_state.messages.append({"role": "bot", "content": response})

        st.rerun()


    except Exception as e:
        st.error("❌ Error occurred:")
        st.code(str(e), language="python")
