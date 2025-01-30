import streamlit as st
import pandas as pd
from datetime import datetime
from utils.page_config import init_page, setup_page_content

# Must be called first
init_page('ideas')

# Then setup the rest of the page
setup_page_content('ideas')

# Initialize session state for ideas if not exists
if 'ideas' not in st.session_state:
    # Create example ideas
    example_ideas = [
        {
            'name': "AI Customer Support Bot",
            'description': "An intelligent chatbot that handles customer queries 24/7, using natural language processing to understand and respond to customer needs. Features personalized responses based on customer history.",
            'status': "Ideation",
            'created_date': "2024-01-20 09:30",
            'last_modified': "2024-01-25 14:15"
        },
        {
            'name': "Smart Product Packaging",
            'description': "Eco-friendly packaging system with QR codes that link to product information, usage tutorials, and sustainability metrics. Includes augmented reality features for interactive unboxing experience.",
            'status': "Ideation",
            'created_date': "2024-01-15 11:20",
            'last_modified': "2024-01-15 11:20"
        },
        {
            'name': "Virtual Try-Before-Buy",
            'description': "AR-powered platform allowing customers to virtually test products before purchase. Includes size recommendations, style matching, and real-time visualization.",
            'status': "Validating",
            'created_date': "2024-01-10 15:45",
            'last_modified': "2024-01-22 16:30"
        },
        {
            'name': "Gamified User Rewards",
            'description': "Loyalty program that turns product interactions into a game. Users earn points, badges, and rewards for completing tasks, writing reviews, and referring friends.",
            'status': "Launched",
            'created_date': "2023-12-01 10:00",
            'last_modified': "2024-01-20 09:45"
        },
        {
            'name': "Market Segmentation Tool",
            'description': "Data-driven tool for identifying and prioritizing target audiences. Analyzes customer behavior, demographics, and market trends to suggest optimal market segments.",
            'status': "Pivoted",
            'created_date': "2023-11-15 13:20",
            'last_modified': "2024-01-18 11:30"
        }
    ]
    st.session_state.ideas = pd.DataFrame(example_ideas)

# Function to add new idea
def add_idea(name, description, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_idea = pd.DataFrame([{
        'name': name,
        'description': description,
        'status': status,
        'created_date': now,
        'last_modified': now
    }])
    st.session_state.ideas = pd.concat([st.session_state.ideas, new_idea], ignore_index=True)

# Display Ideas Table
if not st.session_state.ideas.empty:
    
    # Add filters
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("🔍 Search Ideas", placeholder="Search by name or description")
    with col2:
        status_filter = st.multiselect(
            "Filter by Status",
            options=["Ideation", "Validating", "Pivoted", "Abandoned", "Launched"],
            default=[]
        )
    
    # Filter the dataframe
    df = st.session_state.ideas.copy()
    if search:
        mask = df['name'].str.contains(search, case=False) | df['description'].str.contains(search, case=False)
        df = df[mask]
    if status_filter:
        df = df[df['status'].isin(status_filter)]
    
    # Display table with custom formatting
    st.dataframe(
        df,
        column_config={
            "name": "Name",
            "description": st.column_config.TextColumn(
                "Description",
                width="large",
                help="Detailed description of the idea"
            ),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=["Ideation", "Validating", "Pivoted", "Abandoned", "Launched"],
                width="small"
            ),
            "created_date": st.column_config.DatetimeColumn(
                "Created",
                format="DD/MM/YY HH:mm",
                width="small"
            ),
            "last_modified": st.column_config.DatetimeColumn(
                "Last Modified",
                format="DD/MM/YY HH:mm",
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("No ideas yet! Click 'Add New Idea' to get started!")

st.markdown("---")

# New Idea Form in Expander
with st.expander("➕ Add New Idea", expanded=False):
    with st.form("new_idea_form"):
        name = st.text_input("Idea Name", placeholder="Enter a catchy name for your idea")
        description = st.text_area(
            "Description",
            placeholder="Describe your idea, its unique features, and potential market applications",
            height=100
        )
        
        submitted = st.form_submit_button("Add Idea", type="secondary", use_container_width=True)
        if submitted and name and description:
            add_idea(name, description, "Ideation")  # Default status to "Ideation"
            st.success("✨ Idea added successfully!")
            st.rerun()

# Add button to move to ideate page
if st.button("Let's Model 💰 →", type="primary", use_container_width=True):
    st.switch_page("pages/2_💰_Financials.py") 