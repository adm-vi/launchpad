import streamlit as st
import time
import random
import pandas as pd
import numpy as np
from utils import load_css

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

# Add selectbox here
add_selectbox = st.selectbox(
   "Which idea are you working on?",   
   options=["new idea", "AI for dogs", "startups for toddlers"],
   key="selected_idea"
)

######################################################################################

# Check if there's a selected idea and it's not empty
if "selected_idea" in st.session_state and st.session_state.selected_idea != "new idea":
    selected_idea = st.session_state.selected_idea
    st.success(f"📝 Currently working on: **{selected_idea}**")
    
    # Here we would load any saved data for the existing project
    # For now just showing placeholder text
    st.markdown("""
    ##### Project Details
    Your previously entered information for this project has been loaded.
    You can continue working on this idea or select another project from the sidebar.
    """)
    
    # Add a divider between existing project and new project form
    st.markdown("---")
else:
    # Show prominent call-to-action for new project
    st.info("👇 Get started by creating a new project below!")
    
    # Project name input form
    with st.container():
        st.markdown("### Create New Project")
        with st.form("new_project_form"):
            project_name = st.text_input(
                "Project Name",
                placeholder="AI for dogs", 
                key="new_project_name"
            )
            
            idea_description = st.text_area(
                "Describe your idea",
                placeholder="What are we building?",
                height=150,
                key="new_idea_description"
            )
            
            additional_instructions = st.text_area(
                "Additional Instructions", 
                placeholder="Focus on people aged 25-35, Focus on domestic manufacturing, etc.",
                height=100,
                key="new_additional_instructions"
            )
            
            submit_button = st.form_submit_button("Create New Project", use_container_width=True, type="primary")
            
            if submit_button and project_name:
                # Add new project name to selectbox options
                if project_name not in add_selectbox.options:
                    st.session_state.selected_idea = project_name
                    st.experimental_rerun()
                else:
                    st.error("A project with this name already exists")

########################################################
# Create two columns for configuration options
########################################################

with st.form("ideation_config_form"):
    st.write("##### Configure Your Ideation Session")
    st.markdown("Set your preferences for how you'd like the AI to approach your ideation process.")

    col1, space, col2 = st.columns([1, 0.1, 1])

    with col1:
        st.markdown("##### Response Type")
        st.caption(
            """**Choose how detailed you want the AI's responses to be:**  
            - **Concise**: Quick, focused ideas for early brainstorming  
            - **Detailed**: In-depth analysis for developed concepts"""
        )
        option1 = st.radio(
            label="**Select a response type:**",
            options=["Concise", "Detailed"],
            key="set1",
            horizontal=True
        )

    with col2:
        st.markdown("##### Ideation Style") 
        st.caption(
            """**Use the slider to adjust how conventional you want the ideas to be:**  
            - **Realistic**: Practical, market-ready concepts  
            - **Unhinged**: Creative, out-of-the-box thinking"""
        )

        # Create a slider from 0 to 1 with 0.2 increments
        option2 = st.slider(
            label="Select a value:",  # Simple text label
            min_value=0.0,
            max_value=2.0,
            value=1.0,  # Default value
            step=0.2,
            key="set2"
        )

        # Add the styled text separately
        st.markdown("<div style='display: flex; justify-content: space-between;'><span style='font-size:0.8em; font-style:italic'>Realistic</span><span style='font-size:0.8em; font-style:italic'>Unhinged</span></div>",
                    unsafe_allow_html=True)
        st.write("")

    with st.expander("Additional Files"):
        uploaded_file = st.file_uploader("Choose a file", key="file_upload1")
        if uploaded_file is not None:
            # To read file as bytes:
            bytes_data = uploaded_file.getvalue()
            st.write(bytes_data)
            
    submit_config = st.form_submit_button("Apply Configuration", use_container_width=True, type="primary")

########################################################

_LOREM_IPSUM_A = """
# AI Dog Innovations

1. "Doggie GPT"
  AI bark translator in Shakespearean English
  "To pee, or not to pee, that is the question."

2. "Tail-Wag Trainer 3000"
  Analytics for optimizing tail-wagging cuteness

3. "FetchGPT"
  Predictive ball landing algorithm

4. "PawPal Virtual Therapist"
  AI therapy for vacuum cleaner phobias
"""

_LOREM_IPSUM_B = """
5. "KibbleTunes"
  Breed-specific Spotify playlists
  Example: Lofi Beats to Bark To

6. "SquirrelSense"
  Bluetooth collar alerts for nearby squirrels

7. "Dogfluence AI"
  Instagram automation for canine influencers
  Features: captions, hashtags, AI outfit photos
"""

def stream_data():
    for word in _LOREM_IPSUM_A.split(" "):
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM_B.split(" "):
        yield word + " "
        time.sleep(0.02)

if st.button("Generate Launchpad AI Response", icon="💭", type="primary", use_container_width=True):
   st.write_stream(stream_data)

# if st.button("Discuss Further", icon="🤔", type="secondary", use_container_width=True):
#     st.rerun()

########################################################
# create AI model interface
########################################################

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)

with st.expander("Discuss with Launchpad"):
    # Add clear chat button
    if st.button("clear chat"):
        st.session_state.messages = []
        st.rerun()

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What do you think about this idea?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            response = st.write_stream(response_generator())
        st.session_state.messages.append({"role": "assistant", "content": response})

# button to clear session and restart
if st.button("Start Over", icon="🗑️", type="secondary", use_container_width=True):
    st.rerun()

