import streamlit as st
import pandas as pd
import pickle
import os
from chart_builder import build_forecast_chart, build_pie_chart, build_bar_chart
from narrative_generator import generate_narrative

st.set_page_config(
    page_title="AI Demand Forecast Narrator",
    page_icon="📦",
    layout="wide"
)

@st.cache_data(show_spinner="Loading 23MB Retail Dataset (this takes ~15 seconds on first run)...")
def load_retail_data():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, 'Online Retail.xlsx')
    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        # Clean data
        df = df[df['Quantity'] > 0]
        df = df.dropna(subset=['Description'])
        df['TotalSales'] = df['Quantity'] * df['UnitPrice']
        return df
    return pd.DataFrame()

@st.cache_data(show_spinner="Loading Historical Data & Forecasts...")
def load_data():
    base_dir = os.path.dirname(__file__)
    weekly_df = pd.read_csv(os.path.join(base_dir, 'weekly_revenue.csv'))
    forecast_df = pd.read_csv(os.path.join(base_dir, 'forecast_output.csv'))
    stats_df = pd.read_csv(os.path.join(base_dir, 'stats_summary.csv'))
    
    weekly_df['ds'] = pd.to_datetime(weekly_df['ds'])
    forecast_df['ds'] = pd.to_datetime(forecast_df['ds'])
    
    # Clip yhat, yhat_lower, yhat_upper to 0 minimum
    for col in ['yhat', 'yhat_lower', 'yhat_upper']:
        if col in forecast_df.columns:
            forecast_df[col] = forecast_df[col].clip(lower=0)
            
    return weekly_df, forecast_df, stats_df

@st.cache_resource(show_spinner="Loading AI Prophet Model...")
def load_model():
    base_dir = os.path.dirname(__file__)
    try:
        with open(os.path.join(base_dir, 'prophet_model.pkl'), 'rb') as f:
            model = pickle.load(f)
        return model
    except ModuleNotFoundError:
        # The prophet module is not installed as per instructions.
        # Since the model is not used for prediction, we return None to avoid crashing the app.
        return None
    except Exception as e:
        return None

weekly_df, forecast_df, stats_df = load_data()
model = load_model()
retail_df = load_retail_data()

stats = stats_df.iloc[0].to_dict() if not stats_df.empty else {}

# Sidebar
st.sidebar.title("⚙️ About")
st.sidebar.markdown("""
**Dataset:** Weekly Revenue  
**Forecast Model:** Facebook Prophet  
**LLM:** Gemini 1.5 Flash  
**UI Framework:** Streamlit
""")
st.sidebar.markdown("---")
st.sidebar.markdown("""
**Pipeline:**
1. Process Historical Data
2. Generate Prophet Forecast
3. Extract Key Statistics
4. AI Narrative Generation
""")
st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Interactive Filters")
if not retail_df.empty:
    countries = sorted(retail_df['Country'].unique().tolist())
    # Default to a few countries to avoid overwhelming the initial pie chart
    default_countries = ['United Kingdom', 'Germany', 'France'] if 'United Kingdom' in countries else countries[:3]
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=countries,
        default=default_countries
    )
    
    if selected_countries:
        filtered_df = retail_df[retail_df['Country'].isin(selected_countries)]
    else:
        filtered_df = retail_df
else:
    filtered_df = pd.DataFrame()

st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ AI Report Configuration")
forecast_horizon = st.sidebar.slider("Forecast Horizon (Weeks)", min_value=1, max_value=12, value=12)

# Calculate dynamic stats based on selection
last_hist_date = weekly_df['ds'].max()
future_forecast = forecast_df[forecast_df['ds'] > last_hist_date].sort_values('ds')
selected_future = future_forecast.head(forecast_horizon)
forecast_total_dynamic = selected_future['yhat'].sum()

weekly_sorted = weekly_df.sort_values('ds', ascending=False)
prior_n = weekly_sorted.head(forecast_horizon)
prior_n_total = prior_n['y'].sum()

forecast_change_pct_dynamic = 0
if prior_n_total > 0:
    forecast_change_pct_dynamic = ((forecast_total_dynamic - prior_n_total) / prior_n_total) * 100
    
top_country_dynamic = stats.get('top_country', 'N/A')
top_products_dynamic = stats.get('top_products', 'N/A')
if not filtered_df.empty:
    try:
        top_country_dynamic = filtered_df.groupby('Country')['TotalSales'].sum().idxmax()
        top_products_dynamic = " | ".join(filtered_df.groupby('Description')['Quantity'].sum().nlargest(3).index.tolist())
    except:
        pass

dynamic_stats = stats.copy()
dynamic_stats['forecast_horizon'] = forecast_horizon
dynamic_stats['forecast_total'] = round(forecast_total_dynamic, 2)
dynamic_stats['prior_n_total'] = round(prior_n_total, 2)
dynamic_stats['forecast_change_pct'] = round(forecast_change_pct_dynamic, 2)
dynamic_stats['top_country'] = top_country_dynamic
dynamic_stats['top_products'] = top_products_dynamic

st.sidebar.markdown("---")
generate_btn = st.sidebar.button("▶ Generate AI Report", type="primary", use_container_width=True)

