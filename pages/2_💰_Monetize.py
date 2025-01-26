import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import load_css

######################################################################################
# Page configurations
######################################################################################

st.set_page_config(
    page_title="Monetize",
    page_icon="💰",
    layout="wide",
)

load_css()

# Initialize selected_idea as None if not exists
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None

st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Monetization</h1>
        <p class="header-subtitle">VC STYLE FINANCIAL MODELING</p>
        <hr class="header-divider">
    </div>
""", unsafe_allow_html=True)

# Add selectbox with None as initial state
add_selectbox = st.selectbox(
   "Which idea are you working on?",     
   options=["AI for dogs", "startups for toddlers"],
   index=None,
   placeholder="Select an idea",
   key="selected_idea"
)

st.sidebar.image(
    "/Users/alexmayo/Documents/my_projects/launchpad/launchpad.png", 
    width=None,
    use_container_width=True
)

# Stop rendering if no idea selected
if st.session_state.selected_idea is None:
    st.stop()

######################################################################################
# Tabs
######################################################################################

tab1, tab2 = st.tabs(["Financial Inputs", "Financial Projections"])

with tab1:
    st.markdown("""
        <div style="font-family: 'Geist', sans-serif;">
        <h3>Revenue Model Analysis</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("monetization_analysis"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Market & Competition**")
            market_size = st.number_input(
                "Total Addressable Market (TAM) in $M",
                min_value=0.0,
                format="%.1f",
                value=100.0
            )
            
            competitors = st.number_input(
                "Number of Direct Competitors",
                min_value=0,
                step=1,
                value=5
            )
            
            market_growth = st.slider(
                "Market Growth Rate (% YoY)",
                min_value=0,
                max_value=200,
                value=20
            )

        with col2:
            st.write("**Unit Economics**")
            cac = st.number_input(
                "Est. Customer Acquisition Cost ($)",
                min_value=0.0,
                format="%.2f",
                value=100.00
            )
            
            clv = st.number_input(
                "Est. Customer Lifetime Value ($)",
                min_value=0.0,
                format="%.2f",
                value=500.00
            )
            
            gross_margin = st.slider(
                "Expected Gross Margin (%)",
                min_value=0,
                max_value=100,
                value=70
            )

        st.write("**Revenue Model**")
        pricing_model = st.radio(
            "Primary Revenue Model",
            ["SaaS/Subscription", "Transactional", "Marketplace/Commission", "Freemium", "Enterprise Licensing"]
        )
        
        if pricing_model == "SaaS/Subscription":
            col5, col6 = st.columns(2)
            with col5:
                price_tier1 = st.number_input("Basic Tier Monthly Price ($)", min_value=0.0, format="%.2f", value=10.00)
                conversion_rate1 = st.slider("Basic Tier Conversion (%)", 0, 100, 5)
            with col6:
                price_tier2 = st.number_input("Premium Tier Monthly Price ($)", min_value=0.0, format="%.2f", value=50.00)
                conversion_rate2 = st.slider("Premium Tier Conversion (%)", 0, 100, 2)

        submitted = st.form_submit_button("Generate Financial Projections")

with tab2:
    if submitted:
        st.success("Analysis complete! Generating projections...")
        
        # Create 5-year projections
        years = list(range(1, 6))
        
        # Basic growth assumptions
        monthly_growth_rate = 0.10  # 10% monthly growth
        churn_rate = 0.02  # 2% monthly churn
        
        # Calculate monthly customers and revenue
        months = list(range(1, 61))  # 5 years = 60 months
        monthly_customers = []
        monthly_revenue = []
        
        customers = 100  # Starting with 100 customers
        for month in months:
            customers = customers * (1 + monthly_growth_rate - churn_rate)
            basic_customers = customers * (conversion_rate1/100)
            premium_customers = customers * (conversion_rate2/100)
            monthly_rev = (basic_customers * price_tier1) + (premium_customers * price_tier2)
            
            monthly_customers.append(customers)
            monthly_revenue.append(monthly_rev)
        
        # Create yearly summaries
        yearly_customers = [monthly_customers[i] for i in range(11, 60, 12)]
        yearly_revenue = [sum(monthly_revenue[i-11:i+1]) for i in range(11, 60, 12)]
        
        # Display KPI Dashboard
        st.write("### Key Performance Indicators")
        
        col7, col8, col9 = st.columns(3)
        
        with col7:
            st.metric("LTV/CAC Ratio", f"{(clv/cac):.1f}x")
        with col8:
            st.metric("Gross Margin", f"{gross_margin}%")
        with col9:
            st.metric("Y5 Revenue Run Rate", f"${yearly_revenue[-1]/1000000:.1f}M")
        
        # Revenue Growth Chart
        fig = make_subplots(rows=2, cols=1, subplot_titles=('Monthly Revenue', 'Customer Growth'))
        
        fig.add_trace(
            go.Scatter(x=months, y=monthly_revenue, name="Monthly Revenue"),
            row=1, col=1
        )
        
        fig.add_trace(
            go.Scatter(x=months, y=monthly_customers, name="Total Customers"),
            row=2, col=1
        )
        
        fig.update_layout(height=600, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)
        
        # Financial Projections Table
        projections_df = pd.DataFrame({
            'Year': years,
            'Customers': [int(yearly_customers[i]) for i in range(5)],
            'Revenue': [f"${yearly_revenue[i]/1000000:.1f}M" for i in range(5)],
            'Gross Profit': [f"${(yearly_revenue[i] * gross_margin/100)/1000000:.1f}M" for i in range(5)]
        })
        
        st.write("### 5-Year Financial Projections")
        st.dataframe(projections_df.transpose(), use_container_width=True)
        
        # Sensitivity Analysis
        st.write("### Revenue Sensitivity Analysis")
        sensitivity_df = pd.DataFrame(
            index=['Low Growth (-50%)', 'Base Case', 'High Growth (+50%)'],
            columns=['Year 1', 'Year 3', 'Year 5']
        )
        
        for i, growth_mult in enumerate([0.5, 1.0, 1.5]):
            modified_revenue = [r * growth_mult for r in yearly_revenue]
            sensitivity_df.iloc[i] = [
                f"${modified_revenue[0]/1000000:.1f}M",
                f"${modified_revenue[2]/1000000:.1f}M",
                f"${modified_revenue[4]/1000000:.1f}M"
            ]
        
        st.dataframe(sensitivity_df, use_container_width=True)
