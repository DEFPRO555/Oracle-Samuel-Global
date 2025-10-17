# Display Oracle Samuel Dashboard Images
import streamlit as st
from PIL import Image

def show_dashboard_images():
    """Display the Oracle Samuel dashboard mockup images"""
    
    st.markdown("""
        <div style="text-align: center; margin: 2rem 0;">
            <h2 style="font-family: 'Playfair Display', serif; font-size: 2.5rem; color: #F3E5AB; margin-bottom: 2rem;">
                Oracle Samuel Dashboard Preview
            </h2>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 20px; border: 2px solid #D4AF37; margin-bottom: 1rem;">
                <h3 style="color: #F3E5AB; text-align: center; margin-bottom: 1rem;">📊 Real Estate Dashboard</h3>
                <p style="color: rgba(255,255,255,0.8); text-align: center; font-size: 0.9rem;">Interactive charts, market trends, and property analytics</p>
            </div>
        """, unsafe_allow_html=True)
        # Add your first dashboard image here
        # st.image("assets/oracle_dashboard_1.jpg", use_column_width=True)
    
    with col2:
        st.markdown("""
            <div style="background: rgba(255, 255, 255, 0.05); padding: 1.5rem; border-radius: 20px; border: 2px solid #D4AF37; margin-bottom: 1rem;">
                <h3 style="color: #F3E5AB; text-align: center; margin-bottom: 1rem;">📈 Data Analysis</h3>
                <p style="color: rgba(255,255,255,0.8); text-align: center; font-size: 0.9rem;">Advanced predictive modeling and AI insights</p>
            </div>
        """, unsafe_allow_html=True)
        # Add your second dashboard image here
        # st.image("assets/oracle_dashboard_2.jpg", use_column_width=True)