# Main Area
st.title("📦 AI Demand Forecast Narrative Generator")
st.caption("PS-SL1 | Supply Chain & Logistics | Team B8")
st.markdown("---")

st.subheader("📊 Forecast Summary")
col1, col2, col3, col4 = st.columns(4)

total_revenue = stats.get('total_revenue', 0)
forecast_total = stats.get('forecast_total', 0)
forecast_change_pct = stats.get('forecast_change_pct', 0)
peak_week = stats.get('peak_week', 'N/A')
peak_value = stats.get('peak_value', 0)
trend_direction = str(stats.get('trend_direction', 'N/A')).capitalize()

try:
    total_rev_float = float(total_revenue)
except:
    total_rev_float = 0.0

try:
    forecast_tot_float = float(forecast_total)
    forecast_change_float = float(forecast_change_pct)
except:
    forecast_tot_float = 0.0
    forecast_change_float = 0.0

try:
    peak_val_float = float(peak_value)
    peak_val_str = f"₹{peak_val_float:,.0f}"
except:
    peak_val_str = str(peak_value)

col1.metric("Total Historical Revenue", f"₹{total_rev_float:,.0f}")
col2.metric(
    "12-Week Forecast", 
    f"₹{forecast_tot_float:,.0f}", 
    f"{forecast_change_float:+.1f}% vs prior period"
)
col3.metric("Peak Week", str(peak_week), peak_val_str)
col4.metric("Current Trend", trend_direction)

st.markdown("---")

st.subheader("📈 Demand Forecast Chart")
fig = build_forecast_chart(weekly_df, forecast_df)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("📊 Interactive Data Analytics")
if not filtered_df.empty:
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.plotly_chart(build_pie_chart(filtered_df), use_container_width=True)
        
    with col_chart2:
        st.plotly_chart(build_bar_chart(filtered_df), use_container_width=True)
        
    st.markdown("---")
    st.subheader("🔮 Inventory Stock Predictions (30-Day Outlook)")
    st.markdown("Based on historical run rates (Simple Moving Average), here are the projected stock requirements for the top 10 products.")
    
    # Calculate simple moving average / run rate
    # Total days in dataset
    days_in_dataset = (filtered_df['InvoiceDate'].max() - filtered_df['InvoiceDate'].min()).days
    if days_in_dataset < 30:
        days_in_dataset = 30 # fallback
        
    # Group by product
    stock_df = filtered_df.groupby('Description').agg(
        Total_Quantity_Sold=('Quantity', 'sum'),
        Revenue_Generated=('TotalSales', 'sum')
    ).reset_index()
    
    # Calculate daily run rate and project 30 days
    stock_df['Daily_Run_Rate'] = stock_df['Total_Quantity_Sold'] / days_in_dataset
    stock_df['30_Day_Forecast_Qty'] = (stock_df['Daily_Run_Rate'] * 30).astype(int)
    
    # Sort and format
    stock_df = stock_df.sort_values('Total_Quantity_Sold', ascending=False).head(10)
    stock_df['Revenue_Generated'] = stock_df['Revenue_Generated'].apply(lambda x: f"₹{x:,.2f}")
    
    st.dataframe(
        stock_df[['Description', 'Total_Quantity_Sold', 'Revenue_Generated', '30_Day_Forecast_Qty']],
        use_container_width=True,
        hide_index=True
    )
else:
    st.warning("No data available for the selected filters.")

st.markdown("---")

st.subheader("🖼️ Additional Visual Insights")
tab1, tab2, tab3, tab4 = st.tabs(["Weekly Revenue", "Monthly Seasonality", "Forecast Chart", "Prophet Components"])
base_dir_img = os.path.dirname(__file__)

for tab, img_name in zip(
    [tab1, tab2, tab3, tab4], 
    ["weekly_revenue_raw.png", "monthly_seasonality.png", "forecast_chart.png", "prophet_components.png"]
):
    img_path = os.path.join(base_dir_img, img_name)
    if os.path.exists(img_path):
        tab.image(img_path, use_container_width=True)
    else:
        tab.info(f"{img_name} not found.")

st.markdown("---")

if generate_btn:
    with st.spinner(f"Generating custom {forecast_horizon}-week executive narrative..."):
        narrative, bullets = generate_narrative(dynamic_stats)
        st.session_state['narrative'] = narrative
        st.session_state['bullets'] = bullets

if 'narrative' in st.session_state:
    col_left, col_right = st.columns([3, 2])
    
    with col_left:
        st.subheader("📝 Executive Narrative Report")
        st.write(st.session_state['narrative'])
        
    with col_right:
        st.subheader("✅ Inventory Action Items")
        bullet_lines = st.session_state['bullets'].split('\n')
        for line in bullet_lines:
            line = line.strip()
            if line.startswith('•'):
                st.markdown(line)
                
    st.markdown("---")
    
    full_report = f"Executive Narrative Report\n\n{st.session_state['narrative']}\n\nInventory Action Items\n\n{st.session_state['bullets']}"
    
    st.download_button(
        label="⬇️ Download Full Report (.txt)",
        data=full_report,
        file_name="demand_forecast_report.txt",
        mime="text/plain"
    )
else:
    st.info("👈 Click Generate AI Report in the sidebar to produce the executive narrative.")
