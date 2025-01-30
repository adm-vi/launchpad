import random

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils.page_config import init_page, setup_page_content
from utils.utils import load_css

# Must be called first
init_page('benchmark')

# Then setup the rest of the page
setup_page_content('benchmark')



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

# Get selected idea from sidebar
selected_idea = st.session_state.selected_idea

# Generate sample data based on selected idea
if selected_idea == "AI for dogs":
    competitors = ["PawAI", "BarkTech", "DoggyData", selected_idea]
    target_market = "B2C"
    revenue_model = "Subscription"
elif selected_idea == "startups for toddlers":
    competitors = ["KidVenture", "TinyStartups", "ToddlerTech", selected_idea]
    target_market = "B2B2C" 
    revenue_model = "Freemium"
else:
    competitors = ["Competitor A", "Competitor B", "Competitor C", "New Idea"]
    target_market = "TBD"
    revenue_model = "TBD"

# Create sample competitor data
matrix_data = {
    "Company": competitors,
    "Target Market": [random.choice(["B2B", "B2C", "B2B2C"]) for _ in range(3)] + [target_market],
    "Revenue Model": [random.choice(["Subscription", "One-time", "Freemium"]) for _ in range(3)] + [revenue_model],
    "Average Pricing ($)": [random.randint(20, 200) for _ in range(3)] + [50],
    "Total Customers": [random.randint(1000, 10000) for _ in range(3)] + [2500],
    "CAC ($)": [random.randint(50, 200) for _ in range(3)] + [100],
    "CLV ($)": [random.randint(300, 1000) for _ in range(3)] + [500],
    "Churn Rate (%)": [round(random.uniform(2, 15), 1) for _ in range(3)] + [5.0],
    "Growth Rate (%)": [round(random.uniform(5, 30), 1) for _ in range(3)] + [15.0]
}

df = pd.DataFrame(matrix_data)

######################################################################################
# Competitive Analysis Matrix
######################################################################################
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Competitive Analysis Matrix",
    "Unit Economics Comparison", 
    "TAM Analysis",
    "Growth vs Churn",
    "Market Position",
    "Perceptual Map"
])

with tab1:
    st.dataframe(df, use_container_width=True)

