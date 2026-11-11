import datetime
import random
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Recruitment Dashboard", page_icon="👔", layout="wide"
)

# 2. Custom CSS for Dark Theme & Styling Matching the Screenshot
st.markdown(
    """
    <style>
    /* Main background & font color */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Metric Card Styling */
    div[data-testid="metric-container"] {
        background-color: #1a1c23;
        border: 1px solid #2d3139;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #12141c;
        border-right: 1px solid #2d3139;
    }
    
    /* Custom Card Containers */
    .custom-card {
        background-color: #161922;
        border: 1px solid #282c37;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.4);
    }
    
    /* Table styling */
    table {
        width: 100%;
        color: #ffffff;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. Sidebar Navigation
st.sidebar.title("HR Analytics")
page = st.sidebar.radio(
    "Navigation", ["Dashboard", "Candidates", "Hiring", "Reports", "Settings"]
)

# Sidebar Icons simulation via static text/markdown
st.sidebar.markdown("---")
st.sidebar.markdown("🏠 **Dashboard**")
st.sidebar.markdown("👤 **Candidates**")
st.sidebar.markdown("💼 **Hiring**")
st.sidebar.markdown("📊 **Reports**")
st.sidebar.markdown("⚙️ **Settings**")


# 4. Generate Mock Data
@st.cache_data
def load_data():
  # Candidate Performance over months
  months = [
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
  ]
  applications_monthly = [45, 32, 60, 38, 42, 35, 50, 40, 55, 62, 30, 48]
  df_perf = pd.DataFrame(
      {"month": months, "applications": applications_monthly}
  )

  # Pending Request Approvals data
  pending_requests = [
      {
          "Position": ".Net Developer",
          "Experience": "02 Years",
          "Department": "Development",
          "Rating": "95%",
          "Vacancies": 12,
          "Date": "14.10.2020",
          "Status": "Open",
      },
      {
          "Position": "Graphic Designer",
          "Experience": "05 Years",
          "Department": "Designing",
          "Rating": "90%",
          "Vacancies": 24,
          "Date": "10.08.2020",
          "Status": "Closed",
      },
      {
          "Position": "Java Developer",
          "Experience": "3 Years",
          "Department": "Development",
          "Rating": "88%",
          "Vacancies": 8,
          "Date": "16.12.2020",
          "Status": "Open",
      },
      {
          "Position": "QA Tester",
          "Experience": "04 Years",
          "Department": "Quality & Control",
          "Rating": "87%",
          "Vacancies": 26,
          "Date": "05.11.2020",
          "Status": "Open",
      },
      {
          "Position": "Android Developer",
          "Experience": "05 Years",
          "Department": "Designing",
          "Rating": "85%",
          "Vacancies": 24,
          "Date": "10.08.2020",
          "Status": "Closed",
      },
  ]

  recent_applicants = [
      {
          "name": "Mackeil Jef",
          "role": "Designer",
          "avatar": "👨‍💻",
      },
      {"name": "Rosen Leigh", "role": "Project Manager", "avatar": "👩‍💼"},
      {"name": "Rajesh Marfph", "role": "Team Lead", "avatar": "👨‍💼"},
      {"name": "Joseph George", "role": "Senior Developer", "avatar": "👨‍💻"},
  ]

  recent_hirings = [
      {
          "interviewer": "Joanna Smith",
          "email": "joanna.smith14@gmail.com",
          "job": "Product Manager",
          "shortlisted": 16,
      },
      {
          "interviewer": "Nada Wasei",
          "email": "nada.wasei20@gmail.com",
          "job": "Frontend Developer",
          "shortlisted": 4,
      },
      {
          "interviewer": "Sara Ahmed",
          "email": "sara.ahmed08@gmail.com",
          "job": "Designer",
          "shortlisted": 12,
      },
      {
          "interviewer": "Ahona Deo",
          "email": "ahona.deo10@gmail.com",
          "job": "Backend Developer",
          "shortlisted": 5,
      },
  ]

  return df_perf, pending_requests, recent_applicants, recent_hirings


df, pending_requests, recent_applicants, recent_hirings = load_data()

# 5. Main Content Rendering
if page == "Dashboard":
  # Header
  col_title, col_notif, col_user = st.columns([8, 1, 1])
  with col_title:
    st.markdown("## Recruitment Analytics")
  with col_notif:
    st.markdown("🔔")
  with col_user:
    st.markdown("👤")

  st.markdown("---")

  # Top Row: Candidate Performance & KPI Metric Cards
  top_left, top_right = st.columns([2, 1])

  with top_left:
    st.markdown(
        "<div class='custom-card'><h4>Candidate Performance</h4>",
        unsafe_allow_html=True,
    )

    # Time filter buttons (Weekly, Monthly, Yearly)
    time_filter = st.radio(
        "Timeframe",
        ["Weekly", "Monthly", "Yearly"],
        horizontal=True,
        label_visibility="collapsed",
    )

    # Adjust chart data based on filter
    if time_filter == "Weekly":
      chart_df = pd.DataFrame(
          {
              "month": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
              "applications": [10, 25, 15, 30, 22, 18, 12],
          }
      )
    elif time_filter == "Yearly":
      chart_df = pd.DataFrame(
          {"month": ["2023", "2024", "2025", "2026"], "applications": [180, 240, 310, 420]}
      )
    else:
      chart_df = df

    # Plotly Line Chart with red theme
    fig = px.line(
        chart_df,
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
        height=260,
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

  with top_right:
    col_m1, col_m2 = st.columns(2)
    with col_m1:
      st.metric(
          label="Total Job Posted", value="248", delta="This Month", delta_color="off"
      )
      st.metric(
          label="Get Hired", value="120", delta="This Month", delta_color="off"
      )
    with col_m2:
      st.metric(
          label="Applied Candidates",
          value="2K",
          delta="This Month",
          delta_color="off",
      )
      st.metric(
          label="Today Interviews", value="56", delta="Today", delta_color="off"
      )

  # Middle Row: Job Statistics, Recent Applicants, Recent Hirings
  mid_col1, mid_col2, mid_col3 = st.columns([1, 1, 1.3])

  with mid_col1:
    st.markdown(
        "<div class='custom-card'><h4>Job Statistics</h4>",
        unsafe_allow_html=True,
    )
    # Donut Chart for Male/Female Candidates
    fig_donut = go.Figure(
        data=[
            go.Pie(
                labels=["Male Candidates", "Female Candidates"],
                values=[1234, 1754],
                hole=0.7,
                marker_colors=["#ff4b4b", "#4b9cd3"],
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
                text="<b>Total<br>2988</b>",
                x=0.5,
                y=0.5,
                font_size=14,
                showarrow=False,
                font_color="white",
            )
        ],
    )
    st.plotly_chart(fig_donut, use_container_width=True)
    st.markdown(
        "<p style='text-align: center; font-size: 13px;'>Male Candidates: <b>1,234</b> (▲ 0.3%) &nbsp;|&nbsp; Female Candidates: <b>1,754</b> (▼ 0.1%)</p>",
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

  with mid_col2:
    st.markdown(
        "<div class='custom-card'><h4>Recent Applicants</h4>",
        unsafe_allow_html=True,
    )
    for applicant in recent_applicants:
      col_av, col_info, col_btn = st.columns([1, 3, 2])
      with col_av:
        st.markdown(f"<span style='font-size:24px;'>{applicant['avatar']}</span>", unsafe_allow_html=True)
      with col_info:
        st.markdown(f"**{applicant['name']}**<br><span style='font-size:11px; color:gray;'>{applicant['role']}</span>", unsafe_allow_html=True)
      with col_btn:
        if st.button("Schedule", key=f"sch_{applicant['name']}"):
          st.success(f"Interview scheduled for {applicant['name']}!")
      st.markdown("<hr style='margin: 5px 0; border-color: #282c37;'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

  with mid_col3:
    st.markdown(
        "<div class='custom-card'><h4>Recent Hirings</h4>",
        unsafe_allow_html=True,
    )
    # Header row
    r_h1, r_h2, r_h3 = st.columns([3, 2, 1])
    r_h1.markdown("**Interviewer**")
    r_h2.markdown("**Job Title**")
    r_h3.markdown("**Shortlisted**")
    st.markdown("<hr style='margin: 5px 0; border-color: #282c37;'>", unsafe_allow_html=True)

    for hiring in recent_hirings:
      h_c1, h_c2, h_c3 = st.columns([3, 2, 1])
      with h_c1:
        st.markdown(f"**{hiring['interviewer']}**<br><span style='font-size:10px; color:gray;'>{hiring['email']}</span>", unsafe_allow_html=True)
      with h_c2:
        st.markdown(f"{hiring['job']}")
      with h_c3:
        st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{hiring['shortlisted']}")
      st.markdown("<hr style='margin: 5px 0; border-color: #282c37;'>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

  # Bottom Row: Pending Request Approvals Table
  st.markdown(
      "<div class='custom-card'><h4>Pending Request Approvals</h4>",
      unsafe_allow_html=True,
  )
  
  # Table headers
  t_cols = st.columns([2, 1.5, 2, 1, 1, 1.5, 1, 1])
  headers = ["Position", "Experience", "Department", "Profile Rating", "No.of Vacancies", "Apply Date", "Status", "Action"]
  for col, h in zip(t_cols, headers):
    col.markdown(f"**{h}**")
  
  st.markdown("<hr style='margin: 5px 0; border-color: #282c37;'>", unsafe_allow_html=True)

  # Table rows with interactive Accept buttons
  for idx, req in enumerate(pending_requests):
    cols = st.columns([2, 1.5, 2, 1, 1, 1.5, 1, 1])
    cols[0].markdown(req["Position"])
    cols[1].markdown(req["Experience"])
    cols[2].markdown(req["Department"])
    cols[3].markdown(req["Rating"])
    cols[4].markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;{req['Vacancies']}")
    cols[5].markdown(req["Date"])
    
    status_color = "#28a745" if req["Status"] == "Open" else "#dc3545"
    cols[6].markdown(f"<span style='color: {status_color}; font-weight: bold;'>{req['Status']}</span>", unsafe_allow_html=True)
    
    with cols[7]:
      if st.button("Accept", key=f"accept_{idx}"):
        st.toast(f"Approved request for {req['Position']}!")
        
    st.markdown("<hr style='margin: 5px 0; border-color: #282c37;'>", unsafe_allow_html=True)

  st.markdown("</div>", unsafe_allow_html=True)

elif page == "Candidates":
  st.markdown("## Candidates Management")
  st.info("Candidate database and filtering tools go here.")

elif page == "Hiring":
  st.markdown("## Hiring Pipeline")
  st.info("Manage active interview rounds and job openings.")

elif page == "Reports":
  st.markdown("## Analytics & Reports")
  st.info("Export detailed recruitment metrics and reports.")

elif page == "Settings":
  st.markdown("## Dashboard Settings")
  st.info("Configure user permissions, integrations, and branding.")