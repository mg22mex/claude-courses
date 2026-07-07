import streamlit as st
import requests
import openai  # Used as the client interface for DeepSeek/OpenClaude API keys
import os      # Added to safely read environment variables inside the Hugging Face Docker container

st.set_page_config(page_title="Weatherman Claude Portal", layout="wide")

# --- Configuration & Secrets ---
DEEPSEEK_KEY = os.environ.get("DEEPSEEK_API_KEY")
GITHUB_RAW_URL = "https://raw.githubusercontent.com/mg22mex/claude-courses/main"

st.title("⚡ Weatherman AI Portal")
st.caption("Zero-install enterprise workspace backed by DeepSeek & OpenClaude")

# --- Sidebar Team & Preset Picker ---
st.sidebar.header("Workspace Settings")

# Included General / Master Guide at the top
user = st.sidebar.selectbox(
    "Who is logging in today?",
    ["Select Name", "General / Master Guide", "Rick", "Sunny", "Christine", "Mollie", "Paula & Gabby"]
)

# Map UI names to repository directory paths
folder_map = {
    "General / Master Guide": "", # Root directory
    "Rick": "training/rick",
    "Sunny": "training/sunny",
    "Christine": "training/christine",
    "Mollie": "training/mollie",
    "Paula & Gabby": "training/design"
}

# Map available workspace task presets to each track
preset_map = {
    "General / Master Guide": ["global-onboarding", "portal-flight-manual-lookup"],
    "Rick": ["fulfillment-anomaly-detector", "write-a-prd", "ppt-generation", "architecture-diagram"],
    "Sunny": ["lead-time-anomaly", "customs-tariff-audit", "warehouse-balancing", "xlsx-processing", "data-table-validator"],
    "Mollie": ["csv-analytics", "monte-carlo-analyze-root-cause", "reconciliation-engine", "anomaly-alert-webhook"],
    "Christine": ["brand-guardrails", "email-automation", "listing-verification", "campaign-analytics"],
    "Paula & Gabby": ["svg-auditor", "design-token-validator", "component-spec-compiler", "asset-pack-optimizer"]
}

if user != "Select Name":
    dept_path = folder_map[user]
    
    # Model Router
    model_choice = st.sidebar.radio("Select AI Engine", ["DeepSeek (Data/Logic)", "OpenClaude (Creative/Copy)"])
    
    # Dynamic Secondary Sub-Preset Dropdown Selection
    selected_preset = st.sidebar.selectbox("Select Workspace Preset Task", preset_map[user])
    
    # Dynamically fetch system context from GitHub repo
    with st.spinner("Loading your personalized workspace preset..."):
        try:
            # Construct the file path dynamically based on whether it's root or a department folder
            if dept_path == "":
                master_prompt_url = f"{GITHUB_RAW_URL}/SYSTEM_PROMPT.md"
                preset_prompt_url = f"{GITHUB_RAW_URL}/training/general/presets/{selected_preset}/instructions.md" # Fallback/future structure placeholder
            else:
                master_prompt_url = f"{GITHUB_RAW_URL}/{dept_path}/presets/SYSTEM_PROMPT.md"
                preset_prompt_url = f"{GITHUB_RAW_URL}/{dept_path}/presets/{selected_preset}/instructions.md"

            # Fetch Master Role Profile
            master_resp = requests.get(master_prompt_url)
            master_prompt = master_resp.text if master_resp.status_code == 200 else "You are a helpful assistant for Weatherman."
            
            # Fetch Specific Task Instructions if they exist
            preset_resp = requests.get(preset_prompt_url)
            preset_instructions = preset_resp.text if preset_resp.status_code == 200 else f"Execute operational task: {selected_preset}."
            
            # Combine master persona with specific task directives
            system_prompt = f"{master_prompt}\n\n## Active Task Directives\n{preset_instructions}"
            
        except Exception:
            system_prompt = "You are a helpful assistant for Weatherman."
            
    st.sidebar.success(f"{user}'s Profile & Preset Loaded!")
    
    # --- File Uploader ---
    uploaded_file = st.file_uploader("Attach operational data sheets (.xlsx, .csv, .pdf)", type=["xlsx", "csv", "pdf"])
    file_context = ""
    if uploaded_file is not None:
        st.info(f"📎 Attached: {uploaded_file.name}")
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
        
        # Initialize client pointing to DeepSeek Endpoint
        client = openai.OpenAI(api_key=DEEPSEEK_KEY, base_url="https://api.deepseek.com/v1")
        
        if model_choice == "DeepSeek (Data/Logic)":
            target_model = "deepseek-reasoner"  # Deep-thinking R1 architecture
        else:
            target_model = "deepseek-chat"      # Fast, standard V3 chat model

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            
            # Enabled streaming for smoother output generation
            response_stream = client.chat.completions.create(
                model=target_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_user_content}
                ],
                stream=True
            )
            
            full_response = ""
            for chunk in response_stream:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    response_placeholder.markdown(full_response + "▌")
            
            response_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
else:
    st.warning("Please select your name in the sidebar to activate your custom prompt presets.")