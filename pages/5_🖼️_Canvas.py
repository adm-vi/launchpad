import streamlit as st
from utils.page_config import init_page, setup_page_content

# Initialize the page
init_page('canvas')
setup_page_content('canvas')

# Create two columns for the top row
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])

with col1:
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Key Partnerships</p>", unsafe_allow_html=True)
    st.text_area("List your key partners and suppliers", key="partnerships", height=200)
    
with col2:
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Key Activities</p>", unsafe_allow_html=True)
    st.text_area("What key activities does your value proposition require?", key="activities", height=90)
    
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Key Resources</p>", unsafe_allow_html=True)
    st.text_area("What key resources does your value proposition require?", key="resources", height=90)
    
with col3:
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Value Propositions</p>", unsafe_allow_html=True)
    st.text_area("What value do you deliver to your customers?", key="value_prop", height=200)
    
with col4:
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Customer Relationships</p>", unsafe_allow_html=True)
    st.text_area("What type of relationship does each customer segment expect?", key="relationships", height=90)
    
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Channels</p>", unsafe_allow_html=True)
    st.text_area("Through which channels do your customer segments want to be reached?", key="channels", height=90)
    
with col5:
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Customer Segments</p>", unsafe_allow_html=True)
    st.text_area("Who are you creating value for?", key="segments", height=200)

# Create two columns for the bottom row
col6, col7 = st.columns(2)

with col6:
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Cost Structure</p>", unsafe_allow_html=True)
    st.text_area("What are the most important costs in your business model?", key="costs", height=150)
    
with col7:
    st.markdown("<p style='font-family: \"Geist Mono\", monospace; font-size: 1.25rem; font-weight: bold;'>Revenue Streams</p>", unsafe_allow_html=True)
    st.text_area("For what value are your customers willing to pay?", key="revenue", height=150)
