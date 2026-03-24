import os
import streamlit as st

from llm.llm import generate_code
from utils.code_utils import extract_code
from utils.validator import is_valid_python
from utils.safety import is_safe_code
from playwright.runner import execute_code

st.title("🤖 Playwright AI Agent")

# Debug check
st.write("App started ✅")

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# Show history
for chat in st.session_state.history:
    st.chat_message("user").write(chat["user"])
    st.chat_message("assistant").code(chat["assistant"], language="python")

# Input
user_input = st.chat_input("Enter your automation task...")

if user_input:
    st.chat_message("user").write(user_input)

    with st.spinner("Generating code..."):
        response = generate_code(user_input, st.session_state.history)

    code = extract_code(response)

    if not code:
        st.error("No valid code ❌")
        st.stop()

    valid, error = is_valid_python(code)
    if not valid:
        st.error(f"Invalid code ❌\n{error}")
        st.stop()

    if not is_safe_code(code):
        st.error("Unsafe code ❌")
        st.stop()

    st.code(code, language="python")

    st.info("Running automation...")

    result = execute_code(code)

    if result["success"]:
        st.success("Test Passed ✅")

        if os.path.exists("output.png"):
            st.image("output.png")

    else:
        st.error("Test Failed ❌")
        st.code(result["stderr"])

    st.session_state.history.append({
        "user": user_input,
        "assistant": code
    })