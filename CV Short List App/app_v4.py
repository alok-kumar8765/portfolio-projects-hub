import datetime
import os
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. DATABASE INITIALIZATION (SQLite3)
# -----------------------------------------------------------------------------
def init_db():
  conn = sqlite3.connect("recruitment.db")
  cursor = conn.cursor()

  # Jobs Table with Salary field
  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            department TEXT,
            experience TEXT,
            vacancies INTEGER,
            salary TEXT,
            tools TEXT,
            description TEXT,
            date TEXT,
            status TEXT
        )
    """
  )

  # Candidates Table with Status/Action controls
  cursor.execute(
      """
        CREATE TABLE IF NOT EXISTS candidates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            job_id INTEGER,
            name TEXT,
            email TEXT,
            skills TEXT,
            match_score INTEGER,
            stage TEXT,
            status TEXT,
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
    """
  )

  # Seed initial sample data if empty
  cursor.execute("SELECT COUNT(*) FROM jobs")
  if cursor.fetchone()[0] == 0:
    default_jobs = [
        (
            ".Net Developer",
            "Development",
            "02 Years",
            12,
            "$80,000 - $100,000",
            "C#, .NET, SQL, Azure",
            "Build robust enterprise microservices.",
            "14.10.2020",
            "Open",
        ),
        (
            "Graphic Designer",
            "Designing",
            "05 Years",
            24,
            "$60,000 - $75,000",
            "Figma, Photoshop, Illustrator",
            "Create stunning brand assets.",
            "10.08.2020",
            "Closed",
        ),
        (
            "Python Developer",
            "Development",
            "3 Years",
            8,
            "$90,000 - $115,000",
            "Python, Streamlit, Pandas, SQL",
            "Build analytical web applications.",
            "16.12.2020",
            "Open",
        ),
    ]
    cursor.executemany(
        "INSERT INTO jobs (title, department, experience, vacancies, salary,"
        " tools, description, date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        default_jobs,
    )

  cursor.execute("SELECT COUNT(*) FROM candidates")
  if cursor.fetchone()[0] == 0:
    default_cands = [
        (3, "Mackeil Jef", "mackeil@gmail.com", "Python, SQL, Streamlit", 92, "Interview", "Pending"),
        (1, "Rosen Leigh", "rosen@gmail.com", "C#, .NET, Azure", 78, "Applied", "Pending"),
        (3, "Rajesh Marfph", "rajesh@gmail.com", "Python, Pandas", 85, "Screening", "Accepted"),
    ]
    cursor.executemany(
        "INSERT INTO candidates (job_id, name, email, skills, match_score,"
        " stage, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
        default_cands,
    )

  conn.commit()
  conn.close()


init_db()


def run_query(query, params=(), fetch=True):
  conn = sqlite3.connect("recruitment.db")
  cursor = conn.cursor()
  cursor.execute(query, params)
  result = cursor.fetchall() if fetch else None
  conn.commit()
  conn.close()
  return result


# -----------------------------------------------------------------------------
# 2. PAGE CONFIGURATION & THEME STYLING
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Recruitment Analytics Dashboard", page_icon="👔", layout="wide"
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    div[data-testid="metric-container"] {
        background-color: #161922;
        border: 1px solid #282c37;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.4);
    }
    section[data-testid="stSidebar"] {
        background-color: #12141c;
        border-right: 1px solid #282c37;
    }
    .custom-card {
        background-color: #161922;
        border: 1px solid #282c37;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.5);
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 6px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff2a2a;
        color: white;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 3. SIDEBAR NAVIGATION & PORTAL SWITCHER (FIXED WITH UNIQUE KEYS)
# -----------------------------------------------------------------------------
st.sidebar.title("HR Analytics Hub")
portal_mode = st.sidebar.radio(
    "Select Portal View",
    ["HR & Admin Dashboard", "Candidate Application Portal"],
    key="portal_mode",
)

if portal_mode == "HR & Admin Dashboard":
  page = st.sidebar.radio(
      "Navigation",
      [
          "Dashboard",
          "Post New Job",
          "Candidates Management",
          "Hiring Pipeline (Kanban)",
          "Reports",
      ],
      key="nav_page",
  )
else:
  page = "Candidate Portal"

# -----------------------------------------------------------------------------
# 4. CANDIDATE APPLICATION PORTAL (External View)
# -----------------------------------------------------------------------------
if page == "Candidate Portal":
  st.title("🌟 Candidate Application Portal")
  st.write(
      "Browse open roles, submit your resume/CV, and let our AI match your"
      " skills instantly!"
  )

  open_jobs = run_query(
      "SELECT id, title, department, salary, tools, description FROM jobs WHERE"
      " status='Open'"
  )

  if not open_jobs:
    st.warning("There are currently no open job positions available.")
  else:
    job_map = {f"{j[1]} ({j[2]}) - Offer: {j[3]}": j[0] for j in open_jobs}
    job_details = {j[0]: {"tools": j[4], "desc": j[5]} for j in open_jobs}

    selected_job_label = st.selectbox(
        "Select Job Position to Apply", list(job_map.keys())
    )
    chosen_job_id = job_map[selected_job_label]

    st.info(
        f"**Required Tech Stack / Tools:**"
        f" {job_details[chosen_job_id]['tools']}"
    )

    with st.form("candidate_apply_form"):
      c1, c2 = st.columns(2)
      with c1:
        cand_name = st.text_input("Full Name")
        cand_email = st.text_input("Email Address")
      with c2:
        cand_phone = st.text_input("Phone Number")
        manual_skills = st.text_input(
            "Your Skills (Comma-separated)",
            placeholder="Python, SQL, React, AWS",
        )

      uploaded_cv = st.file_uploader(
          "Upload CV/Resume (PDF or TXT)", type=["pdf", "txt"]
      )
      submitted_app = st.form_submit_button("Submit Application")

      if submitted_app:
        if cand_name and cand_email and manual_skills:
          required_tools_str = job_details[chosen_job_id]["tools"]
          req_list = [
              t.strip().lower() for t in required_tools_str.split(",")
          ]
          cand_list = [s.strip().lower() for s in manual_skills.split(",")]

          if uploaded_cv is not None:
            file_contents = uploaded_cv.read().decode("utf-8", errors="ignore")
            for word in file_contents.split():
              clean_w = word.strip(",.").lower()
              if clean_w in [
                  "python",
                  "sql",
                  "react",
                  "c#",
                  "azure",
                  "figma",
                  "pandas",
              ]:
                if clean_w not in cand_list:
                  cand_list.append(clean_w)

          matching_skills = set(req_list).intersection(set(cand_list))
          score = (
              int((len(matching_skills) / max(len(req_list), 1)) * 100)
              if req_list
              else 70
          )
          score = max(score, 50)

          run_query(
              "INSERT INTO candidates (job_id, name, email, skills, match_score,"
              " stage, status) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (
                  chosen_job_id,
                  cand_name,
                  cand_email,
                  ", ".join(cand_list),
                  score,
                  "Applied",
                  "Pending",
              ),
              fetch=False,
          )

          st.success(
              f"Application submitted successfully! AI Match Score calculated:"
              f" **{score}%**."
          )
        else:
          st.error("Please fill out your name, email, and skills.")

# -----------------------------------------------------------------------------
# 5. HR DASHBOARD VIEW
# -----------------------------------------------------------------------------
elif page == "Dashboard":
  col_title, col_notif, col_user = st.columns([8, 1, 1])
  with col_title:
    st.markdown("## Recruitment Analytics")
  with col_notif:
    st.markdown("🔔")
  with col_user:
    st.markdown("👤")

  st.markdown("---")

  top_left, top_right = st.columns([2, 1])

  with top_left:
    st.markdown(
        "<div class='custom-card'><h4>Candidate Performance</h4>",
        unsafe_allow_html=True,
    )
    time_filter = st.radio(
        "Timeframe",
        ["Weekly", "Monthly", "Yearly"],
        horizontal=True,
        label_visibility="collapsed",
        key="time_filter_dashboard",
    )

    chart_data = pd.DataFrame({
        "month": [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sep",
            "Oct",
            "Nov",
            "Dec",
        ],
        "applications": [45, 32, 60, 38, 42, 35, 50, 40, 55, 62, 30, 48],
    })
    fig = px.line(
        chart_data,
        x="month",
        y="applications",
        markers=True,
        line_shape="spline",
    )
    fig.update_traces(
        line_color="#ff4b4b", line_width=3, marker=dict(size=8, color="#ff4b4b")
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=20, r=20, t=20, b=20),
        height=240,
    )
    st.plotly_chart(fig, width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)

  with top_right:
    total_jobs = len(run_query("SELECT * FROM jobs"))
    total_cands = len(run_query("SELECT * FROM candidates"))
    col_m1, col_m2 = st.columns(2)
    with col_m1:
      st.metric(
          label="Total Job Posted",
          value=str(total_jobs),
          delta="This Month",
          delta_color="off",
      )
      st.metric(
          label="Get Hired", value="120", delta="This Month", delta_color="off"
      )
    with col_m2:
      st.metric(
          label="Applied Candidates",
          value=str(total_cands),
          delta="This Month",
          delta_color="off",
      )
      st.metric(
          label="Today Interviews", value="56", delta="Today", delta_color="off"
      )

  st.markdown("---")

  mid1, mid2 = st.columns([1, 1.2])

  with mid1:
    st.markdown(
        "<div class='custom-card'><h4>Job Statistics</h4>",
        unsafe_allow_html=True,
    )
    fig_donut = go.Figure(
        data=[
            go.Pie(
                labels=["Male Candidates", "Female Candidates"],
                values=[1234, 1754],
                hole=0.7,
                marker_colors=["#ff4b4b", "#0083B0"],
            )
        ]
    )
    fig_donut.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        margin=dict(l=10, r=10, t=10, b=10),
        height=180,
        annotations=[
            dict(
                text="<b>Total<br>2,988</b>",
                x=0.5,
                y=0.5,
                font_size=14,
                showarrow=False,
                font_color="white",
            )
        ],
    )
    st.plotly_chart(fig_donut, width='stretch')
    st.markdown("</div>", unsafe_allow_html=True)

  with mid2:
      st.markdown(
          "<div class='custom-card'><h4>Recent Applicants & Schedule</h4>",
          unsafe_allow_html=True,
      )
      recent_candidates = run_query(
          "SELECT id, name, skills, match_score FROM candidates LIMIT 3"
      )
      for rc in recent_candidates:
        c_id, c_name, c_skills, c_score = rc
        col_a, col_b, col_c = st.columns([2, 2, 1.5])

        # FIXED: Added unsafe_allow_html=True here
        col_a.markdown(
            f"**{c_name}**<br><small>{c_skills[:20]}...</small>",
            unsafe_allow_html=True,
        )

        col_b.markdown(
            f"<span style='color: #ff4b4b;'>Match: {c_score}%</span>",
            unsafe_allow_html=True,
        )
        with col_c:
          if st.button("Schedule", key=f"sch_dash_{c_id}"):
            st.success(f"Interview scheduled for {c_name}!")
        st.markdown(
            "<hr style='margin: 4px 0; border-color: #282c37;'>",
            unsafe_allow_html=True,
        )
      st.markdown("</div>", unsafe_allow_html=True)
  st.markdown(
      "<div class='custom-card'><h4>Pending Request Approvals & Candidate"
      " Status Actions</h4>",
      unsafe_allow_html=True,
  )

  pending_cands = run_query(
      "SELECT c.id, c.name, j.title, c.skills, c.match_score, c.status FROM"
      " candidates c JOIN jobs j ON c.job_id = j.id"
  )

  if pending_cands:
    t_cols = st.columns([2, 2, 2, 1, 1.5, 2])
    t_cols[0].markdown("**Candidate**")
    t_cols[1].markdown("**Applied Role**")
    t_cols[2].markdown("**Skills / Match**")
    t_cols[3].markdown("**Status**")
    t_cols[4].markdown("**Accept**")
    t_cols[5].markdown("**Cancel / Reject**")
    st.markdown(
        "<hr style='margin: 5px 0; border-color: #282c37;'>",
        unsafe_allow_html=True,
    )

    for pc in pending_cands:
      cand_id, cand_name, role_title, skills, score, status = pc
      cols = st.columns([2, 2, 2, 1, 1.5, 2])
      cols[0].markdown(f"**{cand_name}**")
      cols[1].markdown(role_title)
      cols[2].markdown(f"{score}% match")

      status_color = (
          "#28a745"
          if status == "Accepted"
          else ("#dc3545" if status == "Cancelled" else "#ffc107")
      )
      cols[3].markdown(
          f"<span style='color: {status_color}; font-weight:"
          f" bold;'>{status}</span>",
          unsafe_allow_html=True,
      )

      with cols[4]:
        if st.button("✔ Accept", key=f"acc_{cand_id}"):
          run_query(
              "UPDATE candidates SET status = 'Accepted' WHERE id = ?",
              (cand_id,),
              fetch=False,
          )
          st.rerun()

      with cols[5]:
        if st.button("❌ Cancel", key=f"can_{cand_id}"):
          run_query(
              "UPDATE candidates SET status = 'Cancelled' WHERE id = ?",
              (cand_id,),
              fetch=False,
          )
          st.rerun()

      st.markdown(
          "<hr style='margin: 4px 0; border-color: #282c37;'>",
          unsafe_allow_html=True,
      )
  else:
    st.info("No candidates pending approval.")

  st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 6. POST NEW JOB VIEW
# -----------------------------------------------------------------------------
elif page == "Post New Job":
  st.title("📝 Post a Job Description & Salary Budget")
  st.write(
      "Define job openings, required tools/technologies, and compensation"
      " packages."
  )

  with st.form("hr_job_post_form"):
    c1, c2 = st.columns(2)
    with c1:
      title = st.text_input(
          "Job Title", placeholder="e.g. Senior Frontend Engineer"
      )
      dept = st.selectbox(
          "Department",
          ["Development", "Designing", "Quality & Control", "Product", "HR"],
      )
      experience = st.text_input("Required Experience", placeholder="e.g. 3-5 Years")
    with c2:
      vacancies = st.number_input(
          "Number of Vacancies", min_value=1, max_value=50, value=1
      )
      salary = st.text_input(
          "Salary / Budget Offer", placeholder="e.g. $95,000 - $120,000"
      )
      tools = st.text_input(
          "Required Tools & Technologies (Comma-separated)",
          placeholder="Python, React, Docker, SQL",
      )

    description = st.text_area(
        "Job Description & Requirements",
        placeholder=(
            "Detail responsibilities, tech stacks, and qualifications..."
        ),
    )
    published = st.form_submit_button("Publish Job Posting")

    if published:
      if title and tools and salary:
        date_str = datetime.date.today().strftime("%d.%m.%Y")
        run_query(
            "INSERT INTO jobs (title, department, experience, vacancies,"
            " salary, tools, description, date, status) VALUES (?, ?, ?, ?, ?,"
            " ?, ?, ?, ?)",
            (
                title,
                dept,
                experience,
                vacancies,
                salary,
                tools,
                description,
                date_str,
                "Open",
            ),
            fetch=False,
        )
        st.success(
            f"Job '{title}' published successfully with salary budget {salary}!"
        )
      else:
        st.error(
            "Please fill out Job Title, Salary Offer, and Required Tools &"
            " Technologies."
        )

# -----------------------------------------------------------------------------
# 7. OTHER HR PAGES (Candidates Management, Kanban Pipeline, Reports)
# -----------------------------------------------------------------------------
elif page == "Candidates Management":
  st.title("👤 All Candidates Database")
  df_cands = pd.DataFrame(
      run_query(
          "SELECT c.id, c.name, c.email, j.title, c.skills, c.match_score,"
          " c.status FROM candidates c JOIN jobs j ON c.job_id = j.id"
      ),
      columns=["ID", "Name", "Email", "Role", "Skills", "Match Score", "Status"],
  )
  st.dataframe(df_cands, width='stretch')

elif page == "Hiring Pipeline (Kanban)":
  st.title("💼 Recruitment Pipeline Kanban Board")
  stages = ["Applied", "Screening", "Interview", "Offered"]
  cols = st.columns(len(stages))

  all_cands = run_query("SELECT id, name, skills, match_score, stage FROM candidates")

  for idx, stage in enumerate(stages):
    with cols[idx]:
      st.markdown(f"### {stage}")
      st.markdown("---")
      stage_list = [c for c in all_cands if c[4] == stage]
      for c in stage_list:
        st.markdown(
            f"""
                <div style="background-color: #161922; padding: 12px; border-radius: 8px; border: 1px solid #282c37; margin-bottom: 10px;">
                    <b>{c[1]}</b><br>
                    <small>Skills: {c[2]}</small><br>
                    <span style="color: #ff4b4b;">Match: {c[3]}%</span>
                </div>
                """,
            unsafe_allow_html=True,
        )
        if idx < len(stages) - 1:
          next_s = stages[idx + 1]
          if st.button(f"Move ➡️ {next_s}", key=f"kanban_{c[0]}"):
            run_query(
                "UPDATE candidates SET stage = ? WHERE id = ?",
                (next_s, c[0]),
                fetch=False,
            )
            st.rerun()

elif page == "Reports":
  st.title("📊 HR Analytics & Reports")
  st.download_button(
      "📥 Download Active Jobs Report (CSV)",
      data=pd.DataFrame(run_query("SELECT * FROM jobs")).to_csv(index=False),
      file_name="jobs_report.csv",
      mime="text/csv",
  )