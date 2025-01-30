import streamlit as st
from pathlib import Path

def load_css():
    current_dir = Path(__file__).parent
    css_path = current_dir / 'style.css'
    with open(css_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)