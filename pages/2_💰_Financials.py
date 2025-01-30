import random
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.page_config import init_page, setup_page_content
from utils.utils import load_css

# Must be called first
init_page('financials')

# Then setup the rest of the page
setup_page_content('financials')

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

    col1, space, col2 = st.columns([1, 0.2, 1])

    with col1:
        st.markdown("##### Year 1")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("Price/Month ($):"); col1b.number_input(label="price", label_visibility="collapsed", value=10, key="product_price")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("MoM Growth Rate (%):"); col1b.number_input(label="growth", label_visibility="collapsed", value=25, key="product_growth")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("MoM Churn Rate (%):"); col1b.number_input(label="churn", label_visibility="collapsed", value=10, key="product_churn")
        col1a, col1b, space = st.columns([4, 3, 2]); col1a.write("Starting Customers (#):"); col1b.number_input(label="customers", label_visibility="collapsed", value=10, key="product_customers")

    with col2:
        st.markdown("##### Year 2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("Price/Month ($):"); col2b.number_input(label="price", label_visibility="collapsed", value=12, key="product_a_price_2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("MoM Growth Rate (%):"); col2b.number_input(label="growth", label_visibility="collapsed", value=15, key="product_a_growth_2")
        col2a, col2b, space = st.columns([4, 3, 2]); col2a.write("MoM Churn Rate (%):"); col2b.number_input(label="churn", label_visibility="collapsed", value=8, key="product_a_churn_2")
    
    st.divider()
    st.markdown("### Expense Assumptions")

# Financials
with tab1:
    st.markdown("### Financials")
    price_1 = st.session_state.product_price
    growth_1 = st.session_state.product_growth / 100
    churn_1 = st.session_state.product_churn / 100
    initial_customers = st.session_state.product_customers
    price_2 = st.session_state.product_a_price_2
    growth_2 = st.session_state.product_a_growth_2 / 100
    churn_2 = st.session_state.product_a_churn_2 / 100

    # Generate month labels (next 24 months)
    start_date = datetime.now()
    # Using calendar months instead of fixed 30-day intervals to avoid skipping February
    months = []
    for i in range(12):
        # Add months one at a time to properly handle month transitions
        next_date = start_date.replace(day=1) + pd.DateOffset(months=i)
        months.append(next_date.strftime('%b-%y'))

    # Initialize lists for calculations
    starting_customers = []
    new_customers = []
    churned_customers = []
    ending_customers = []
    monthly_revenue = []

    # Calculate customer metrics for each month
    current_customers = initial_customers

    for i in range(12):
        # Starting customers (same as previous month's ending customers)
        if i == 0:
            starting_customers.append(initial_customers)
        else:
            starting_customers.append(ending_customers[i-1])
        
        # New customers (based on previous month's ending customers)
        new_customer_count = round(current_customers * growth_1)
        new_customers.append(new_customer_count)
        
        # Churned customers
        churned_customer_count = round(current_customers * churn_1)
        churned_customers.append(-churned_customer_count)
        
        # Ending customers
        current_customers = current_customers + new_customer_count - churned_customer_count
        ending_customers.append(current_customers)

        # Monthly revenue
        monthly_revenue.append(current_customers * price_1)

    # Create customer growth dataframe
    customer_data = {
        'Metric': [
            'Starting Customers',
            'New Customers',
            'Churned Customers',
            'Ending Customers',
            'Monthly Revenue'
        ]
    }

    # Add data for each month
    for i, month in enumerate(months):
        customer_data[month] = [
            f"{starting_customers[i]:,.0f}",
            f"{new_customers[i]:,.0f}",
            f"{churned_customers[i]:,.0f}",
            f"{ending_customers[i]:,.0f}",
            f"${monthly_revenue[i]:,.0f}"
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

    # Display KPI Dashboard
    st.write("### Key Performance Indicators")
    
    col7, col8, col9 = st.columns(3)
    
    with col7:
        st.metric("LTV/CAC Ratio", "4x")
    with col8:
        st.metric("Gross Margin", "60%")
    with col9:
        st.metric("Runway", "12 months")
    
    # Revenue Growth Chart
    fig = make_subplots(rows=2, cols=1, subplot_titles=('Monthly Revenue', 'Customer Growth'))
    
    fig.add_trace(
        go.Scatter(x=months, y=monthly_revenue, name="Monthly Revenue"),
        row=1, col=1
    )