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
            'idea name': "AI Customer Support Bot",
            'details': "An intelligent chatbot that handles customer queries 24/7, using natural language processing to understand and respond to customer needs. Features personalized responses based on customer history.",
            'type': "🤖 AI",
            'viability score': "0.57",
            'status': "Ideation",
            'customers': "0",
            'revenue': "$0",
            'created_date': "2024-01-20 09:30",
            'last_modified': "2024-01-25 14:15"
        },
        {
            'idea name': "Virtual Try-Before-Buy",
            'details': "AR-powered platform allowing customers to virtually test products before purchase. Includes size recommendations, style matching, and real-time visualization.",
            'type': "🔍 MarTech",
            'viability score': "0.46",
            'status': "Validating",
            'customers': "0",
            'revenue': "$0",
            'created_date': "2024-01-10 15:45",
            'last_modified': "2024-01-22 16:30"
        },
        {
            'idea name': "Gamified User Rewards",
            'details': "Loyalty program that turns product interactions into a game. Users earn points, badges, and rewards for completing tasks, writing reviews, and referring friends.",
            'type': "🤖 AI",
            'viability score': "0.71",
            'status': "Launched",
            'customers': "46",
            'revenue': "$1,300",
            'created_date': "2023-12-01 10:00",
            'last_modified': "2024-01-20 09:45"
        },
    ]
    st.session_state.ideas = pd.DataFrame(example_ideas)

# Function to add new idea
def add_idea(name, details, category, status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    new_idea = pd.DataFrame([{
        'idea name': name,
        'details': details,
        'type': category,
        'viability score': "0",
        'status': status,
        'customers': "0",
        'revenue': "$0",
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
        mask = df['name'].str.contains(search, case=False) | df['details'].str.contains(search, case=False)
        df = df[mask]
    if status_filter:
        df = df[df['status'].isin(status_filter)]
    
    # Display table with custom formatting
    st.dataframe(
        df,
        column_config={
            "idea name": st.column_config.TextColumn(
                "Idea Name",
                pinned=True,
                width="medium",
                help="Name of the idea"
            ),
            "details": st.column_config.TextColumn(
                "Details",
                width="medium",
                help="Description of the idea"
            ),
            "type": st.column_config.SelectboxColumn(
                "Type",
                help="Category/market", 
                width="small",
                options=[
                    "📊 SaaS",
                    "📈 eCommerce", 
                    "🤖 AI",
                    "🔍 MarTech",
                    "💰 FinTech",
                    "🏠 PropTech",
                ],
                required=True,
            ),
            "viability score": st.column_config.NumberColumn(
                "Viability Score",
                format="%.2f",
                width="small",
                help="Viability score"
            ),
            "status": st.column_config.SelectboxColumn(
                "Status",
                options=["Ideation", "Validating", "Pivoted", "Abandoned", "Launched"],
                width="small"
            ),
            "customers": st.column_config.NumberColumn(
                "Customers",
                format="%d",
                width="small",
                help="Number of customers"
            ),
            "revenue": st.column_config.NumberColumn(
                "Revenue",
                format="$%d",
                width="small",
                help="Revenue generated"
            ),
            "created_date": st.column_config.DatetimeColumn(
                "Created",
                format="MM/DD/YY",
                width="small"
            ),
            "last_modified": st.column_config.DatetimeColumn(
                "Last Modified",
                format="MM/DD/YY",
                width="small"
            )
        },
        hide_index=True,
        use_container_width=True
    )
else:
    st.info("No ideas yet! Click 'Add New Idea' to get started!")

# Add custom CSS to reduce spacing
st.markdown("""
    <style>
        div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stDataFrame"]) {
            margin-bottom: -2rem;
        }
    </style>
    """, unsafe_allow_html=True)

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
        type = st.selectbox(
            "Type",
            options=[
                "📊 SaaS",
                "📈 eCommerce", 
                "🤖 AI",
                "🔍 MarTech",
                "💰 FinTech",
                "🏠 PropTech",
            ]
        )
        
        submitted = st.form_submit_button("Add Idea", type="secondary", use_container_width=True)
        if submitted and name and description:
            add_idea(name, description, type, "Ideation")
            st.session_state.show_success = True
            st.rerun()

# Show success message if flag is set
if 'show_success' in st.session_state and st.session_state.show_success:
    st.success("✨ Idea added successfully!")
    st.session_state.show_success = False

# Add button to move to ideate page
if st.button("Let's Model 💰 →", type="primary", use_container_width=True):
    st.switch_page("pages/2_💰_Financials.py") 