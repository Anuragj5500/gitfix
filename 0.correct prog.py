import streamlit as st
import os
from sandbox.container_mgr import Sandbox
from agent.graph import build_graph

st.set_page_config(page_title="GitFix AI", page_icon="Rx")

st.title("🛠️ GitFix: Autonomous Code Repair")
st.markdown("Upload a broken Python file, and watch the AI agent fix it live.")

# --- 1. Manage Sandbox ---
@st.cache_resource
def get_sandbox():
    box = Sandbox()
    box.build_and_start()
    return box

try:
    sandbox = get_sandbox()
    st.success("Docker Sandbox Ready 🐳")
except Exception as e:
    st.error(f"Could not start Docker: {e}")
    st.stop()

# --- 2. File Upload ---
uploaded_file = st.file_uploader("Upload a Python file (.py)", type="py")

if uploaded_file:
    file_path = os.path.join(os.getcwd(), uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.subheader("Original Code")
    with open(file_path, "r") as f:
        original_code = f.read()
    st.code(original_code, language="python")

    # --- 3. The Agent Loop ---
    if st.button("✨ Auto-Fix Code"):
        app = build_graph()
        
        initial_state = {
            "code_filename": uploaded_file.name,
            "error_log": "",
            "current_code": "",
            "iterations": 0,
            "status": "start"
        }
        
        st.divider()
        st.write("### 🧠 Agent Progress")
        
        # USE STREAM() INSTEAD OF INVOKE()
        # This lets us catch updates step-by-step
        stream = app.stream(initial_state)
        
        for event in stream:
            for key, value in event.items():
                if key == "coder":
                    st.info(f"🤖 **Coder:** Rewrote the code (Iteration {value['iterations']})")
                elif key == "tester":
                    if value['status'] == "fixed":
                        st.success("✅ **Tester:** Tests Passed!")
                    else:
                        st.error("❌ **Tester:** Tests Failed. Sending back to Coder...")
                        with st.expander("View Error Log"):
                            st.code(value['error_log'])

        # --- 4. Final Result ---
        st.divider()
        st.subheader("✅ Final Fixed Code")
        
        with open(file_path, "r") as f:
            fixed_code = f.read()
            
        st.code(fixed_code, language="python")
        st.download_button("Download Fixed File", fixed_code, file_name=f"fixed_{uploaded_file.name}")