import streamlit as st
from utils import load_css


######################################################################################
# page configurations
######################################################################################

st.set_page_config(
    page_title="The Pitch",
    page_icon="📊",
    layout="wide",
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
        <h1 class="header-title">Pitch Deck</h1>
        <p class="header-subtitle">How to socialize your idea</p>
        <hr class="header-divider">
    </div>
""", unsafe_allow_html=True
)

# Initialize selected_idea as None if not exists
if 'selected_idea' not in st.session_state:
    st.session_state.selected_idea = None

# Add selectbox with None as initial state
add_selectbox = st.selectbox(
   "Which idea are you working on?",     
   options=["AI for dogs", "startups for toddlers"],
   index=None,
   placeholder="Select an idea",
   key="selected_idea"
)

# Stop rendering if no idea selected
if st.session_state.selected_idea is None:
    st.stop()

######################################################################################

def create_slide(title, slide_number, content_fn):
    slide_html_start = f"""
        <div class="slide">
            <div class="slide-number">SLIDE {slide_number}</div>
            <div class="slide-title">{title}</div>
            <div class="slide-content">
    """
    slide_html_end = """
            </div>
        </div>
    """
    
    with st.container():
        st.markdown(slide_html_start, unsafe_allow_html=True)
        content_fn()  # Execute the content function inside the container
        st.markdown(slide_html_end, unsafe_allow_html=True)

# Slide 1: Problem & Solution
def slide1_content():
    cols = st.columns(2)
    with cols[0]:
        st.markdown('<h3 style="font-family: Geist; margin-bottom: 0.5rem;">The Problem</h3>', unsafe_allow_html=True)
        st.text_area("Problem Description", key="problem", height=150, label_visibility="collapsed")
    with cols[1]:
        st.markdown('<h3 style="font-family: Geist; margin-bottom: 0.5rem;">Our Solution</h3>', unsafe_allow_html=True)
        st.text_area("Solution Description", key="solution", height=150, label_visibility="collapsed")

create_slide("Problem & Solution", 1, slide1_content)

# Slide 2: Market Opportunity
def slide2_content():
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Addressable Market (TAM)", "$XXB")
        st.metric("Serviceable Addressable Market (SAM)", "$XXB")
    with col2:
        st.metric("Serviceable Obtainable Market (SOM)", "$XXB")
        st.text_area("Describe market growth and trends", height=100)
create_slide("Market Opportunity", 2, slide2_content)

# Slide 3: Product & Technology
def slide3_content():
    st.image("https://via.placeholder.com/600x300", caption="Product Screenshot")
    st.text_area("What makes your technology unique?", height=100)
    st.text_area("Future product roadmap", height=100)
create_slide("Product & Technology", 3, slide3_content)

# Slide 4: Business Model & Traction
def slide4_content():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current MRR", "$XXk")
        st.metric("YoY Growth", "XX%")
    with col2:
        st.metric("CAC", "$XXX")
        st.metric("LTV", "$XXXX")
    with col3:
        st.metric("Gross Margin", "XX%")
        st.metric("Burn Rate", "$XXk/month")
create_slide("Business Model & Traction", 4, slide4_content)

# Slide 5: Go-to-Market Strategy
def slide5_content():
    st.text_area("Distribution Strategy", height=100)
    col1, col2 = st.columns(2)
    with col1:
        st.text_area("Marketing Channels", height=100)
    with col2:
        st.text_area("Sales Strategy", height=100)
create_slide("Go-to-Market Strategy", 5, slide5_content)

# Slide 6: Competitive Analysis
def slide6_content():
    competition_data = {
        'Feature': ['Feature 1', 'Feature 2', 'Feature 3', 'Feature 4'],
        'Our Solution': ['✅', '✅', '✅', '✅'],
        'Competitor A': ['✅', '❌', '✅', '❌'],
        'Competitor B': ['❌', '✅', '❌', '✅']
    }
    st.dataframe(competition_data, use_container_width=True)
    st.text_area("Key Competitive Advantages", height=100)
create_slide("Competitive Landscape", 6, slide6_content)

# Slide 7: Team
def slide7_content():
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image("https://via.placeholder.com/150", caption="CEO")
        st.text_area("CEO Background", height=100)
    with col2:
        st.image("https://via.placeholder.com/150", caption="CTO")
        st.text_area("CTO Background", height=100)
    with col3:
        st.image("https://via.placeholder.com/150", caption="COO")
        st.text_area("COO Background", height=100)
create_slide("World-Class Team", 7, slide7_content)

# Slide 8: Financials & Ask
def slide8_content():
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Raising", "$XXM")
        st.metric("Pre-money Valuation", "$XXM")
        st.metric("Runway Extension", "XX months")
    with col2:
        st.text_area("Use of Funds", height=150)
        st.text_area("Key Milestones", height=150)
create_slide("The Ask", 8, slide8_content)

# Export options
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.download_button(
        label="Download as PDF",
        data="Pitch deck data...",
        file_name="pitch_deck.pdf",
        mime="application/pdf"
    )
with col2:
    st.download_button(
        label="Download as PPT",
        data="Pitch deck data...",
        file_name="pitch_deck.pptx",
        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
    )



