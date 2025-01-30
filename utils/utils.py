import streamlit as st
from pathlib import Path

def load_css():
    """Load CSS from the style.css file in the root directory"""
    # Get the root project directory (two levels up from this file)
    root_dir = Path(__file__).parent.parent
    css_file = root_dir / "style.css"
    
    with open(css_file) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)