with tab2:
    with st.container():
        fig = make_subplots(rows=1, cols=2, subplot_titles=('CAC vs CLV', 'CLV/CAC Ratio'))
        
        # CAC vs CLV Bar Chart
        fig.add_trace(
            go.Bar(name='CAC', x=competitors, y=df['CAC ($)']),
            row=1, col=1
        )
        fig.add_trace(
            go.Bar(name='CLV', x=competitors, y=df['CLV ($)']),
            row=1, col=1
        )
        
        # CLV/CAC Ratio
        clv_cac_ratio = df['CLV ($)'] / df['CAC ($)']
        fig.add_trace(
            go.Bar(x=competitors, y=clv_cac_ratio, name='CLV/CAC Ratio'),
            row=1, col=2
        )
        
        fig.update_layout(height=400, showlegend=True)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    with st.container():
        # Sample TAM breakdown data
        market_segments = {
            'Enterprise': random.randint(2000, 4000),
            'Mid-Market': random.randint(1000, 2000), 
            'SMB': random.randint(500, 1000),
            'Consumer': random.randint(200, 500)
        }
        
        # Calculate total TAM
        total_tam = sum(market_segments.values())
        
        # Create modern treemap visualization
        fig4 = go.Figure(go.Treemap(
            labels=list(market_segments.keys()),
            parents=[''] * len(market_segments),
            values=list(market_segments.values()),
            textinfo='label+value',
            texttemplate='%{label}<br>$%{value}M',
            hovertemplate='Segment: %{label}<br>TAM: $%{value}M<extra></extra>',
            marker=dict(
                colors=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
                line=dict(width=2, color='white')
            )
        ))
        
        fig4.update_layout(
            title={
                'text': 'Total Addressable Market Breakdown',
                'y': 0.95,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top',
                'font': dict(size=24)
            },
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
        )
        
        st.plotly_chart(fig4, use_container_width=True)

        # Display modern metrics cards
        st.markdown("""
            <style>
            .metric-card {
                background-color: #f8f9fa;
                border-radius: 10px;
                padding: 20px;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .metric-value {
                font-size: 24px;
                font-weight: bold;
                color: #1f77b4;
            }
            .metric-label {
                font-size: 14px;
                color: #666;
                margin-top: 5px;
            }
            </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">${total_tam:,.0f}M</div>
                    <div class="metric-label">Total Addressable Market</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col2:
            largest_segment = max(market_segments.items(), key=lambda x: x[1])
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{largest_segment[0]}</div>
                    <div class="metric-label">Largest Market Segment</div>
                </div>
            """, unsafe_allow_html=True)
            
        with col3:
            avg_segment = total_tam / len(market_segments)
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">${avg_segment:,.0f}M</div>
                    <div class="metric-label">Average Segment Size</div>
                </div>
            """, unsafe_allow_html=True)

with tab4:
    with st.container():
        fig2 = px.scatter(df, x='Growth Rate (%)', y='Churn Rate (%)', 
                         size='CLV ($)', color='Company',
                         title='Growth vs Churn (bubble size represents CLV)')
        st.plotly_chart(fig2, use_container_width=True)

with tab5:
    with st.container():
        # Calculate market position scores (simplified)
        df['Market Score'] = (df['Growth Rate (%)'] * 0.4 + 
                             df['CLV ($)'] / df['CAC ($)'] * 0.4 - 
                             df['Churn Rate (%)'] * 0.2)
        
        fig3 = px.bar(df, x='Company', y='Market Score',
                      title='Overall Market Position Score',
                      color='Company')
        st.plotly_chart(fig3, use_container_width=True)

with tab6:
    with st.container():
        # Create figure with secondary y-axis
        fig = go.Figure()
        
        # Add scatter points for each competitor
        fig.add_trace(go.Scatter(
            x=df['Average Pricing ($)'],
            y=df['Growth Rate (%)'],
            mode='markers',
            marker=dict(
                size=30,
                color=['#6B5B95', '#FF6B6B', '#4ECDC4', '#45B7D1'],
                line=dict(width=1, color='#333333')
            ),
            text=df['Company'],
            hovertemplate="<b>%{text}</b><br>" +
                         "Price: $%{x}<br>" +
                         "Growth: %{y}%<br>" +
                         "<extra></extra>"
        ))
        
        # Calculate the middle points for axes
        x_middle = (df['Average Pricing ($)'].max() + df['Average Pricing ($)'].min()) / 2
        y_middle = (df['Growth Rate (%)'].max() + df['Growth Rate (%)'].min()) / 2
        
        # Update layout for quadrant style with centered axes
        fig.update_layout(
            title="Market Position Analysis",
            xaxis=dict(
                title="Innovative Value",
                showgrid=False,
                zeroline=False,
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True,
                range=[
                    df['Average Pricing ($)'].min() - (df['Average Pricing ($)'].max() - df['Average Pricing ($)'].min()) * 0.2,
                    df['Average Pricing ($)'].max() + (df['Average Pricing ($)'].max() - df['Average Pricing ($)'].min()) * 0.2
                ]
            ),
            yaxis=dict(
                title="Sustainable Growth",
                showgrid=False,
                zeroline=False,
                showline=True,
                linewidth=2,
                linecolor='black',
                mirror=True,
                range=[
                    df['Growth Rate (%)'].min() - (df['Growth Rate (%)'].max() - df['Growth Rate (%)'].min()) * 0.2,
                    df['Growth Rate (%)'].max() + (df['Growth Rate (%)'].max() - df['Growth Rate (%)'].min()) * 0.2
                ]
            ),
            showlegend=False,
            plot_bgcolor='white',
            height=600,
            width=800,
            shapes=[
                # Vertical line (x-axis)
                dict(
                    type='line',
                    x0=x_middle,
                    y0=df['Growth Rate (%)'].min() - (df['Growth Rate (%)'].max() - df['Growth Rate (%)'].min()) * 0.2,
                    x1=x_middle,
                    y1=df['Growth Rate (%)'].max() + (df['Growth Rate (%)'].max() - df['Growth Rate (%)'].min()) * 0.2,
                    line=dict(color='black', width=2)
                ),
                # Horizontal line (y-axis)
                dict(
                    type='line',
                    x0=df['Average Pricing ($)'].min() - (df['Average Pricing ($)'].max() - df['Average Pricing ($)'].min()) * 0.2,
                    y0=y_middle,
                    x1=df['Average Pricing ($)'].max() + (df['Average Pricing ($)'].max() - df['Average Pricing ($)'].min()) * 0.2,
                    y1=y_middle,
                    line=dict(color='black', width=2)
                )
            ],
            annotations=[
                # Quadrant labels
                dict(x=0.95, y=0.95, xref="paper", yref="paper",
                     text="High Value, High Growth", showarrow=False),
                dict(x=0.95, y=0.05, xref="paper", yref="paper",
                     text="High Value, Low Growth", showarrow=False),
                dict(x=0.05, y=0.95, xref="paper", yref="paper",
                     text="Low Value, High Growth", showarrow=False),
                dict(x=0.05, y=0.05, xref="paper", yref="paper",
                     text="Low Value, Low Growth", showarrow=False),
                # Axis labels
                dict(x=0, y=1.05, xref="paper", yref="paper",
                     text="High", showarrow=False),
                dict(x=0, y=-0.05, xref="paper", yref="paper",
                     text="Low", showarrow=False),
                dict(x=-0.05, y=0.5, xref="paper", yref="paper",
                     text="Least", showarrow=False, textangle=-90),
                dict(x=1.05, y=0.5, xref="paper", yref="paper",
                     text="Most", showarrow=False, textangle=-90)
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("""
            #### Positioning Map Insights
            - **Top Right**: Premium market leaders with high growth
            - **Top Left**: Emerging players with strong growth potential
            - **Bottom Right**: Established players with slower growth
            - **Bottom Left**: Market challengers and new entrants
            
            The size of each circle represents market presence. Hover over points to see detailed metrics.
        """)


######################################################################################


# compare the idea, the biz plan and the pricing to other existing businesses
# create a dataframe comparing on the following key criteria/metrics:
# - idea
# - biz plan
# - pricing
# - competition
# - target audience
# - marketing strategy
# - revenue model
# - customer acquisition cost
# - customer retention rate
# - customer lifetime value
# - customer churn rate
# - customer acquisition cost
# - customer retention rate
# - customer lifetime value
# - customer churn rate