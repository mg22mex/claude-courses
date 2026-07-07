import streamlit as st
import requests
import openai  # Used as the client interface for DeepSeek/OpenClaude API keys
import os      # Added to safely read environment variables inside the Hugging Face Docker container

st.set_page_config(page_title="Weatherman Claude Portal", layout="wide")

# --- Configuration & Secrets ---
# FIX: Using os.environ.get ensures Hugging Face picks up your DEEPSEEK_API_KEY flawlessly
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY")
GITHUB_RAW_URL = "https://raw.githubusercontent.com/mg22mex/claude-courses/main/training"

st.title("⚡ Weatherman AI Portal")
st.caption("Zero-install enterprise workspace backed by DeepSeek & OpenClaude")

# --- Sidebar Team Picker ---
st.sidebar.header("Workspace Settings")
user = st.sidebar.selectbox(
    "Who is logging in today?",
    ["Select Name", "Rick", "Sunny", "Christine", "Mollie", "Paula & Gabby"]
)

# Map UI names to your repository directory folders
folder_map = {
    "Rick": "rick",
    "Sunny": "sunny",
    "Christine": "christine",
    "Mollie": "mollie",
    "Paula & Gabby": "design"
}

if user != "Select Name":
    dept_folder = folder_map[user]
    
    # Model Router adapted for DeepSeek execution engine setups
    model_choice = st.sidebar.radio("Select AI Engine", ["DeepSeek (Data/Logic)", "OpenClaude (Creative/Copy)"])
    
    # Dynamically fetch the system preset from your GitHub repo
    with st.spinner("Loading your personalized workspace preset..."):
        try:
            # Assumes the preset instruction file lives at: training/{dept}/presets/SYSTEM_PROMPT.md
            response = requests.get(f"{GITHUB_RAW_URL}/{dept_folder}/presets/SYSTEM_PROMPT.md")
            system_prompt = response.text if response.status_code == 200 else "You are a helpful assistant for Weatherman."
        except Exception:
            system_prompt = "You are a helpful assistant for Weatherman."
            
    st.sidebar.success(f"{user}'s Profile Loaded Active!")
    
    # --- File Uploader ---
    uploaded_file = st.file_uploader("Attach operational data sheets (.xlsx, .csv, .pdf)", type=["xlsx", "csv", "pdf"])
    file_context = ""
    if uploaded_file is not None:
        st.info(f"📎 Attached: {uploaded_file.name}")
        # Simple text representation for prototype testing
        file_context = f"\n\n[Attached File Content from {uploaded_file.name}]:\n" + str(uploaded_file.read())

    # --- Chat Interface ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask a question, run a baseline template, or analyze data..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Build payload combining system instructions, attached context files, and the user prompt
        full_user_content = prompt + file_context if file_context else prompt
        
        # Point both setups to DeepSeek Base URL using the environment variable key
        client = openai.OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com/v1")
        
        if model_choice == "DeepSeek (Data/Logic)":
            target_model = "deepseek-reasoner"  # Deep-thinking R1 architecture
        else:
            target_model = "deepseek-chat"      # Fast, standard V3 chat model

        with st.chat_message("assistant"):
            response_stream = client.chat.completions.create(
                model=target_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_user_content}
                ],
                stream=False
            )
            ai_response = response_stream.choices[0].message.content
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
else:
    st.warning("Please select your name in the sidebar to activate your custom prompt presets.")