# dashboard/app.py
import streamlit as st
import subprocess
import os
import sys

st.set_page_config(
    page_title="Advanced QA Framework Dashboard",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Enterprise QA Automation Control Center")
st.markdown("Trigger, monitor, and audit test executions across UI, API, and Visual suites.")

# Sidebar controls for test execution configuration
st.sidebar.header("Test Configuration")
environment = st.sidebar.selectbox("Environment", ["dev", "staging"])
browser = st.sidebar.selectbox("Browser Engine", ["chromium", "firefox", "webkit"])
test_suite = st.sidebar.selectbox(
    "Test Suite", 
    [
        "All Tests (Full Suite)",
        "Authentication Tests (tests/test_auth.py)",
        "API Tests (tests/test_api.py)",
        "Visual Regression (tests/test_visual.py)",
        "Accessibility Audits (tests/test_accessibility.py)"
    ]
)
headed_mode = st.sidebar.checkbox("Run in Headed Browser Mode", value=False)

# Map UI selections to pytest arguments
suite_mapping = {
    "All Tests (Full Suite)": "tests/",
    "Authentication Tests (tests/test_auth.py)": "tests/test_auth.py",
    "API Tests (tests/test_api.py)": "tests/test_api.py",
    "Visual Regression (tests/test_visual.py)": "tests/test_visual.py",
    "Accessibility Audits (tests/test_accessibility.py)": "tests/test_accessibility.py"
}

target_path = suite_mapping[test_suite]

col1, col2 = st.columns(2)

with col1:
    st.subheader("Execution Controls")
    if st.button("▶️ Execute Selected Test Suite", type="primary"):
        with st.spinner(f"Running {test_suite} on {environment} ({browser})..."):
            
            # Construct pytest command
            cmd = [
                sys.executable, "-m", "pytest",
                target_path,
                f"--browser={browser}",
                "--alluredir=reports/allure-results"
            ]
            if headed_mode:
                cmd.append("--headed")
                
            # Set environment variables for subprocess
            env = os.environ.copy()
            env["ENV"] = environment
            
            # Run test execution
            result = subprocess.run(cmd, capture_output=True, text=True, env=env)
            
            st.session_state["last_output"] = result.stdout + result.stderr
            st.session_state["exit_code"] = result.returncode

with col2:
    st.subheader("Live Execution Status")
    if "exit_code" in st.session_state:
        if st.session_state["exit_code"] == 0:
            st.success("✅ Test Suite Passed Successfully!")
        else:
            st.error("❌ Test Suite Encountered Failures.")
            
        with st.expander("View Full Pytest Terminal Logs", expanded=True):
            st.code(st.session_state.get("last_output", "No execution output yet."), language="text")
    else:
            st.info("Configure settings in the sidebar and click 'Execute Selected Test Suite' to start.")

st.markdown("---")
st.markdown("### 📊 Reporting & Artifacts")
if st.button("Generate & Open Allure Report Summary"):
    st.info("Run `allure serve reports/allure-results` in your local terminal to launch the interactive HTML report.")