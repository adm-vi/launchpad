import streamlit as st
import pandas as pd
import random
from utils import load_css

######################################################################################
# Initialize session state
######################################################################################

# Initialize idea metrics if not exists
if 'idea_metrics' not in st.session_state:
    st.session_state.idea_metrics = {
        'AI for dogs': {
            'viability_score': random.uniform(0.7, 0.95),
            'predicted_profit': random.randint(200000, 800000),
            'cash_burn': random.randint(150000, 600000),
            'time_to_breakeven': random.randint(12, 36),
            'strengths': [
                'Strong market demand',
                'Clear value proposition',
                'Innovative technology'
            ],
            'improvements': [
                'Marketing strategy refinement',
                'Customer acquisition optimization',
                'Product feature expansion'
            ]
        },
        'startups for toddlers': {
            'viability_score': random.uniform(0.6, 0.9),
            'predicted_profit': random.randint(100000, 600000),
            'cash_burn': random.randint(100000, 400000),
            'time_to_breakeven': random.randint(18, 42),
            'strengths': [
                'Unique market positioning',
                'Growing target market',
                'Strong brand potential'
            ],
            'improvements': [
                'Product development acceleration',
                'Distribution channel optimization',
                'Market penetration strategy'
            ]
        }
    }

# Initialize selected_idea as None if not exists
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None

######################################################################################
# Page Configuration
######################################################################################

st.set_page_config(
    page_title="Investment Committee",
    page_icon="📋",
    layout="wide",
)

load_css()

######################################################################################
# Header and Branding
######################################################################################

st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Investment Committee</h1>
        <p class="header-subtitle">FEEDBACK FROM LAUNCHPAD</p>
        <hr class="header-divider">
    </div>
""", unsafe_allow_html=True)

# Add selectbox with None as initial state
add_selectbox = st.selectbox(
   "Which idea are you working on?",     
   options=["AI for dogs", "startups for toddlers"],
   index=None,  # This makes it start empty
   placeholder="Select an idea",  # This shows as placeholder text
   key="selected_idea"
)

st.logo(
    "images/sunglasses.png",
    size="large",
    link="https://streamlit.io/gallery",
)

st.sidebar.image(
    "images/launchpad.png", 
    width=None,
    use_container_width=True
)

######################################################################################
# Data Access
######################################################################################

# Get metrics once and use throughout the page
metrics = st.session_state.idea_metrics.get(st.session_state.selected_idea, {})
if not metrics or st.session_state.selected_idea is None:  # Check for None
    st.stop()

######################################################################################
# Project Overview Card
######################################################################################

st.markdown(f"""
    <div class="gradient-card" style='display:flex; align-items:center;'>
        <div style='flex:1'>
            <h3 style='margin-left:20px; margin-bottom:0px'>{st.session_state.selected_idea}</h3>
            <small style='color:#fff; margin-left:30px; font-family:monospace;'>Selected Project</small>
        </div>
        <div style='background:{"rgba(46, 125, 50, 0.2)" if metrics["viability_score"]>=0.7 else "rgba(245, 124, 0, 0.2)"}; padding:8px 15px; border-radius:15px; text-align:center; margin-right:20px'>
            <div style='font-weight:bold; font-family:monospace; font-size: 1.8em; color:{"#fff"}'>{metrics['viability_score']:.2f}</div>
            <small style='color:#fff; font-family:monospace; font-size: 1.0em'>Viability</small>
        </div>
    </div>
