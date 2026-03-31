import streamlit as st
import pandas as pd
import plotly.express as px

# Basic Page Setup
st.set_page_config(page_title="Executive Dashboard", layout="wide")

# --- 1. DYNAMIC DATA HANDLING ---
# In a real scenario, replace the 'data' dictionary with:
# pd.read_csv('your_s3_bucket_link_or_local_path.csv')
def get_team_data():
    data = {
        'Team': ['IAM', 'Cloud Ops', 'GRC', 'Network Security', 'IAM', 'GRC'],
        'Project': ['Role Cleanup', 'S3 Logging', 'Audit Prep', 'Firewall Refresh', 'SSO Migration', 'Policy Update'],
        'Status': ['In Progress', 'Completed', 'Pending', 'In Progress', 'Completed', 'In Progress'],
        'Progress_Value': [65, 100, 10, 40, 100, 55],
        'Month': ['March', 'March', 'March', 'March', 'March', 'March']
    }
    return pd.DataFrame(data)

df = get_team_data()

# --- 2. EXECUTIVE SIDEBAR ---
st.sidebar.title("Dashboard Controls")
all_teams = df['Team'].unique()
selected_teams = st.sidebar.multiselect("Filter by Team", options=all_teams, default=all_teams)
selected_month = st.sidebar.selectbox("Reporting Month", options=df['Month'].unique())

# Filter data dynamically
filtered_df = df[(df['Team'].isin(selected_teams)) & (df['Month'] == selected_month)]

# --- 3. DASHBOARD UI ---
st.title("📊 Monthly Executive Updates")
st.markdown(f"**Viewing updates for:** {', '.join(selected_teams)} | **Period:** {selected_month}")

# Top Row Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Teams", len(selected_teams))
col2.metric("✅ Completed", len(filtered_df[filtered_df['Status'] == 'Completed']))
col3.metric("⏳ In Progress", len(filtered_df[filtered_df['Status'] == 'In Progress']))
col4.metric("❌ Pending", len(filtered_df[filtered_df['Status'] == 'Pending']))

st.divider()

# Visual Progress Chart
st.subheader("Project Status Visualizer")
fig = px.bar(
    filtered_df, 
    x='Project', 
    y='Progress_Value', 
    color='Status',
    text='Progress_Value',
    color_discrete_map={'Completed': '#28a745', 'In Progress': '#ffc107', 'Pending': '#dc3545'}
)
st.plotly_chart(fig, use_container_width=True)

# Detailed Data Table
st.subheader("Activity List & Project Details")
st.table(filtered_df[['Team', 'Project', 'Status', 'Progress_Value']])

# --- 4. SUGGESTION FOR TRACKING ---
st.info("""
**Pro-Tip for Progress Tracking:** To keep this dynamic, host a CSV file on a shared drive or AWS S3. 
Update the `get_team_data()` function to pull from that URL so the dashboard 
updates automatically whenever a team lead changes the source file.
""")
