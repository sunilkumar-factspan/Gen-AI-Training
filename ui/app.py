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

    # --- STEP 1: INITIAL GENERATION ---
    with st.spinner("Generating initial code..."):
        response = generate_code(user_input, st.session_state.history)
    
    code = extract_code(response)
    
    # Standard Validation
    if not code or not is_valid_python(code)[0] or not is_safe_code(code):
        st.error("Generated code failed validation ❌")
        st.stop()

    st.code(code, language="python")
    st.info("Running automation...")

    # --- STEP 2: FIRST EXECUTION ---
    result = execute_code(code)

    # --- STEP 3: SELF-HEALING (RETRY LOGIC) ---
    if not result["success"]:
        st.warning("⚠️ Test failed. Attempting Self-Healing...")
        
        # ui/app.py (Inside Step 3: Self-Healing)
        healing_prompt = f"""
        The previous code for the task: '{user_input}' failed with error: {result['stderr']}

        STRICT INSTRUCTIONS:
        1. Stay focused ONLY on the website requested: {user_input}.
        2. Do NOT use selectors for other websites (like Flipkart or GitHub) unless they were explicitly requested.
        3. The search input on Google is typically page.locator("textarea[name='q']").
        4. Fix the error while following all original STEALTH and sync_api rules.
        """

        with st.spinner("Analyzing error and healing code..."):
            # Request a fix from the LLM
            healed_response = generate_code(healing_prompt, st.session_state.history)
            healed_code = extract_code(healed_response)

        if healed_code and is_valid_python(healed_code)[0] and is_safe_code(healed_code):
            # FIXED: Removed 'label' argument to prevent TypeError
            st.markdown("### ✨ Healed Code")
            st.code(healed_code, language="python")
            st.info("Running healed automation...")
            
            # Re-execute with the new code
            result = execute_code(healed_code)
            code = healed_code  # Update code for history
        else:
            st.error("Could not generate a safe/valid healed script.")

    # --- STEP 4: FINAL RESULTS ---
    if result["success"]:
        st.success("Test Passed ✅")
        if os.path.exists("output.png"):
            st.image("output.png")
            with open("output.png", "rb") as file:
                st.download_button(
                    label="Download Screenshot",
                    data=file,
                    file_name=f"test_report_{user_input[:10].replace(' ', '_')}.png",
                    mime="image/png"
                )
    else:
        st.error("Test Failed ❌")
        st.code(result["stderr"])

    # Update history with the final version of the code (initial or healed)
    st.session_state.history.append({
        "user": user_input,
        "assistant": code
    })