""", unsafe_allow_html=True)

######################################################################################
# Metrics Cards
######################################################################################

st.markdown(f"""
    <div style='display: flex; gap: 20px; margin-bottom: 20px;'>
        <div style='
            flex: 1;
            padding: 15px;
            border-radius: 15px;
            background: linear-gradient(135deg, #fff9c4 0%, #ffffff 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 1.2em; color: #2C3E50; margin-bottom: 2px;'>💰</div>
            <h4 style='color: #2C3E50; margin: 0 0 8px 0; font-size: 0.9em;'>Predicted Profit</h4>
            <div style='background: rgba(248,249,250,0.7); padding: 8px; border-radius: 8px;'>
                <p style='margin: 0; font-size: 1.1em;'><span class="header-subtitle">${metrics['predicted_profit']:,}</span></p>
                <p style='margin: 2px 0 0 0; color: #666; font-size: 0.8em;'>24 Month Projection</p>
            </div>
        </div>
        <div style='
            flex: 1;
            padding: 15px;
            border-radius: 15px;
            background: linear-gradient(135deg, #fff9c4 0%, #ffffff 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 1.2em; color: #2C3E50; margin-bottom: 2px;'>🔥</div>
            <h4 style='color: #2C3E50; margin: 0 0 8px 0; font-size: 0.9em;'>Monthly Burn</h4>
            <div style='background: rgba(248,249,250,0.7); padding: 8px; border-radius: 8px;'>
                <p style='margin: 0; font-size: 1.1em;'><b>${metrics['cash_burn']:,}</b></p>
                <p style='margin: 2px 0 0 0; color: #666; font-size: 0.8em;'>Current Rate</p>
            </div>
        </div>
        <div style='
            flex: 1;
            padding: 15px;
            border-radius: 15px;
            background: linear-gradient(135deg, #fff9c4 0%, #ffffff 100%);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        '>
            <div style='font-size: 1.2em; color: #2C3E50; margin-bottom: 2px;'>⏱️</div>
            <h4 style='color: #2C3E50; margin: 0 0 8px 0; font-size: 0.9em;'>Breakeven</h4>
            <div style='background: rgba(248,249,250,0.7); padding: 8px; border-radius: 8px;'>
                <p style='margin: 0; font-size: 1.1em;'><b>{metrics['time_to_breakeven']} months</b></p>
                <p style='margin: 2px 0 0 0; color: #666; font-size: 0.8em;'>Time to Profitability</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

######################################################################################
# Investment Readiness Assessment
######################################################################################

st.markdown("""
<style>
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin: 10px 0;
    font-family: 'Courier New', Courier, monospace;
}
.metric-value {
    font-size: 24px;
    font-weight: bold;
}
.metric-delta {
    font-size: 14px;
    margin-top: 5px;
}
</style>
""", unsafe_allow_html=True)

# Calculate metrics
clv_cac = 3.5
growth_rate = 15
churn_rate = 5
arr = metrics['predicted_profit']
burn_rate = metrics['cash_burn']
runway_months = arr / burn_rate * 12 if burn_rate > 0 else float('inf')
low_val = arr * 5
high_val = arr * (10 if growth_rate > 50 else 7)

# First row of metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div>CLV/CAC Ratio</div>
        <div class="metric-value">{clv_cac:.1f}x</div>
        <div class="metric-delta" style="color: {'green' if clv_cac >= 3 else 'red'}">
            {"Good" if clv_cac >= 3 else "Needs Improvement"}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div>Growth Rate</div>
        <div class="metric-value">{growth_rate}%</div>
        <div class="metric-delta" style="color: {'green' if growth_rate > 10 else 'red'}">
            {"Good" if growth_rate > 10 else "Needs Improvement"}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div>Churn Rate</div>
        <div class="metric-value">{churn_rate}%</div>
        <div class="metric-delta" style="color: {'green' if churn_rate < 8 else 'red'}">
            {"Good" if churn_rate < 8 else "Needs Improvement"}
        </div>
    </div>
    """, unsafe_allow_html=True)

# Second row of metrics
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div>ARR</div>
        <div class="metric-value">${arr:,.0f}</div>
        <div class="metric-delta" style="color: {'green' if arr > 1000000 else 'orange'}">
            {"Series A Ready" if arr > 1000000 else "Seed Stage"}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="metric-card">
        <div>Runway</div>
        <div class="metric-value">{runway_months:.1f} months</div>
        <div class="metric-delta" style="color: {'green' if runway_months > 12 else 'red'}">
            {"Healthy" if runway_months > 12 else "Fundraise Soon"}
        </div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="metric-card">
        <div>Valuation Range</div>
        <div class="metric-value">${low_val/1000000:.1f}M - ${high_val/1000000:.1f}M</div>
        <div class="metric-delta">Based on current metrics</div>
    </div>
    """, unsafe_allow_html=True)

######################################################################################
# Strategic Analysis
######################################################################################

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
        <div class="gradient-card">
                <h3>Core Strengths</h3>
                <div class="content">
                    {''.join([f"<div class='item'><span style='color:#28a745;font-weight:bold'>✓</span> {strength}</div>" for strength in metrics['strengths']])}
                </div>
        </div>
    """, unsafe_allow_html=True)
        
with col2:
    st.markdown(f"""
        <div class="gradient-card">
                <h3>Growth Opportunities</h3>
                <div class="content">
                    {''.join([f"<div class='item'><span style='color:#28a745;font-weight:bold'>○</span> {improvement}</div>" for improvement in metrics['improvements']])}
                </div>
        </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
        <div class="gradient-card">
                <h3>Strategic Recommendations</h3>
                <div class="content">
                    <div class='item'><span style='color:#28a745;font-weight:bold'>○</span> <b>Primary Focus:</b> {metrics['improvements'][0]}</div>
                    <div class='item'><span style='color:#28a745;font-weight:bold'>○</span> <b>Leverage Point:</b> {metrics['strengths'][0]}</div>
                    <div class='item'><span style='color:#28a745;font-weight:bold'>○</span> <b>Timeline:</b> Target breakeven within {metrics['time_to_breakeven']} months</div>
                    <div class='item'><span style='color:#28a745;font-weight:bold'>○</span> <b>Risk Level:</b> {'High attention needed' if metrics['time_to_breakeven'] > 24 else 'Standard oversight'}</div>
                </div>
        </div>
""", unsafe_allow_html=True)

# Create a container with the button and text stacked vertically
st.markdown("""
    <div style='display: flex; flex-direction: column; align-items: flex-end; margin-top: 20px;'>
""", unsafe_allow_html=True)

# Add the button
if st.button("🪦 Pivot", type="secondary"):
    st.switch_page("pages/1_📓_Ideas.py")

# Add the text below
st.markdown("""
        <div style='font-style: italic; color: #666; font-size: 0.9em; margin-top: 8px;'>
            "better to have tried and failed than to never have tried at all"
        </div>
    </div>
""", unsafe_allow_html=True)



