import streamlit as st
import os
import time
from sandbox.container_mgr import Sandbox
from agent.graph import build_graph

# --- 1. CONFIGURATION & THEME ---
st.set_page_config(
    page_title="GitFix | AI Auto-Debugger",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. ADVANCED CSS (The "Pro" Look) ---
st.markdown("""
<style>
    /* IMPORT FONT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* BACKGROUND GRADIENT */
    .stApp {
        background: linear-gradient(to bottom right, #0e1117, #151922);
        color: #e0e0e0;
    }

    /* CARD STYLING (Glassmorphism) */
    .css-1r6slb0, .stExpander, .stCodeBlock, .stStatus {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }

    /* BUTTON STYLING */
    div.stButton > button {
        background: linear-gradient(90deg, #00C853 0%, #69F0AE 100%);
        color: #003300;
        border: none;
        padding: 0.6rem 2rem;
        font-weight: 800;
        font-size: 16px;
        border-radius: 8px;
        transition: transform 0.2s;
        width: 100%;
    }
    div.stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(0, 200, 83, 0.4);
    }

    /* METRIC CARDS */
    div[data-testid="metric-container"] {
        background-color: #1E232B;
        border: 1px solid #2E3642;
        padding: 10px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER SECTION ---
col_logo, col_title = st.columns([1, 6])
with col_logo:
    # Robot Icon
    st.image("https://cdn-icons-png.flaticon.com/512/9311/9311508.png", width=85)
with col_title:
    st.markdown("<h1 style='margin-bottom:0; color:#00E676;'>GitFix AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:18px; color:#888;'>Autonomous Self-Healing Code Infrastructure</p>", unsafe_allow_html=True)

st.divider()

# --- 4. SIDEBAR (Smart Status Panel) ---
with st.sidebar:
    st.markdown("### 🔌 System Status")
    
    # Initialize Sandbox (Hybrid Check)
    @st.cache_resource
    def get_sandbox():
        box = Sandbox()
        if box.is_active:
            box.build_and_start()
        return box

    sandbox = get_sandbox()

    if sandbox.is_active:
        # LOCAL DOCKER MODE
        st.success("Docker Engine: **ONLINE**")
        st.metric(label="Execution Mode", value="🐳 Real Sandbox", delta="Secure")
    else:
        # CLOUD SIMULATION MODE
        st.warning("Docker Engine: **OFFLINE**")
        st.metric(label="Execution Mode", value="☁️ Cloud Sim", delta="Demo Only")
        st.info("Running in Cloud Simulation Mode. (Real execution requires local Docker).")
        
    st.divider()
    st.markdown("### 🛠️ Configuration")
    model_type = st.selectbox("AI Model", ["GPT-4o (GitHub)", "GPT-3.5 Turbo"], index=0)
    st.caption(f"v1.2.0 | { 'Local' if sandbox.is_active else 'Cloud' } Build")

# --- 5. MAIN WORKSPACE ---

# Top Metrics Row
m1, m2, m3 = st.columns(3)
m1.metric("Agent Status", "Idle", delta_color="off")
m2.metric("Files Queued", "0")
m3.metric("Success Rate", "100%")

st.markdown("### 📂 Project Workspace")

uploaded_file = st.file_uploader("", type="py", help="Upload broken python script")

if uploaded_file:
    # SAVE FILE LOCALLY
    file_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # READ CONTENT
    with open(file_path, "r") as f:
        original_code = f.read()

    # CODE PREVIEW AREA
    with st.expander("📄 View Source Code", expanded=True):
        st.code(original_code, language="python", line_numbers=True)

    # ACTION AREA
    st.markdown("<br>", unsafe_allow_html=True)
    col_btn_1, col_btn_2, col_btn_3 = st.columns([1, 2, 1])
    
    with col_btn_2:
        start_btn = st.button("🚀 INITIATE AUTO-REPAIR SEQUENCE")

    # --- EXECUTION LOOP ---
    if start_btn:
        st.markdown("---")
        
        # Two-Column Dashboard for Execution
        status_col, terminal_col = st.columns([1, 1])
        
        with status_col:
            st.subheader("🧠 Neural Processing")
            status_box = st.status("Initializing Agent Swarm...", expanded=True)
            
        with terminal_col:
            st.subheader("💻 Live Terminal")
            terminal = st.empty()
            terminal.code("Waiting for agent logs...", language="bash")

        # INIT GRAPH
        app = build_graph()
        initial_state = {
            "code_filename": uploaded_file.name,
            "error_log": "",
            "current_code": "",
            "iterations": 0,
            "status": "start"
        }

        # STREAMING EXECUTION
        # We catch potential errors gracefully
        try:
            stream = app.stream(initial_state)
            logs = ""
            
            for event in stream:
                for key, value in event.items():
                    if key == "coder":
                        # UPDATE UI
                        status_box.write(f"⚙️ **Iteration {value['iterations']}**: Refactoring Logic...")
                        status_box.update(label="🤖 Agent is writing code...", state="running")
                        
                        # UPDATE TERMINAL
                        logs += f"> [CODER] Fixing bugs in {uploaded_file.name}...\n"
                        terminal.code(logs, language="bash")
                        time.sleep(0.3) 
                        
                    elif key == "tester":
                        if value['status'] == "fixed":
                            status_box.update(label="✅ Repair Successful!", state="complete", expanded=False)
                            logs += "> [TESTER] ✅ ALL TESTS PASSED.\n"
                            terminal.code(logs, language="bash")
                        else:
                            status_box.update(label="❌ Tests Failed. Analyzing...", state="error")
                            logs += f"> [TESTER] ❌ FAIL. Error: {value['error_log'][:50]}...\n"
                            terminal.code(logs, language="bash")
                            
        except Exception as e:
            status_box.update(label="⚠️ Critical Error", state="error")
            st.error(f"An error occurred during execution: {e}")

        # --- FINAL COMPARISON ---
        st.markdown("---")
        st.subheader("✨ Repair Report")
        
        with open(file_path, "r") as f:
            fixed_code = f.read()
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**❌ Original (Broken)**")
            st.code(original_code, language="python")
        with c2:
            st.markdown("**✅ Patched (Fixed)**")
            st.code(fixed_code, language="python")
            
        st.balloons()

        # DOWNLOAD
        st.download_button(
            label="💾 Download Fixed Script",
            data=fixed_code,
            file_name=f"fixed_{uploaded_file.name}",
            mime="text/x-python"
        )
else:
    # Empty State Helper
    st.info("👆 Upload a Python file to begin the debugging session.")