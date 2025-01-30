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
# Welcome Content
######################################################################################

st.markdown("""
    <div style="font-family: 'Geist', sans-serif;">
    
    **Forget Y-Combinator, forget about co-founders, and forget about years-long discovery.**
    
    **Launchpad is your ultimate business ideation platform, combining AI-driven insights with practical strategies  
    to turn your ideas into sustainable, revenue-generating ventures.**
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="font-family: 'Funnel Display', sans-serif;font-weight: bold;font-size: 24px;margin-bottom: 20px;">
        Launchpad AI Features 👇 
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
                <div class="metric-card" style="height: 130px;">
                    <div style="font-family: 'Funnel Display', sans-serif; font-weight: bold; font-size: 1.2em;">
                        {feature["title"]}<span style="float: right;">{feature["icon"]}</span>
                    </div>
                    <div class="metric-delta">{feature["description"]}</div>
                </div>
                """, unsafe_allow_html=True)





