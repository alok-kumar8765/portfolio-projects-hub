import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Code Security Scanner", page_icon="🛡️", layout="wide")

st.markdown("""
    <style>
    .metric-card {
        background-color: #1a1c23;
        border: 1px solid #2d3139;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

if "issues" not in st.session_state:
    st.session_state.issues = []
if "code_files" not in st.session_state:
    st.session_state.code_files = {
        "app.py": "import os\nimport subprocess\nfrom flask import Flask\n\napp = Flask(__name__)\n\n@app.route('/run')\ndef run():\n    cmd = request.args.get('cmd')\n    return subprocess.check_output(cmd, shell=True)\n\npassword = \"admin123\"\napi_key = \"sk-1234567890abcdef\"\napp.run(debug=True)",
        "utils.py": "import hashlib\n\ndef hash_data(data):\n    return hashlib.md5(data.encode()).hexdigest()"
    }

def scan_code(filename, code):
    issues = []
    for idx, line in enumerate(code.splitlines(), 1):
        if "shell=True" in line:
            issues.append({"id": len(issues)+1, "severity": "Critical", "issue_type": "Command Injection", "file": filename, "line": idx, "description": "Shell injection risk detected.", "vulnerable_code": line, "recommendation": "Avoid shell=True.", "secure_code": "subprocess.check_output(args, shell=False)"})
        if "password" in line or "api_key" in line:
            issues.append({"id": len(issues)+1, "severity": "Critical", "issue_type": "Hardcoded Secret", "file": filename, "line": idx, "description": "Hardcoded credential detected.", "vulnerable_code": line, "recommendation": "Use environment variables.", "secure_code": "os.environ.get('API_KEY')"})
        if "debug=True" in line:
            issues.append({"id": len(issues)+1, "severity": "High", "issue_type": "Debug Mode", "file": filename, "line": idx, "description": "Debug mode enabled.", "vulnerable_code": line, "recommendation": "Disable in production.", "secure_code": "app.run(debug=False)"})
        if "hashlib.md5" in line:
            issues.append({"id": len(issues)+1, "severity": "Medium", "issue_type": "Insecure Crypto", "file": filename, "line": idx, "description": "Weak hash algorithm.", "vulnerable_code": line, "recommendation": "Use SHA-256.", "secure_code": "hashlib.sha256()"})
    return issues

st.title("🛡️ AI Code Security Scanner")
st.caption("Detect Vulnerabilities • Analyze Code • Get Security Suggestions")

col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
with col2:
    if st.button("⚡ Scan Project"):
        all_issues = []
        for fname, code in st.session_state.code_files.items():
            all_issues.extend(scan_code(fname, code))
        st.session_state.issues = all_issues
        st.success("Project scanned!")

with col3:
    uploaded = st.file_uploader("Upload File", type=["py"], label_visibility="collapsed")
    if uploaded:
        content = uploaded.read().decode("utf-8")
        st.session_state.code_files[uploaded.name] = content
        st.session_state.issues = scan_code(uploaded.name, content)

with col4:
    if st.button("📥 Generate Report"):
        st.download_button("Download Report", data="Security Audit Report\nTotal Issues: " + str(len(st.session_state.issues)), file_name="report.md")

st.divider()

menu = st.sidebar.radio("Navigation", ["Dashboard", "Scan Code", "Results", "Security Tips", "Fix Suggestions", "Settings", "About"])

if menu == "Dashboard":
    c1, c2, c3, c4 = st.columns(4)
    crit = sum(1 for i in st.session_state.issues if i["severity"] == "Critical")
    high = sum(1 for i in st.session_state.issues if i["severity"] == "High")
    med = sum(1 for i in st.session_state.issues if i["severity"] == "Medium")
    low = sum(1 for i in st.session_state.issues if i["severity"] == "Low")
    
    c1.markdown(f"<div class='metric-card'><h4>Critical</h4><h2>{crit}</h2></div>", unsafe_allow_html=True)
    c2.markdown(f"<div class='metric-card'><h4>High</h4><h2>{high}</h2></div>", unsafe_allow_html=True)
    c3.markdown(f"<div class='metric-card'><h4>Medium</h4><h2>{med}</h2></div>", unsafe_allow_html=True)
    c4.markdown(f"<div class='metric-card'><h4>Low</h4><h2>{low}</h2></div>", unsafe_allow_html=True)
    
    st.write("")
    col_a, col_b = st.columns([1.2, 1])
    with col_a:
        sel_file = st.selectbox("Select File", list(st.session_state.code_files.keys()))
        new_code = st.text_area("Code Editor", value=st.session_state.code_files[sel_file], height=300)
        if new_code != st.session_state.code_files[sel_file]:
            st.session_state.code_files[sel_file] = new_code
            st.session_state.issues = scan_code(sel_file, new_code)
    with col_b:
        st.markdown("#### Issue Distribution")
        df_chart = pd.DataFrame({"Severity": ["Critical", "High", "Medium", "Low"], "Count": [crit, high, med, low]})
        st.bar_chart(df_chart.set_index("Severity"))
        
    st.divider()
    st.markdown("#### Scan Results & Inspector")
    if st.session_state.issues:
        df = pd.DataFrame(st.session_state.issues)
        st.dataframe(df[["id", "severity", "issue_type", "file", "line", "description"]], use_container_width=True)
        issue_id = st.selectbox("Select Issue ID for Details", df["id"])
        item = next(i for i in st.session_state.issues if i["id"] == issue_id)
        st.info(item["description"])
        col_v, col_s = st.columns(2)
        with col_v:
            st.code(item["vulnerable_code"], language="python")
        with col_s:
            st.code(item["secure_code"], language="python")
    else:
        st.info("Click 'Scan Project' or upload a file to begin.")

elif menu == "Scan Code":
    st.header("Scan Code Workspace")
    code_input = st.text_area("Paste Python Code:", "os.system('rm -rf /')")
    if st.button("Scan Snippet"):
        res = scan_code("snippet.py", code_input)
        st.write(res)

elif menu == "Results":
    st.header("All Results")
    if st.session_state.issues:
        st.dataframe(pd.DataFrame(st.session_state.issues))
    else:
        st.info("No issues found.")

elif menu == "Security Tips":
    st.header("Security Tips")
    st.write("- Avoid shell=True\n- Never hardcode secrets\n- Disable debug mode in production")

elif menu == "Fix Suggestions":
    st.header("Fix Suggestions")
    for f, c in st.session_state.code_files.items():
        st.write(f"File: {f}")
        for iss in scan_code(f, c):
            st.code(iss["secure_code"])

elif menu == "Settings":
    st.header("Settings")
    st.checkbox("Enable AST Analysis", True)

elif menu == "About":
    st.header("About")
    st.write("AI Code Security Scanner (Streamlit Edition)")