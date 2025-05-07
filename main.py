import streamlit as st
from utils.page_config import init_page, setup_page_content

######################################################################################
# page configurations
######################################################################################

# Must be called first
init_page('main')

# Setup the page content
setup_page_content('main')

######################################################################################
# Header
######################################################################################

st.markdown("""
    <div style="
        width: 100%;
        margin: -0.5rem 0 0.5rem 0;
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 0.75rem;
    ">
        <div style="
            font-family: 'Geist', sans-serif;
            color: #555;
        ">
            <p style="font-size: 1rem; line-height: 1.4; margin: 0 0 1rem 0; text-align: left;">
                Forget Y-Combinator, forget about co-founders, and forget about years-long product discovery.
            </p>
            <p style="font-size: 1rem; line-height: 1.4; margin: 0; text-align: left;">
                Get started in minutes with our guided process:<br><br>
                <span style="font-size: 0.9rem;">• Brainstorm and validate your ideas<br>
                • Project your financials and market fit<br>
                • Create a compelling pitch deck<br>
                • Get AI-powered feedback</span>
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

######################################################################################
# Feature Cards
######################################################################################

# Define features
features = [
    {"title": "Idea Journal", "icon": "📓", "description": "Your ideas in one place"},
    {"title": "Financial Projections", "icon": "💰", "description": "Back-of-the-napkin financial projections"},
    {"title": "Business Model Canvas", "icon": "🎯", "description": "Your business model on a single page"},
    {"title": "Feedback", "icon": "🛠️", "description": "Proceed or pivot"},
]

# Define upcoming features
features_row_2 = [
    {"title": "Ideation", "icon": "💡", "description": "AI-powered whiteboard"},
    {"title": "Benchmarks", "icon": "🎯", "description": "Compare your idea to the competition"},
    {"title": "User Research", "icon": "💭", "description": "AI-simulated feedback from your first users"}
]

# Create a single row of 4 equal cards
cols = st.columns(4)
for i, col in enumerate(cols):
    feature = features[i]
    with col:
        st.markdown(f"""
        <div class="feature-card" style="
            height: 200px !important;
            margin: 0.5rem 0;
            padding: 1rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 0.5rem;
            background: white;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        ">
            <div style="font-family: 'Funnel Display', sans-serif; font-weight: bold; font-size: 1.1em; margin-bottom: 0.5rem;">
                {feature["title"]}<span style="float: right;">{feature["icon"]}</span>
            </div>
            <div style="color: #666; font-size: 0.9em;">{feature["description"]}</div>
        </div>
        """, unsafe_allow_html=True)


# Create a second row of 3 equal cards for upcoming features
cols_upcoming = st.columns([1.33, 1.33, 1.33])
for i, col in enumerate(cols_upcoming):
    feature = features_row_2[i]
    with col:
        st.markdown(f"""
        <div class="feature-card" style="
            height: 120px;
            margin: 0.5rem 0;
            padding: 0.7rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
            border-radius: 0.5rem;
            background: white;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
            opacity: 0.7;
        ">
            <div style="font-family: 'Funnel Display', sans-serif; font-weight: bold; font-size: 1.1em; margin-bottom: 0.5rem;">
                {feature["title"]}<span style="float: right;">{feature["icon"]}</span>
            </div>
            <div style="color: #666; font-size: 0.9em;">{feature["description"]}</div>
            <div style="color: #ff0000; font-size: 0.8em; font-style: italic; font-weight: bold; margin-top: 0.5rem;">Coming soon</div>
        </div>
        """, unsafe_allow_html=True)
