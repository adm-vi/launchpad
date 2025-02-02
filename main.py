import streamlit as st
from utils.page_config import init_page, setup_page_content

######################################################################################
# page configurations
######################################################################################

# Must be called first
init_page('main')

# Then setup the rest of the page
setup_page_content('main')

######################################################################################
# Header
######################################################################################

st.markdown("""
    <div style="
        width: 100%;
        background: linear-gradient(to bottom, #ffffff, #f8f9fa);
        border: 1px solid rgba(0, 0, 0, 0.1);
        padding: 1rem;
        margin: 0.5rem 0;
    ">
        <div style="
            font-family: 'Geist', sans-serif;
            color: #555;
            max-width: 800px;
            margin: 0;
        ">
            <p style="font-size: 1.1rem; line-height: 1.6; margin: 0; text-align: left;">
                Forget Y-Combinator, forget about co-founders, and forget about years-long product discovery.<br><br>
                Launchpad is your ultimate business ideation platform, combining AI-driven insights with practical strategies to turn your ideas into sustainable, revenue-generating ventures.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)

######################################################################################
# Feature Cards
######################################################################################

# Define features
features = [
    {"title": "Ideation", "icon": "💡", "description": "AI-powered whiteboard"},
    {"title": "Idea Journal", "icon": "📓", "description": "AI-powered whiteboard"},
    {"title": "Financial Projections", "icon": "💰", "description": "Back-of-the-napkin financial projections"},
    {"title": "Benchmarks", "icon": "🎯", "description": "Compare your idea to the competition"},
    {"title": "Pitch Deck", "icon": "📊", "description": "Your idea on a few slides"},
    {"title": "User Research", "icon": "💭", "description": "AI-simulated feedback from your first users"},
    {"title": "Feedback", "icon": "🛠️", "description": "Proceed or pivot"}
]

# Create rows of 3 cards each
for i in range(0, len(features), 3):
    cols = st.columns(3)
    for j, col in enumerate(cols):
        if i + j < len(features):
            feature = features[i + j]
            with col:
                st.markdown(f"""
                <div class="feature-card" style="height: 130px;">
                    <div style="font-family: 'Funnel Display', sans-serif; font-weight: bold; font-size: 1.2em;">
                        {feature["title"]}<span style="float: right;">{feature["icon"]}</span>
                    </div>
                    <div class="feature-description">{feature["description"]}</div>
                </div>
                """, unsafe_allow_html=True)
