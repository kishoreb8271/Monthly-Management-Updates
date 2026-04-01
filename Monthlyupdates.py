import streamlit as st
import pandas as pd
import plotly.express as px

# Basic Page Setup
st.set_page_config(page_title="Executive Security Dashboard", layout="wide")

# --- 1. DYNAMIC DATA HANDLING ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO9Q_7kjiiayiR_SYjvDZIR_BsjGRpVjkckRbWjWXHxGzAh3Lx0hEjpxjkw8IwHQ4rPyNY4RS4Ocbn/pub?output=csv"

@st.cache_data(ttl=600) 
def get_team_data():
    try:
        df = pd.read_csv(SHEET_URL)
        # Clean numeric data just in case
        df['Progress_Value'] = pd.to_numeric(df['Progress_Value'], errors='coerce').fillna(0)
        return df
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return pd.DataFrame(columns=['Month', 'Team', 'Project', 'Status', 'Progress_Value', 'Executive_Summary', 'Metric_Value'])

df = get_team_data()

# --- 2. EXECUTIVE SIDEBAR ---
st.sidebar.title("🛠️ Control Center")
if st.sidebar.button('🔄 Refresh Live Data'):
    st.cache_data.clear()
    st.rerun()

if not df.empty:
    all_teams = df['Team'].unique()
    selected_teams = st.sidebar.multiselect("Filter by Team", options=all_teams, default=all_teams)
    
    all_months = df['Month'].unique()
    selected_month = st.sidebar.selectbox("Select Reporting Month", options=all_months)

    # Filter data dynamically
    filtered_df = df[(df['Team'].isin(selected_teams)) & (df['Month'] == selected_month)]

    # --- 3. DASHBOARD UI ---
    st.title("📊 Monthly Management Updates")
    st.markdown(f"**Teams:** {', '.join(selected_teams)} | **Reporting Period:** {selected_month} 2026")

    # Top Row Metrics (The "At a Glance" view)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Projects", len(filtered_df))
    m2.metric("✅ Completed", len(filtered_df[filtered_df['Status'] == 'Completed']))
    m3.metric("⏳ In Progress", len(filtered_df[filtered_df['Status'] == 'In Progress']))
    m4.metric("❌ Pending", len(filtered_df[filtered_df['Status'] == 'Pending']))

    st.divider()

    # --- 4. TEAM SPECIFIC INSIGHTS (The "Effective" Way) ---
    st.subheader("🛡️ Strategic Team Insights")
    c1, c2 = st.columns(2)

    with c1:
        if "VAPT" in selected_teams:
            vapt_data = filtered_df[filtered_df['Team'] == 'VAPT']
            st.info("**VAPT Focus:** Focus on critical remediation and reducing the attack surface.")
            # Example metric from a 'Metric_Value' column if you add it to your sheet
            st.metric
