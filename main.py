import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -----------------------------------------------------------------------------
# Configuration & Setup
# -----------------------------------------------------------------------------
st.set_page_config(page_title="COVID-19 Analytics Dashboard", layout="wide")
# Custom CSS for "Fluid" UI
st.markdown("""
<style>
    .main { background-color: #f5f5f5; }
    .st-emotion-cache-16idsys p { font-size: 1.1rem; }
    div[data-testid="stMetricValue"] { font-size: 2rem; color: #2c3e50; }
    h1, h2, h3 { color: #2c3e50; font-family: 'Segoe UI', sans-serif; }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Data Loading (Cached for Performance)
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    # Loading the main dataset
    df = pd.read_csv('covid_19_data.csv')
    df['ObservationDate'] = pd.to_datetime(df['ObservationDate'])
    
    # Preprocessing: Calculate Active Cases
    df['Active'] = df['Confirmed'] - df['Deaths'] - df['Recovered']
    
    # Cleaning Country Names for consistency (optional handling)
    df['Country/Region'] = df['Country/Region'].replace('Mainland China', 'China')
    
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Dataset files not found. Please ensure 'covid_19_data.csv' is in the directory.")
    st.stop()

# -----------------------------------------------------------------------------
# Sidebar: Navigation, Filters & Key Terms
# -----------------------------------------------------------------------------
st.sidebar.title("Disease Spread/ Covid Analysis")

# 1. Navigation
page = st.sidebar.radio("Navigate", ["Global Overview", "Nation Analysis", "Raw Data"])

st.sidebar.markdown("---")

# 2. Filters (Global scope or specific depending on page, but kept here for UI consistency)
st.sidebar.subheader("Date Filter")
min_date = df['ObservationDate'].min().date()
max_date = df['ObservationDate'].max().date()
start_date, end_date = st.sidebar.date_input("Select Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data based on date
mask = (df['ObservationDate'].dt.date >= start_date) & (df['ObservationDate'].dt.date <= end_date)
df_filtered = df.loc[mask]

st.sidebar.markdown("---")

# 3. Key Terms / Glossary (As requested)
with st.sidebar.expander("Key Terms & Definitions", expanded=True):
    st.markdown("""
    **Confirmed**: Total cumulative positive cases.
    
    **Active**: Currently infected (`Confirmed - Deaths - Recovered`).
    
    **Recovered**: People who have healed.
    
    **Deaths**: Fatalities attributed to COVID-19.
    
    **Mortality Rate**: `(Deaths / Confirmed) * 100`
    """)

st.sidebar.info("Designed by Gaurav Khadka")

# -----------------------------------------------------------------------------
# Main Interface: Logic based on Selection
# -----------------------------------------------------------------------------

if page == "Global Overview":
    st.title("Global Pandemic Overview")
    
    # Latest snapshot for KPI
    latest_date = df_filtered['ObservationDate'].max()
    df_latest = df_filtered[df_filtered['ObservationDate'] == latest_date]
    global_stats = df_latest.groupby('ObservationDate')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()

    if not global_stats.empty:
        total_confirmed = int(global_stats['Confirmed'].iloc[0])
        total_deaths = int(global_stats['Deaths'].iloc[0])
        total_recovered = int(global_stats['Recovered'].iloc[0])
        total_active = int(global_stats['Active'].iloc[0])
        
        # KPI Row
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Confirmed", f"{total_confirmed:,}", delta_color="off")
        col2.metric("Total Active", f"{total_active:,}", delta_color="inverse")
        col3.metric("Total Recovered", f"{total_recovered:,}", delta_color="normal")
        col4.metric("Total Deaths", f"{total_deaths:,}", delta_color="inverse")

    # Global Trend Chart
    st.subheader("Global Trends Over Time")
    global_trend = df_filtered.groupby('ObservationDate')[['Confirmed', 'Recovered', 'Deaths']].sum().reset_index()
    
    fig_trend = px.line(global_trend, x='ObservationDate', y=['Confirmed', 'Recovered', 'Deaths'], 
                        title='Global Accumulation of Cases',
                        labels={'value': 'Count', 'ObservationDate': 'Date', 'variable': 'Category'},
                        color_discrete_map={'Confirmed': '#3498db', 'Recovered': '#2ecc71', 'Deaths': '#e74c3c'})
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Top Countries Bar Chart
    st.subheader("Top Affected Nations")
    country_totals = df_latest.groupby('Country/Region')['Confirmed'].sum().reset_index().sort_values('Confirmed', ascending=False).head(10)
    fig_bar = px.bar(country_totals, x='Confirmed', y='Country/Region', orientation='h', 
                     text='Confirmed', color='Confirmed', color_continuous_scale='Viridis',
                     title=f"Top 10 Countries by Confirmed Cases (as of {latest_date.date()})")
    fig_bar.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig_bar, use_container_width=True)


elif page == "Nation Analysis":
    st.title("Nation-Specific Analysis")
    
    # Country Selector
    country_list = sorted(df['Country/Region'].unique())
    selected_country = st.selectbox("Select a Nation to Analyze:", country_list, index=country_list.index('US') if 'US' in country_list else 0)
    
    # Filter Data for Nation
    df_country = df_filtered[df_filtered['Country/Region'] == selected_country]
    
    # Aggregation for the specific country
    country_trend = df_country.groupby('ObservationDate')[['Confirmed', 'Deaths', 'Recovered', 'Active']].sum().reset_index()
    
    if not country_trend.empty:
        # Latest stats for the country
        latest_c = country_trend.iloc[-1]
        
        # Custom Cards for Country
        st.markdown(f"### Current Status: {selected_country}")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Confirmed", f"{int(latest_c['Confirmed']):,}")
        c2.metric("Active", f"{int(latest_c['Active']):,}")
        c3.metric("Recovered", f"{int(latest_c['Recovered']):,}")
        c4.metric("Deaths", f"{int(latest_c['Deaths']):,}")
        
        # Tabs for detailed views
        tab1, tab2 = st.tabs(["Trends", "Rate Analysis"])
        
        with tab1:
            st.subheader(f"Trajectory in {selected_country}")
            fig_ct = go.Figure()
            fig_ct.add_trace(go.Scatter(x=country_trend['ObservationDate'], y=country_trend['Confirmed'], name='Confirmed', line=dict(color='#3498db')))
            fig_ct.add_trace(go.Scatter(x=country_trend['ObservationDate'], y=country_trend['Active'], name='Active', line=dict(color='#f1c40f', dash='dash')))
            fig_ct.add_trace(go.Scatter(x=country_trend['ObservationDate'], y=country_trend['Deaths'], name='Deaths', line=dict(color='#e74c3c')))
            st.plotly_chart(fig_ct, use_container_width=True)
            
        with tab2:
            st.subheader("Efficiency Metrics")
            country_trend['Recovery Rate'] = (country_trend['Recovered'] / country_trend['Confirmed']) * 100
            country_trend['Mortality Rate'] = (country_trend['Deaths'] / country_trend['Confirmed']) * 100
            
            fig_rates = px.line(country_trend, x='ObservationDate', y=['Recovery Rate', 'Mortality Rate'],
                                color_discrete_map={'Recovery Rate': 'green', 'Mortality Rate': 'red'},
                                title=f"Recovery vs Mortality Rate in {selected_country}")
            st.plotly_chart(fig_rates, use_container_width=True)

elif page == "Raw Data":
    st.title("Dataset Explorer")
    st.write("View the raw data filtered by your date selection.")
    st.dataframe(df_filtered)
    
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button("Download Filtered CSV", data=csv, file_name="filtered_covid_data.csv", mime="text/csv")