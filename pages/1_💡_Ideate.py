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
                key="idea_description"
            )
            
            additional_instructions = st.text_area(
                "Additional Instructions", 
                placeholder="Focus on people aged 25-35, Focus on domestic manufacturing, etc.",
                height=100,
                key="additional_instructions"
            )
            
            # Configuration options section
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

                option2 = st.slider(
                    label="Select a value:",
                    min_value=0.0,
                    max_value=2.0,
                    value=1.0,
                    step=0.2,
                    key="set2"
                )

                st.markdown("<div style='display: flex; justify-content: space-between;'><span style='font-size:0.8em; font-style:italic'>Realistic</span><span style='font-size:0.8em; font-style:italic'>Unhinged</span></div>",
                            unsafe_allow_html=True)
                st.write("")

            with st.expander("Additional Files"):
                uploaded_file = st.file_uploader("Choose a file", key="file_upload1")
                if uploaded_file is not None:
                    bytes_data = uploaded_file.getvalue()
                    st.write(bytes_data)
            
            submit_button = st.form_submit_button("Save Idea Details", use_container_width=True, type="primary")
            
            if submit_button:
                st.success("Idea details saved!")



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
    # Get idea description from session state
    idea_desc = st.session_state.get("new_idea_description", "")
    
    # Initialize Ollama model
    llm = Ollama(model="tinyllama")
    
    # Create prompt for idea generation
    prompt = f"""Generate creative startup ideas based on this description: {idea_desc}
    Format the response as a numbered list with brief descriptions.
    Focus on innovative and practical solutions."""
    
    # Get response from model
    response = llm(prompt)
    
    # Stream the response word by word
    for word in response.split():
        yield word + " "
        time.sleep(0.02)

if st.button("Generate Launchpad AI Response", icon="💭", type="primary", use_container_width=True):
   st.write_stream(stream_data)

########################################################
# create AI model interface
########################################################

# Create a prompt template for ideation
ideation_template = PromptTemplate(
    input_variables=["idea_context", "user_input"],
    template="""You are a helpful AI assistant for startup ideation and brainstorming.
    Current project context: {idea_context}
    
    User question: {user_input}
    
    Please provide creative and constructive feedback while considering:
    1. Market potential
    2. Technical feasibility
    3. Innovation aspects
    4. Potential challenges
    
    Response:"""
)

# Update the response generator to include max_tokens
def response_generator(prompt):
    llm = Ollama(model="tinyllama")
    # Get the current idea context
    idea_context = st.session_state.get("selected_idea", "New startup idea")
    
    # Format the prompt using the template
    formatted_prompt = ideation_template.format(
        idea_context=idea_context,
        user_input=prompt
    )
    
    response = llm(formatted_prompt)
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
            response = st.write_stream(response_generator(prompt))
        st.session_state.messages.append({"role": "assistant", "content": response})

# Add button to move to monetize tab
if st.button("Continue to Monetize →", type="secondary", use_container_width=True):
    st.switch_page("pages/2_💰_Monetize.py")

# button to clear session and restart
if st.button("Start Over", icon="🗑️", type="tertiary", use_container_width=True):
    st.rerun()

######################################################################################
# AI Chat Interface
######################################################################################

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

def generate_initial_analysis():
    llm = Ollama(model="tinyllama")
    prompt = f"""
    Project Idea: {st.session_state.idea_description}
    Additional Context: {st.session_state.additional_instructions}
    Response Type: {st.session_state.response_type}
    Creativity Level: {st.session_state.creativity_level}
    
    Please analyze this startup idea and provide:
    1. Market potential
    2. Technical feasibility
    3. Innovation aspects
    4. Potential challenges
    5. Next steps
    
    Response:
    """
    
    return llm(prompt)

# Generate Launchpad AI Response button
if st.button("Generate Launchpad AI Response", icon="💭", type="primary", use_container_width=True, key="generate_analysis"):
    if st.session_state.idea_description:
        with st.status("Generating analysis..."):
            initial_response = generate_initial_analysis()
            # Add the initial analysis to chat history
            st.session_state.messages.append({"role": "assistant", "content": initial_response})
    else:
        st.warning("Please describe your idea first!")

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input for follow-up questions
if prompt := st.chat_input("Ask a follow-up question about your idea", key="chat_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        llm = Ollama(model="tinyllama")
        response = llm(f"""
        Previous context: {st.session_state.idea_description}
        Chat history: {str(st.session_state.messages)}
        
        User question: {prompt}
        
        Please provide a helpful response considering the previous context and chat history.
        """)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# Clear chat button
if st.button("Clear Chat", type="secondary", key="clear_chat"):
    st.session_state.messages = []
    st.rerun()

