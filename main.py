import streamlit as st
from utils import load_css

######################################################################################
# page configurations
######################################################################################

st.set_page_config(
    page_title="hello",
    page_icon="👋",
    layout="wide",
    # menu_items={
    #     'Get Help': 'https://www.extremelycoolapp.com/help',
    #     'Report a bug': "https://www.extremelycoolapp.com/bug",
    #     'About': "# This is a header. This is an *extremely* cool app!"
    # }
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

######################################################################################
# Header and Branding
######################################################################################

st.markdown("""
    <div class="header-container">
        <h1 class="header-title">Welcome to Launchpad</h1>
        <p class="header-subtitle">AI-Powered Product Acceleration</p>
        <hr class="header-divider">
    </div>
""", unsafe_allow_html=True
)
######################################################################################

st.markdown("""
    <div style="font-family: 'Geist', sans-serif;">
    
    **Forget Y-Combinator—Launchpad is your ultimate business ideation platform,
    combining AI-driven insights with practical strategies to turn your ideas into
    sustainable, revenue-generating ventures.**
    
    **Launchpad's AI can help you:**
            
    - **Ideas** - Your ideas are safe here.
    - **Ideate** - Need help refining your idea? Looking for new inspiration? We've got you covered.
    - **Monetize** - Let our AI analyze various pricing strategies and select the best one for your idea
    - **Benchmark** - Compare your idea to potential competition
    - **Pitch** - Ideas on a page.
    - **Feedback** - Proceed or pivot.
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="header-container">
        <div style="display: flex; align-items: center; gap: 1rem;">
            <span style="font-size: 32px;">👈</span>
            <p class="header-subtitle">Select an option from the sidebar to get started</p>
        </div>
    </div>
""", unsafe_allow_html=True)





