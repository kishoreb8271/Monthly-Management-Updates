import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Page Config
st.set_page_config(page_title="Executive Security Dashboard", layout="wide", initial_sidebar_state="expanded")

# 2. Dynamic Data Fetching
SHEET_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQO9Q_7kjiiayiR_SYjvDZIR_BsjGRpVjkckRbWjWXHxGzAh3Lx0hEjpxjkw8IwHQ4rPyNY4RS4Ocbn/pub?output=csv"

@st.cache_data(ttl=300)
def load_data():
    try:
        data = pd.read_csv(SHEET_URL)
        # Ensure numeric types
        data['Progress_Value'] = pd.to_numeric(data['Progress_Value'], errors='coerce').fillna(0)
        return data
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return pd.DataFrame()

df = load_data()

# 3. Sidebar Controls
st.sidebar.title("🛂 Dashboard Controls")
if st.sidebar.button('🔄 Sync Live Data'):
    st.cache_data.clear()
    st.rerun()

if not df.empty:
    # Get unique lists for filtering
    all_months = df['Month'].unique().tolist()
    all_teams = df['Team'].unique().tolist()

    selected_month = st.sidebar.selectbox("Select Reporting Month", options=all_months, index=len(all_months)-1)
    selected_teams = st.sidebar.multiselect("Select Teams", options=all_teams, default=all_teams)

    # 4. Data Logic for MoM Comparison
    current_df = df[(df['Month'] == selected_month) & (df['Team'].isin(selected_teams))]
    
    # Calculate Previous Month Data for Delta
    prev_month_idx = all_months.index(selected_month) - 1
    if prev_month_idx >= 0:
        prev_month = all_months[prev_month_idx]
        prev_df = df[(df['Month'] == prev_month) & (df['Team'].isin(selected_teams))]
        prev_complete = len(prev_df[prev_df['Status'] == 'Completed'])
    else:
        prev_complete = 0

    # 5. UI: Main Header
    st.title("📊 Cyber Security & GRC Executive Summary")
    st.markdown(f"**Reporting Period:** {selected_month} | **Status:** Live")
    
    # 6. Executive KPI Row (With Deltas)
    curr_complete = len(current_df[current_df['Status'] == 'Completed'])
    delta_val = curr_complete - prev_complete

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric("Active Projects", len(current_df))
    kpi2.metric("✅ Completed", curr_complete, delta=f"{delta_val} vs last month")
    kpi3.metric("⏳ In Progress", len(current_df[current_df['Status'] == 'In Progress']))
    kpi4.metric("❌ Pending", len(current_df[current_df['Status'] == 'Pending']), delta_color="inverse")

    st.divider()

    # 7. Visual Insights
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("🚀 Project Velocity & Progress")
        fig = px.bar(
            current_df, 
            x='Project', 
            y='Progress_Value', 
            color='Status',
            text=current_df['Progress_Value'].apply(lambda x: f'{int(x)}%'),
            color_discrete_map={'Completed': '#28a745', 'In Progress': '#ffc107', 'Pending': '#dc3545'},
            template="plotly_white"
        )
        fig.update_layout(yaxis_range=[0, 110], showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader("⚠️ Risk Concentration")
        if 'Risk_Level' in current_df.columns:
            risk_fig = px.pie(current_df, names='Risk_Level', hole=0.4,
                             color='Risk_Level',
                             color_discrete_map={'High': '#d62728', 'Medium': '#ff7f0e', 'Low': '#2ca02c'})
            st.plotly_chart(risk_fig, use_container_width=True)
        else:
            st.info("Add a 'Risk_Level' column to your Sheet to see the Risk Breakdown.")

    # 8. Detailed Activity List
    st.subheader("📝 Detailed Monthly Activity Log")
    st.dataframe(
        current_df[['Team', 'Project', 'Status', 'Progress_Value', 'Executive_Summary' if 'Executive_Summary' in current_df.columns else 'Project']], 
        use_container_width=True, 
        hide_index=True
    )

else:
    st.error("Could not load data. Please verify your Google Sheet link.")

st.caption("Confidential Executive Report | Generated via Streamlit")
