import streamlit as st
import time
import random
import pandas as pd
import numpy as np
from utils import load_css
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

######################################################################################
# page configurations
######################################################################################

st.set_page_config(
    page_title="ideate",
    page_icon="💡",
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
        <h1 class="header-title">Ideate</h1>
        <p class="header-subtitle">Your AI-Powered Whiteboard</p>
        <hr class="header-divider">
    </div>
""", unsafe_allow_html=True
)

# Add selectbox with None as initial state
add_selectbox = st.selectbox(
   "Which idea are you working on?",     
   options=["AI for dogs", "startups for toddlers"],
   index=None,
   placeholder="Select an idea",
   key="selected_idea"
)

######################################################################################

# Check if there's a selected idea
if "selected_idea" in st.session_state and st.session_state.selected_idea:
    selected_idea = st.session_state.selected_idea
    st.success(f"📝 Currently working on: **{selected_idea}**")
    
    # Here we would load any saved data for the existing project
    st.markdown("""
    ##### Project Details
    Your previously entered information for this project has been loaded.
    You can continue working on this idea or select another project from the sidebar.
    """)
    
    # Add a divider between existing project and new project form
    st.markdown("---")

# Load project details based on selection
if st.session_state.selected_idea:
    # Here we would load the project details from a database/storage
    # For now using dummy data
    project_details = {
        "AI for dogs": "An AI-powered platform that helps understand dog behaviors and needs, providing personalized training and care recommendations.",
        "startups for toddlers": "Educational program teaching entrepreneurship basics to toddlers through interactive play and simple business concepts."
    }
    
    # Store the idea description for use in prompts
    st.session_state['idea_description'] = project_details[st.session_state.selected_idea]
    st.session_state['combined_text'] = project_details[st.session_state.selected_idea]
    
    # Display the loaded description
    st.info("📝 Project Description: " + project_details[st.session_state.selected_idea])


# Model settings section
st.write("##### Model Settings")
st.markdown("Fine-tune how the AI generates responses by adjusting these technical parameters.")

col1, space, col2 = st.columns([1, 0.1, 1])

with col1:
    st.markdown("##### Temperature")
    st.caption(
        """**Control the creativity level of the AI:**  
        - **Focused**: More deterministic and consistent  
        - **Creative**: More varied and unexpected"""
    )
    temperature = st.slider(
        label="Select a value:",
        min_value=0.0,
        max_value=2.0,
        value=0.7,
        step=0.1,
        key="temperature"
    )
    st.markdown("<div style='display: flex; justify-content: space-between;'><span style='font-size:0.8em; font-style:italic'>Focused</span><span style='font-size:0.8em; font-style:italic'>Creative</span></div>",
                unsafe_allow_html=True)
    st.write("")

with col2:
    st.markdown("##### Response Length")
    st.caption(
        """**Set how detailed you want the response to be:**  
        - **Shorter**: Quick, concise responses  
        - **Longer**: More comprehensive outputs"""
    )
    max_tokens = st.slider(
        label="Select a value:",
        min_value=100,
        max_value=2000,
        value=750,
        step=50,
        key="max_tokens"
    )
    st.markdown("<div style='display: flex; justify-content: space-between;'><span style='font-size:0.8em; font-style:italic'>Shorter</span><span style='font-size:0.8em; font-style:italic'>Longer</span></div>",
                unsafe_allow_html=True)
    st.write("")

# Chat interface
def generate_response(prompt, is_initial=False):
    llm = Ollama(
        model="tinyllama",
        temperature=temperature,
        num_predict=max_tokens
    )
    
    if is_initial:
        # Initial ideation prompt
        system_prompt = f"""
        You are a creative ideation partner helping expand on the following idea:
        {st.session_state.get('combined_text', '')}

        Please provide creative suggestions and ideas in the following format:

        CORE CONCEPT EXPANSION:
        • [List 3-4 creative ways to expand the core concept]

        UNIQUE FEATURES:
        • [List 4-5 innovative features that would make this product/service stand out]

        CREATIVE USE CASES:
        • [List 3-4 interesting ways this could be used]

        POTENTIAL TWISTS:
        • [List 3-4 unexpected directions or pivots worth considering]

        Be imaginative and think outside the box while keeping suggestions practical enough to implement.
        """
    else:
        # Follow-up ideation prompt
        system_prompt = f"""
        You are a creative ideation partner. We're brainstorming about this idea:
        {st.session_state.get('idea_description', '')}
        
        Their question is: {prompt}

        Please provide an imaginative response with:
        • 3-4 creative suggestions directly related to their question
        • 2-3 unexpected angles they may not have considered
        • 2-3 specific examples or use cases to illustrate your ideas
        
        Format everything as bullet points and keep the tone encouraging and exploratory.
        """
    
    response = llm(system_prompt)
    for word in response.split():
        yield word + " "

with st.expander("💭 Launchpad AI Analysis", expanded=True):
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Add buttons in columns
    col1, col2 = st.columns([4, 1])
    with col1:
        if st.button("Launchpad Launch", type="primary", key="initial_analysis"):
            combined_text = f"""
            IDEA DESCRIPTION:
            {st.session_state.get('idea_description', '')}

            ADDITIONAL CONTEXT:
            {st.session_state.get('additional_context', '')}
            """
            response = "".join(generate_response(combined_text, is_initial=True))
            st.session_state.messages.append({"role": "assistant", "content": response})
    with col2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                # Format user messages with numbered points
                formatted_text = message["content"]
                # Add line breaks before numbered points
                for i in range(1, 10):
                    formatted_text = formatted_text.replace(f"{i}.", f"\n\n{i}.")
                st.markdown(formatted_text)
            else:
                # Format assistant messages with proper spacing
                formatted_response = message["content"]
                
                # Clean up extra whitespace and indentation
                formatted_response = "\n".join(line.strip() for line in formatted_response.split("\n"))
                
                # Add spacing around bullet points
                formatted_response = formatted_response.replace("•", "\n\n• ")
                
                # Format section headers
                sections = ["CORE CONCEPT", "UNIQUE FEATURES", "CREATIVE USE CASES", "POTENTIAL TWISTS", 
                          "MARKET ANALYSIS", "TECHNICAL FEASIBILITY", "INNOVATION ASSESSMENT", "RECOMMENDATIONS"]
                for section in sections:
                    formatted_response = formatted_response.replace(section, f"\n\n### {section}\n")
                
                # Add spacing after periods that end sentences
                formatted_response = formatted_response.replace(". ", ".\n\n")
                
                # Clean up any multiple newlines (more than 2)
                while "\n\n\n" in formatted_response:
                    formatted_response = formatted_response.replace("\n\n\n", "\n\n")
                
                st.markdown(formatted_response)

    # Accept user input
    if prompt := st.chat_input("Ask a follow-up question"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        # Generate and display assistant response
        with st.chat_message("assistant"):
            response = st.write_stream(generate_response(prompt))
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()  # Rerun to properly format the response

# Add button to move to monetize tab
if st.button("Continue to Monetize 💰 →", type="secondary", use_container_width=True):
    st.switch_page("pages/2_💰_Monetize.py")

# button to clear session and restart
if st.button("Start Over", icon="🗑️", type="tertiary", use_container_width=True):
    st.rerun()
