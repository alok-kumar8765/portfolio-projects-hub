import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# -----------------------------------------------------------------------------
# 1. PAGE SETUP & SESSION STATE INITIALIZATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Recruitment Analytics Dashboard",
    page_icon="👔",
    layout="wide",
)

# Custom Styling
st.markdown(
    """
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    div[data-testid="metric-container"] {
        background-color: #1a1c23; border: 1px solid #2d3139;
        padding: 15px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    section[data-testid="stSidebar"] { background-color: #12141c; border-right: 1px solid #2d3139; }
    .custom-card {
        background-color: #161922; border: 1px solid #282c37;
        border-radius: 12px; padding: 20px; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Initialize Session States
if "total_jobs_posted" not in st.session_state:
  st.session_state.total_jobs_posted = 248

if "job_postings" not in st.session_state:
  st.session_state.job_postings = [
      {
          "id": 1,
          "title": ".Net Developer",
          "department": "Development",
          "experience": "02 Years",
          "vacancies": 12,
          "date": "14.10.2020",
          "status": "Open",
      },
      {
          "id": 2,
          "title": "Graphic Designer",
          "department": "Designing",
          "experience": "05 Years",
          "vacancies": 24,
          "date": "10.08.2020",
          "status": "Closed",
      },
      {
          "id": 3,
          "title": "Java Developer",
          "department": "Development",
          "experience": "3 Years",
          "vacancies": 8,
          "date": "16.12.2020",
          "status": "Open",
      },
      {
          "id": 4,
          "title": "QA Tester",
          "department": "Quality & Control",
          "experience": "04 Years",
          "vacancies": 26,
          "date": "05.11.2020",
          "status": "Open",
      },
  ]

if "candidates" not in st.session_state:
  st.session_state.candidates = [
      {
          "name": "Mackeil Jef",
          "role": "Designer",
          "stage": "Interview",
          "match_score": 92,
      },
      {
          "name": "Rosen Leigh",
          "role": "Project Manager",
          "stage": "Applied",
          "match_score": 78,
      },
      {
          "name": "Rajesh Marfph",
          "role": "Team Lead",
          "stage": "Screening",
          "match_score": 85,
      },
      {
          "name": "Joseph George",
          "role": "Senior Developer",
          "stage": "Offered",
          "match_score": 95,
      },
      {
          "name": "Daniel Jackson",
          "role": "Designer",
          "stage": "Applied",
          "match_score": 64,
      },
  ]

if "scheduled_interviews" not in st.session_state:
  st.session_state.scheduled_interviews = []

# -----------------------------------------------------------------------------
# 2. SIDEBAR NAVIGATION
# -----------------------------------------------------------------------------
st.sidebar.title("HR Analytics")
selected_page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Post New Job",
        "AI Resume Screener",
        "Hiring Pipeline",
        "Reports",
    ],
)

# -----------------------------------------------------------------------------
# 3. PAGE 1: DASHBOARD VIEW
# -----------------------------------------------------------------------------
if selected_page == "Dashboard":
  st.title("Recruitment Analytics")

  # Top KPI Metrics
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Total Job Posted", str(st.session_state.total_jobs_posted), "+1 This Month")
  col2.metric("Applied Candidates", "2,000", "+12%")
  col3.metric("Get Hired", "120", "+5%")
  col4.metric(
      "Today Interviews",
      str(len(st.session_state.scheduled_interviews) + 56),
      "Active",
  )

  st.divider()

  # Main Content Charts Row
  c1, c2 = st.columns([2, 1])

  with c1:
    st.markdown(
        "<div class='custom-card'><h4>Candidate Performance</h4>",
        unsafe_allow_html=True,
    )
    tf = st.radio(
        "Timeframe",
        ["Weekly", "Monthly", "Yearly"],
        horizontal=True,
        label_visibility="collapsed",
    )

    data_map = {
        "Weekly": {
            "x": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "y": [12, 24, 18, 35, 28, 15, 10],
        },
        "Monthly": {
            "x": [
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
            "y": [45, 32, 60, 38, 42, 35, 50, 40, 55, 62, 30, 48],
        },
        "Yearly": {
            "x": ["2023", "2024", "2025", "2026"],
            "y": [320, 450, 610, 890],
        },
    }

    df_chart = pd.DataFrame(data_map[tf])
    fig = px.line(
        df_chart,
        x="x",
        y="y",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#ff4b4b"],
    )
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=240,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

  with c2:
    st.markdown(
        "<div class='custom-card'><h4>Job Statistics</h4>",
        unsafe_allow_html=True,
    )
    fig_donut = go.Figure(
        data=[
            go.Pie(
                labels=["Male Candidates", "Female Candidates"],
                values=[1234, 1754],
                hole=0.6,
                marker_colors=["#ff4b4b", "#0083B0"],
            )
        ]
    )
    fig_donut.update_layout(
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        height=210,
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
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

  st.divider()

  # Interactive Schedule Section & Pending Requests
  row2_col1, row2_col2 = st.columns([1, 1.2])

  with row2_col1:
    st.markdown(
        "<div class='custom-card'><h4>Schedule Interviews</h4>",
        unsafe_allow_html=True,
    )
    for idx, cand in enumerate(st.session_state.candidates[:3]):
      ac1, ac2, ac3 = st.columns([2, 2, 2])
      ac1.write(f"**{cand['name']}**")
      ac2.write(f"<small>{cand['role']}</small>", unsafe_allow_html=True)

      with ac3:
        if st.button("Schedule", key=f"sch_{idx}"):
          st.session_state.scheduled_interviews.append({
              "candidate": cand["name"],
              "role": cand["role"],
              "date": str(datetime.date.today()),
          })
          st.success(f"Scheduled for {cand['name']}!")
      st.markdown(
          "<hr style='margin: 5px 0; border-color: #282c37;'>",
          unsafe_allow_html=True,
      )
    st.markdown("</div>", unsafe_allow_html=True)

  with row2_col2:
    st.markdown(
        "<div class='custom-card'><h4>Pending Request Approvals</h4>",
        unsafe_allow_html=True,
    )
    for job in st.session_state.job_postings:
      cols = st.columns([2, 2, 1.5, 1.5])
      cols[0].write(f"**{job['title']}**")
      cols[1].write(job["department"])

      status_color = "#28a745" if job["status"] == "Open" else "#dc3545"
      cols[2].markdown(
          f"<span style='color:{status_color}'>{job['status']}</span>",
          unsafe_allow_html=True,
      )

      with cols[3]:
        if job["status"] == "Open":
          if st.button("Accept", key=f"acc_{job['id']}"):
            job["status"] = "Approved"
            st.toast(f"Approved {job['title']}!")
            st.rerun()
        else:
          st.write("✅ Approved")
      st.markdown(
          "<hr style='margin: 5px 0; border-color: #282c37;'>",
          unsafe_allow_html=True,
      )
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 4. PAGE 2: POST NEW JOB
# -----------------------------------------------------------------------------
elif selected_page == "Post New Job":
  st.title("📝 Post a Job Description")
  st.write("Translate HR recruitment requirements into dynamic system data.")

  with st.form("post_job_form"):
    c1, c2 = st.columns(2)
    with c1:
      title = st.text_input("Job Title", placeholder="e.g. Senior Python Developer")
      dept = st.selectbox(
          "Department",
          ["Development", "Designing", "Quality & Control", "Product", "HR"],
      )
      exp = st.text_input("Experience Required", placeholder="e.g. 3-5 Years")
    with c2:
      vacancies = st.number_input(
          "Vacancies", min_value=1, max_value=50, value=1
      )
      manager = st.text_input("Hiring Manager", placeholder="e.g. Sarah Connor")
      budget = st.text_input("Salary Budget", placeholder="e.g. $90,000 - $110,000")

    description = st.text_area("Job Description & Requirements")
    submitted = st.form_submit_button("Publish Job Position")

    if submitted:
      if title and description:
        st.session_state.total_jobs_posted += 1
        new_entry = {
            "id": len(st.session_state.job_postings) + 1,
            "title": title,
            "department": dept,
            "experience": exp,
            "vacancies": vacancies,
            "date": datetime.date.today().strftime("%d.%m.%Y"),
            "status": "Open",
        }
        st.session_state.job_postings.append(new_entry)
        st.success(f"Job posting '{title}' published successfully!")
      else:
        st.error("Please fill in required fields (Title and Description).")

# -----------------------------------------------------------------------------
# 5. PAGE 3: AI RESUME SCREENER & MATCH SCORE ENGINE
# -----------------------------------------------------------------------------
elif selected_page == "AI Resume Screener":
  st.title("🤖 AI Resume Screening & Match Engine")
  st.write("Upload candidate resumes to rank them against selected job descriptions.")

  col_job, col_file = st.columns([1, 1])
  with col_job:
    selected_job_title = st.selectbox(
        "Select Active Position",
        [j["title"] for j in st.session_state.job_postings],
    )
    req_skills = st.multiselect(
        "Key Required Skills",
        ["Python", "Streamlit", "SQL", "Docker", "REST API", "Figma", "AWS"],
        default=["Python", "SQL"],
    )

  with col_file:
    uploaded_file = st.file_uploader("Upload CV/Resume (TXT or PDF)", type=["txt", "pdf"])

  if uploaded_file and st.button("Run AI Match Score"):
    # Simulated AI parsing & matching
    score = 88
    st.divider()
    st.subheader("Match Analysis Result")

    m1, m2 = st.columns(2)
    m1.metric("Overall Match Score", f"{score}%", "+8% threshold")
    m2.progress(score / 100)

    st.markdown("### Skill Breakdown")
    st.success("✅ Matching Skills Found: Python, SQL, REST API")
    st.warning("⚠️ Missing Skills: Docker")

# -----------------------------------------------------------------------------
# 6. PAGE 4: HIRING PIPELINE (KANBAN BOARD)
# -----------------------------------------------------------------------------
elif selected_page == "Hiring Pipeline":
  st.title("💼 Recruitment Kanban Pipeline")

  stages = ["Applied", "Screening", "Interview", "Offered"]
  cols = st.columns(len(stages))

  for idx, stage in enumerate(stages):
    with cols[idx]:
      st.markdown(f"### {stage}")
      st.markdown("---")

      # Filter candidates by stage
      stage_candidates = [
          c for c in st.session_state.candidates if c["stage"] == stage
      ]

      for c_idx, candidate in enumerate(stage_candidates):
        with st.container():
          st.markdown(
              f"""
                    <div style="background-color: #1a1c23; padding: 12px; border-radius: 8px; border: 1px solid #333; margin-bottom: 10px;">
                        <b>{candidate['name']}</b><br>
                        <small>{candidate['role']}</small><br>
                        <span style="color: #ff4b4b;">Match: {candidate['match_score']}%</span>
                    </div>
                    """,
              unsafe_allow_html=True,
          )

          # Stage movement control
          if idx < len(stages) - 1:
            if st.button(
                f"Move to {stages[idx+1]} ➡️", key=f"m_{candidate['name']}"
            ):
              candidate["stage"] = stages[idx + 1]
              st.rerun()

# -----------------------------------------------------------------------------
# 7. PAGE 5: REPORTS & SCHEDULED INTERVIEWS
# -----------------------------------------------------------------------------
elif selected_page == "Reports":
  st.title("📊 HR Reports & Scheduled Events")

  st.subheader("Scheduled Interviews")
  if st.session_state.scheduled_interviews:
    st.table(pd.DataFrame(st.session_state.scheduled_interviews))
  else:
    st.info("No interviews scheduled yet.")

  st.divider()

  st.subheader("Export System Data")
  df_export = pd.DataFrame(st.session_state.job_postings)
  st.download_button(
      label="📥 Download Job Postings (CSV)",
      data=df_export.to_csv(index=False),
      file_name="job_postings.csv",
      mime="text/csv",
  )