import streamlit as st
import pandas as pd
from datetime import datetime
from utils import load_css

st.set_page_config(
    page_title="Ideas",
    page_icon="📝",
    layout="wide"
)

load_css()

st.logo(
    "/Users/alexmayo/Documents/my_projects/launchpad/sunglasses.png",
    size="large",
    link="https://streamlit.io/gallery",
)

st.sidebar.image(
    "/Users/alexmayo/Documents/my_projects/launchpad/launchpad.png", 
    width=None,  # Remove width to auto-fill
    use_container_width=True  # Makes image fill width of sidebar
)

st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Ideas</h1>
        <p class="header-subtitle">Manage Your Innovation Pipeline</p>
        <hr class="header-divider">
    </div>
""", unsafe_allow_html=True)

# Initialize session state for ideas if not exists
if 'ideas' not in st.session_state:
    # Create example ideas
    example_ideas = [
        {
            'name': "AI Customer Support Bot",
            'description': "An intelligent chatbot that handles customer queries 24/7, using natural language processing to understand and respond to customer needs. Features personalized responses based on customer history.",
            'status': "In Progress",
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
            options=["In Progress", "Ideation", "Validating", "Pivoted", "Abandoned", "Launched"],
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
                options=["In Progress", "Ideation", "Validating", "Pivoted", "Abandoned", "Launched"],
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
        col1, col2 = st.columns([2, 1])
        with col1:
            name = st.text_input("Idea Name", placeholder="Enter a catchy name for your idea")
            description = st.text_area(
                "Description",
                placeholder="Describe your idea, its unique features, and potential market applications",
                height=100
            )
        with col2:
            status = st.selectbox(
                "Status",
                options=["In Progress", "Ideation", "Validating", "Pivoted", "Abandoned", "Launched"],
                index=1
            )
        
        submitted = st.form_submit_button("Add Idea", type="secondary", use_container_width=True)
        if submitted and name and description:
            add_idea(name, description, status)
            st.success("✨ Idea added successfully!")
            st.rerun()

# Add button to move to ideate page
if st.button("Start Ideating 💡 →", type="primary", use_container_width=True):
    st.switch_page("pages/2_💡_Ideate.py") 