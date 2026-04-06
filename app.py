import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page Config
st.set_page_config(
    page_title="Ferry Analytics Dashboard",
    page_icon="⛴️",
    layout="wide"
)

# ── Load Data
@st.cache_data
def load_data():
    df = pd.read_csv('data/ferry_processed.csv')
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    return df

df = load_data()

# ── Sidebar Filters
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/37/Flag_of_Toronto.svg/200px-Flag_of_Toronto.svg.png", width=100)
st.sidebar.title("⛴️ Ferry Analytics")
st.sidebar.markdown("---")

selected_years = st.sidebar.multiselect(
    "Select Year(s)",
    options=sorted(df['Year'].unique()),
    default=sorted(df['Year'].unique())
)

selected_seasons = st.sidebar.multiselect(
    "Select Season(s)",
    options=['Spring','Summer','Fall','Winter'],
    default=['Spring','Summer','Fall','Winter']
)

granularity = st.sidebar.radio(
    "Granularity",
    options=['15-min', 'Hourly', 'Daily'],
    index=1
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data Source:** Toronto Open Data")
st.sidebar.markdown("**Period:** 2015–2026")

# ── Filter Data
filtered = df[
    (df['Year'].isin(selected_years)) &
    (df['Season'].isin(selected_seasons))
]

# ── Title
st.title("⛴️ Ferry Capacity Utilization & Operational Efficiency")
st.markdown("**Jack Layton Ferry Terminal — Toronto Island Ferry Analytics**")
st.markdown("---")

# ── KPI Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Records", f"{len(filtered):,}")
with col2:
    util = filtered['Operational_Load_Index'].mean() * 100
    st.metric("Avg Utilization", f"{util:.1f}%")
with col3:
    cong = (filtered['Is_Congested'].sum() / len(filtered)) * 100
    st.metric("Congestion Rate", f"{cong:.1f}%", delta="⚠️ High" if cong > 20 else "✅ OK")
with col4:
    idle = (filtered['Is_Idle'].sum() / len(filtered)) * 100
    st.metric("Idle Rate", f"{idle:.1f}%")
with col5:
    avg_activity = filtered['Total_Activity'].mean()
    st.metric("Avg Activity/Interval", f"{avg_activity:.0f}")

st.markdown("---")

# ── Row 1: Timeline + Season Bar
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Activity Timeline by Year")
    yearly = filtered.groupby('Year')['Total_Activity'].sum().reset_index()
    fig1 = px.bar(yearly, x='Year', y='Total_Activity',
                  color='Total_Activity', color_continuous_scale='Blues',
                  title='Total Ferry Activity Per Year')
    fig1.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🌍 Activity by Season")
    seasonal = filtered.groupby('Season')['Total_Activity'].mean().reset_index()
    season_order = ['Spring','Summer','Fall','Winter']
    seasonal['Season'] = pd.Categorical(seasonal['Season'], categories=season_order, ordered=True)
    seasonal = seasonal.sort_values('Season')
    fig2 = px.bar(seasonal, x='Season', y='Total_Activity',
                  color='Season',
                  color_discrete_map={
                      'Spring':'#2ecc71','Summer':'#f39c12',
                      'Fall':'#e74c3c','Winter':'#3498db'
                  })
    fig2.update_layout(showlegend=False, height=350)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Heatmap + Pie
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔥 Activity Heatmap — Hour vs Day")
    pivot = filtered.pivot_table(
        values='Total_Activity',
        index='Hour', columns='DayOfWeek', aggfunc='mean'
    ).round(1)
    pivot.columns = ['Mon','Tue','Wed','Thu','Fri','Sat','Sun']
    fig3 = px.imshow(pivot, color_continuous_scale='YlOrRd',
                     labels=dict(x="Day", y="Hour", color="Avg Activity"),
                     aspect='auto')
    fig3.update_layout(height=400)
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("⚡ Operational Status")
    normal = len(filtered[(filtered['Is_Idle']==0) & (filtered['Is_Congested']==0)])
    fig4 = go.Figure(data=[go.Pie(
        labels=['Normal','Idle','Congested'],
        values=[normal, filtered['Is_Idle'].sum(), filtered['Is_Congested'].sum()],
        hole=0.4,
        marker_colors=['#3498db','#95a5a6','#e74c3c']
    )])
    fig4.update_layout(height=400)
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Hourly Pattern
st.subheader("⏰ Average Activity by Hour of Day")
hourly = filtered.groupby('Hour')['Total_Activity'].mean().reset_index()
fig5 = px.line(hourly, x='Hour', y='Total_Activity',
               markers=True, line_shape='spline',
               color_discrete_sequence=['#e74c3c'])
fig5.add_hrect(y0=hourly['Total_Activity'].quantile(0.75),
               y1=hourly['Total_Activity'].max(),
               fillcolor="red", opacity=0.1,
               annotation_text="Congestion Zone")
fig5.update_layout(height=300)
st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.caption("Built by Inderjeet | Ferry Capacity Utilization & Operational Efficiency Analytics | Data: Toronto Open Data")


# ── ML Forecasting Section
st.markdown("---")
st.subheader("🤖 ML Demand Forecasting — Random Forest")

ml_df = pd.read_csv('data/ferry_daily_ml.csv')
ml_df['Date'] = pd.to_datetime(ml_df['Date'])

col1, col2 = st.columns(2)

with col1:
    # Actual vs Predicted
    last_365 = ml_df.tail(365)
    fig_ml = go.Figure()
    fig_ml.add_trace(go.Scatter(
        x=last_365['Date'], y=last_365['Total_Activity'],
        name='Actual', line=dict(color='steelblue', width=2)
    ))
    fig_ml.add_trace(go.Scatter(
        x=last_365['Date'], y=last_365['RF_Predicted'],
        name='Predicted', line=dict(color='red', width=2, dash='dash')
    ))
    fig_ml.update_layout(
        title='Actual vs Predicted — Last 365 Days',
        height=400,
        legend=dict(orientation='h')
    )
    st.plotly_chart(fig_ml, use_container_width=True)

with col2:
    # Feature importance
    features = ['Year','Month','DayOfWeek','IsWeekend',
                'DayOfYear','Season_Code','Lag_7','Lag_14','Rolling_7']
    importance = [0.01, 0.00, 0.07, 0.06, 0.04, 0.00, 0.05, 0.04, 0.78]
    imp_df = pd.DataFrame({'Feature': features, 'Importance': importance})
    imp_df = imp_df.sort_values('Importance', ascending=True)
    
    fig_imp = px.bar(imp_df, x='Importance', y='Feature',
                     orientation='h', color='Importance',
                     color_continuous_scale='Blues',
                     title='Feature Importance')
    fig_imp.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_imp, use_container_width=True)

# Model metrics
m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Model", "Random Forest")
with m2:
    st.metric("Features Used", "9")
with m3:
    st.metric("Training Period", "2015–2024")