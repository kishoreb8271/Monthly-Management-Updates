import streamlit as st
import pandas as pd
import plotly.express as px

# Basic Page Setup
st.set_page_config(page_title="Executive Dashboard", layout="wide")

# --- 1. DYNAMIC DATA HANDLING ---
# Your Google Sheets CSV Link (Converted from pubhtml to pub?output=csv)
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO9Q_7kjiiayiR_SYjvDZIR_BsjGRpVjkckRbWjWXHxGzAh3Lx0hEjpxjkw8IwHQ4rPyNY4RS4Ocbn/pub?output=csv"

@st.cache_data(ttl=600)  # Caches data for 10 minutes to stay fast but stay updated
def get_team_data():
    try:
        # Pulls directly from the live Google Sheet
        df = pd.read_csv(SHEET_URL)
        return df
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        # Fallback empty dataframe with correct columns if connection fails
        return pd.DataFrame(columns=['Month', 'Team', 'Project', 'Status', 'Progress_Value'])

df = get_team_data()

# --- 2. EXECUTIVE SIDEBAR ---
st.sidebar.title("Dashboard Controls")

# Added a refresh button so executives can force an update
if st.sidebar.button('🔄 Refresh Data'):
    st.cache_data.clear()
    st.rerun()

if not df.empty:
    all_teams = df['Team'].unique()
    selected_teams = st.sidebar.multiselect("Filter by Team", options=all_teams, default=all_teams)
    
    all_months = df['Month'].unique()
    selected_month = st.sidebar.selectbox("Reporting Month", options=all_months)

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
    if not filtered_df.empty:
        fig = px.bar(
            filtered_df, 
            x='Project', 
            y='Progress_Value', 
            color='Status',
            text='Progress_Value',
            # Ensures colors stay consistent with the status
            color_discrete_map={'Completed': '#28a745', 'In Progress': '#ffc107', 'Pending': '#dc3545'}
        )
        st.plotly_chart(fig, use_container_width=True)

        # Detailed Data Table
        st.subheader("Activity List & Project Details")
        st.table(filtered_df[['Team', 'Project', 'Status', 'Progress_Value']])
    else:
        st.warning("No data found for the selected filters.")

else:
    st.warning("The data source is empty or could not be loaded. Check your Google Sheet headers.")

# --- 4. TRACKING INFO ---
st.info("""
**Note:** Changes made in the Google Sheet may take a few minutes to appear due to Google's 
publishing delay and the app's 10-minute cache. Click **'Refresh Data'** in the sidebar to sync manually.
""")
