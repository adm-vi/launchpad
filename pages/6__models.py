import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import load_css
import random
from datetime import datetime, timedelta

######################################################################################
# page configurations
######################################################################################

st.set_page_config(
    page_title="models",
    page_icon="🎯",
    layout="wide",
)

load_css()

st.logo(
    "images/sunglasses.png",
    size="large",
    link="https://streamlit.io/gallery",
)

st.sidebar.image(
    "images/launchpad.png", 
    width=None,  # Remove width to auto-fill
    use_container_width=True  # Makes image fill width of sidebar
)

st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Models</h1>
        <p class="header-subtitle">HOW DO WE STACK UP?</p>
        <hr class="header-divider">
    </div>
""", unsafe_allow_html=True
)

# Initialize selected_idea as None if not exists
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None

# Add selectbox with None as initial state
add_selectbox = st.selectbox(
   "Which idea are you working on?",     
   options=["Acme Corp.", "Vandelay Industries"],
   index=None,
   placeholder="Select an idea",
   key="selected_idea"
)

# Stop rendering if no idea selected
if st.session_state.selected_idea is None:
    st.stop()

######################################################################################

# Get selected idea from sidebar
selected_idea = st.session_state.selected_idea

# Create tabs
tab0, tab1, tab2, tab3, tab4 = st.tabs(["Inputs", "Customers", "Revenues", "Expenses", "Summary"])

# Inputs
with tab0:
    st.markdown("### Revenue Assumptions")

    st.markdown("##### Product A Assumptions")
    col1, space, col2 = st.columns([1, 0.2, 1])

    with col1:
        st.markdown("##### Year 1")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("Price/Month ($):"); col1b.number_input(label="price", label_visibility="collapsed", value=10, key="product_a_price")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("MoM Growth Rate (%):"); col1b.number_input(label="growth", label_visibility="collapsed", value=15, key="product_a_growth")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("MoM Churn Rate (%):"); col1b.number_input(label="churn", label_visibility="collapsed", value=10, key="product_a_churn")

    with col2:
        st.markdown("##### Year 2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("Price/Month ($):"); col2b.number_input(label="price", label_visibility="collapsed", value=12, key="product_a_price_2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("MoM Growth Rate (%):"); col2b.number_input(label="growth", label_visibility="collapsed", value=15, key="product_a_growth_2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("MoM Churn Rate (%):"); col2b.number_input(label="churn", label_visibility="collapsed", value=8, key="product_a_churn_2")
    
    st.markdown("##### Product B Assumptions")
    col1, space, col2 = st.columns([1, 0.2, 1])

    with col1:
        st.markdown("##### Year 1")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("Price/Month ($):"); col1b.number_input(label="price", label_visibility="collapsed", value=5, key="product_b_price")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("MoM Growth Rate (%):"); col1b.number_input(label="growth", label_visibility="collapsed", value=20, key="product_b_growth")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("MoM Churn Rate (%):"); col1b.number_input(label="churn", label_visibility="collapsed", value=10, key="product_b_churn")

    with col2:
        st.markdown("##### Year 2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("Price/Month ($):"); col2b.number_input(label="price", label_visibility="collapsed", value=7, key="product_b_price_2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("MoM Growth Rate (%):"); col2b.number_input(label="growth", label_visibility="collapsed", value=20, key="product_b_growth_2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("MoM Churn Rate (%):"); col2b.number_input(label="churn", label_visibility="collapsed", value=8, key="product_b_churn_2")

    st.divider()
    st.markdown("### Expense Assumptions")

# Customers
with tab1:
    # Input metrics for customer growth
    st.markdown("### Customer Growth Model")
    col1, col2 = st.columns(2)

    with col1:
        monthly_growth_rate = st.slider("Monthly Customer Growth Rate (%)", 0, 20, 10) / 100
        initial_customers = st.number_input("Initial Customers", value=100)
        initial_price = st.number_input("Initial Price ($)", value=10)

    with col2:
        monthly_churn_rate = st.slider("Monthly Churn Rate (%)", 0, 10, 3) / 100

    # Generate month labels (next 24 months)
    start_date = datetime.now()
    months = [(start_date + timedelta(days=30*i)).strftime('%b-%y') for i in range(24)]

    # Initialize lists for calculations
    starting_customers = []
    new_customers = []
    churned_customers = []
    ending_customers = []

    # Calculate customer metrics for each month
    current_customers = initial_customers

    for i in range(24):
        # Starting customers (same as previous month's ending customers)
        starting_customers.append(current_customers)
        
        # New customers (based on previous month's ending customers)
        new_customer_count = round(current_customers * monthly_growth_rate)
        new_customers.append(new_customer_count)
        
        # Churned customers
        churned_customer_count = round(current_customers * monthly_churn_rate)
        churned_customers.append(-churned_customer_count)
        
        # Ending customers
        current_customers = current_customers + new_customer_count - churned_customer_count
        ending_customers.append(current_customers)

    # Create customer growth dataframe
    customer_data = {
        'Metric': [
            'Starting Customers',
            'New Customers',
            'Churned Customers',
            'Ending Customers'
        ]
    }

    # Add data for each month
    for i, month in enumerate(months):
        customer_data[month] = [
            f"{starting_customers[i]:,.0f}",
            f"{new_customers[i]:,.0f}",
            f"{churned_customers[i]:,.0f}",
            f"{ending_customers[i]:,.0f}"
        ]

    customer_df = pd.DataFrame(customer_data)

    # Display customer growth overview
    st.dataframe(customer_df, use_container_width=True)

# Revenues
with tab2:
    # Revenues
    avg_revenue = st.number_input("Average Monthly Revenue per Customer ($)", value=50)

    mrr_data = {
        'Metric': [
            'Starting MRR',
            'New MRR', 
            'Churned MRR',
            'Ending MRR'
        ]
    }

    # Add data for each month
    for i, month in enumerate(months):
        mrr_data[month] = [
            f"${starting_customers[i] * avg_revenue:,.0f}",
            f"${new_customers[i] * avg_revenue:,.0f}", 
            f"${churned_customers[i] * avg_revenue:,.0f}",
            f"${ending_customers[i] * avg_revenue:,.0f}"
        ]

    mrr_df = pd.DataFrame(mrr_data)

    st.markdown("### Monthly Recurring Revenue")
    st.dataframe(mrr_df, use_container_width=True)

# Expenses
with tab3:
    st.markdown("### Expenses")
    st.info("Coming soon! This tab will contain cost modeling features.")

# Summary
with tab4:
    st.markdown("### Summary")
    st.info("Coming soon! This tab will contain summary features.")
