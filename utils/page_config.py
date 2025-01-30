import streamlit as st
from .config import PAGES, DEFAULT_LAYOUT, LOGO_PATH, LOGO_LINK, SIDEBAR_IMAGE_PATH
from .utils import load_css

def init_page(page_name: str):
    """Initialize page config (must be called first)"""
    page_config = PAGES[page_name]
    
    st.set_page_config(
        page_title=page_config['title'],
        page_icon=page_config['icon'],
        layout=DEFAULT_LAYOUT,
    )

def setup_page_content(page_name: str):
    """Setup the rest of the page content"""
    page_config = PAGES[page_name]
    
    load_css()
    
    st.logo(
        LOGO_PATH,
        size="large",
        link=LOGO_LINK,
    )
    
    st.sidebar.image(
        SIDEBAR_IMAGE_PATH, 
        width=None,
        use_container_width=True
    )
    
    st.markdown(f"""
        <div class="header-container">
            <h1 class="header-title">{page_config['title']}</h1>
            <p class="header-subtitle">{page_config['subtitle']}</p>
            <hr class="header-divider">
        </div>
    """, unsafe_allow_html=True)