import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup Page Configuration
st.set_page_config(page_title="Executive Team Dashboard", layout="wide")

# 2. Mock Data Generator (In a real scenario, use: pd.read_csv('updates.csv'))
def load_data():
    data = {
        'Team': ['IAM', 'Cloud Security', 'GRC', 'IAM', 'GRC', 'Cloud Security'],
        'Project': ['SSO Integration', 'S3 Bucket Encryption', 'NIST Audit', 'PAM Setup', 'Policy Review', 'Lambda Security'],
        'Status': ['Completed', 'In Progress', 'Pending', 'In Progress', 'Completed', 'In Progress'],
        'Update_Month': ['March', 'March', 'March', 'March', 'March', 'March'],
        'Progress_Percent': [100, 45, 10, 60, 100, 30]
    }
    return pd.DataFrame(data)

df = load_data()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Dashboard Filters")
selected_team = st.sidebar.multiselect("Select Teams", options=df['Team'].unique(), default=df['Team'].unique())
selected_month = st.sidebar.selectbox("Select Month", options=df['Update_Month'].unique())

# Filter dataframe based on selection
filtered_df = df[(df['Team'].isin(selected_team)) & (df['Update_Month'] == selected_month)]

# --- MAIN DASHBOARD ---
st.title("🚀 Executive Monthly Updates")
st.markdown(f"**Reporting Period:** {selected_month} 2026")

# 3. Key Metrics (Number of Teams & Status)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Teams", len(selected_team))
col2.metric("Completed", len(filtered_df[filtered_df['Status'] == 'Completed']))
col3.metric("In Progress", len(filtered_df[filtered_df['Status'] == 'In Progress']))
col4.metric("Pending", len(filtered_df[filtered_df['Status'] == 'Pending']))

st.divider()

# 4. Visual Progress Chart
st.subheader("Team Activity Overview")
fig = px.bar(
    filtered_df, 
    x='Project', 
    y='Progress_Percent', 
    color='Status',
    text='Progress_Percent',
    barmode='group',
    color_discrete_map={'Completed': '#2ca02c', 'In Progress': '#ff7f0e', 'Pending': '#d62728'}
)
st.plotly_chart(fig, use_container_width=True)

# 5. Activity List / Projects Table
st.subheader("Detailed Activity List")
st.dataframe(
    filtered_df[['Team', 'Project', 'Status', 'Progress_Percent']], 
    use_container_width=True,
    hide_index=True
)

# 6. Progress Tracking Suggestion
with st.expander("💡 How to track progress updates?"):
    st.write("""
    1. **Centralized Data:** Use an AWS S3 bucket to host a `status.json` or `data.csv`.
    2. **Automation:** Set up an n8n workflow or a Python script to pull updates from team Slack channels or Jira.
    3. **Standardized Input:** Ensure every team uses the same status labels: `Completed`, `In Progress`, and `Pending`.
    """)