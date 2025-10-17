# © 2025 Dowek Analytics Ltd.
# Oracle Samuel - Premium UI Enhancements Module
# $1,000,000 Website Design Implementation

import streamlit as st
import base64
from pathlib import Path

def load_premium_css():
    """Load premium enhanced CSS styles"""
    with open('assets/premium_enhanced.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def create_hero_section():
    """Create cinematic hero section with animations"""
    st.markdown("""
        <div class="hero-section">
            <div class="hero-background"></div>
            <div class="hero-particles"></div>
            <div class="hero-content reveal-fade-in">
                <h1 class="hero-title">ORACLE SAMUEL</h1>
                <p class="hero-subtitle">The Future of Real Estate Intelligence</p>
                <button class="btn-premium btn-gold">Start Predicting Now</button>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_stats_section():
    """Create animated statistics counters"""
    st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem; padding: 4rem 2rem; background: var(--dark-navy);">
            <div class="glass-card reveal-scale" style="text-align: center;">
                <div class="stats-counter">99.2%</div>
                <div class="stats-label">Accuracy Rate</div>
            </div>
            <div class="glass-card reveal-scale" style="text-align: center; animation-delay: 0.1s;">
                <div class="stats-counter">500K+</div>
                <div class="stats-label">Predictions Made</div>
            </div>
            <div class="glass-card reveal-scale" style="text-align: center; animation-delay: 0.2s;">
                <div class="stats-counter">$2.5B+</div>
                <div class="stats-label">Property Value Analyzed</div>
            </div>
            <div class="glass-card reveal-scale" style="text-align: center; animation-delay: 0.3s;">
                <div class="stats-counter">24/7</div>
                <div class="stats-label">AI Monitoring</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_analytics_showcase():
    """Create financial analytics showcase section with image"""
    st.markdown("""
        <div class="analytics-showcase">
            <div style="max-width: 1200px; margin: 0 auto;">
                <h2 class="reveal-fade-in" style="font-family: var(--font-display); font-size: 3.5rem; color: var(--primary-gold); text-align: center; margin-bottom: 3rem;">
                    Advanced Market Intelligence
                </h2>
                <div class="section-image-overlay reveal-slide-right">
                    <img src="https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=1200" 
                         alt="Financial Analytics Dashboard" 
                         class="analytics-image">
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem; margin-top: 3rem;">
                    <div class="glass-card luxury-hover">
                        <h3 style="color: var(--primary-gold); font-family: var(--font-display); margin-bottom: 1rem;">📊 Real-Time Analytics</h3>
                        <p style="color: rgba(255,255,255,0.8);">Monitor market trends with live data visualization and predictive insights powered by advanced AI algorithms.</p>
                    </div>
                    <div class="glass-card luxury-hover">
                        <h3 style="color: var(--primary-gold); font-family: var(--font-display); margin-bottom: 1rem;">🎯 Precision Forecasting</h3>
                        <p style="color: rgba(255,255,255,0.8);">99.2% accuracy in price predictions using ensemble machine learning models and historical data analysis.</p>
                    </div>
                    <div class="glass-card luxury-hover">
                        <h3 style="color: var(--primary-gold); font-family: var(--font-display); margin-bottom: 1rem;">🔮 Market Intelligence</h3>
                        <p style="color: rgba(255,255,255,0.8);">Comprehensive market insights with geographic heat maps and trend analysis across multiple cities.</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_smart_city_section():
    """Create smart city technology section"""
    st.markdown("""
        <div class="realestate-showcase">
            <div style="max-width: 1200px; margin: 0 auto;">
                <h2 class="reveal-fade-in" style="font-family: var(--font-display); font-size: 3.5rem; color: var(--primary-blue); text-align: center; margin-bottom: 3rem;">
                    Smart City Integration
                </h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center;">
                    <div class="reveal-slide-right">
                        <div class="section-image-overlay">
                            <img src="https://images.unsplash.com/photo-1480714378408-67cf0d13bc1b?w=800" 
                                 alt="Smart City Technology">
                        </div>
                    </div>
                    <div class="reveal-fade-in">
                        <h3 style="font-family: var(--font-display); font-size: 2rem; color: var(--primary-blue); margin-bottom: 1.5rem;">
                            Future-Ready Real Estate Intelligence
                        </h3>
                        <p style="color: #475569; font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
                            Oracle Samuel leverages cutting-edge AI technology to provide unprecedented insights into urban real estate markets. 
                            Our platform analyzes millions of data points to deliver accurate, actionable intelligence for investors, developers, and homeowners.
                        </p>
                        <div class="gradient-border" style="background: white; padding: 2rem; border-radius: 20px;">
                            <ul style="list-style: none; padding: 0;">
                                <li style="margin-bottom: 1rem; color: #0A1931;">✨ AI-Powered Valuation Models</li>
                                <li style="margin-bottom: 1rem; color: #0A1931;">🌍 Geographic Market Analysis</li>
                                <li style="margin-bottom: 1rem; color: #0A1931;">📈 Investment Opportunity Scoring</li>
                                <li style="margin-bottom: 1rem; color: #0A1931;">🔐 Enterprise-Grade Security</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_ai_technology_section():
    """Create AI technology showcase with handshake image"""
    st.markdown("""
        <div class="ai-tech-section">
            <div style="max-width: 1200px; margin: 0 auto;">
                <h2 class="reveal-fade-in" style="font-family: var(--font-display); font-size: 3.5rem; color: var(--primary-gold); text-align: center; margin-bottom: 3rem;">
                    AI-Powered Trust & Innovation
                </h2>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; align-items: center;">
                    <div class="reveal-fade-in">
                        <h3 style="font-family: var(--font-display); font-size: 2rem; color: white; margin-bottom: 1.5rem;">
                            Partnership in Intelligence
                        </h3>
                        <p style="color: rgba(255,255,255,0.8); font-size: 1.1rem; line-height: 1.8; margin-bottom: 2rem;">
                            Oracle Samuel represents the perfect synergy between human expertise and artificial intelligence. 
                            Our advanced algorithms work alongside real estate professionals to deliver unmatched accuracy and insights.
                        </p>
                        <button class="btn-premium btn-glass">Explore Technology</button>
                    </div>
                    <div class="reveal-slide-right">
                        <div class="section-image-overlay card-3d">
                            <img src="https://images.unsplash.com/photo-1556761175-b413da4baf72?w=800" 
                                 alt="AI Partnership">
                        </div>
                    </div>
                </div>
                
                <div class="ai-tech-grid" style="margin-top: 4rem;">
                    <div class="glass-card luxury-hover">
                        <h4 style="color: var(--primary-gold); font-family: var(--font-tech); font-size: 1.5rem; margin-bottom: 1rem;">🤖 Machine Learning</h4>
                        <p style="color: rgba(255,255,255,0.7);">Advanced ensemble models combining XGBoost, LightGBM, and CatBoost for superior prediction accuracy.</p>
                    </div>
                    <div class="glass-card luxury-hover">
                        <h4 style="color: var(--primary-gold); font-family: var(--font-tech); font-size: 1.5rem; margin-bottom: 1rem;">🧠 Deep Learning</h4>
                        <p style="color: rgba(255,255,255,0.7);">Neural networks trained on millions of property transactions for pattern recognition and anomaly detection.</p>
                    </div>
                    <div class="glass-card luxury-hover">
                        <h4 style="color: var(--primary-gold); font-family: var(--font-tech); font-size: 1.5rem; margin-bottom: 1rem;">🔄 Self-Learning</h4>
                        <p style="color: rgba(255,255,255,0.7);">Continuous model improvement through automated retraining and performance monitoring.</p>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_property_showcase():
    """Create luxury property showcase section"""
    st.markdown("""
        <div class="realestate-showcase">
            <div style="max-width: 1200px; margin: 0 auto;">
                <h2 class="reveal-fade-in" style="font-family: var(--font-display); font-size: 3.5rem; color: var(--primary-blue); text-align: center; margin-bottom: 3rem;">
                    Premium Property Intelligence
                </h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2rem;">
                    <div class="property-card reveal-scale">
                        <div class="section-image-overlay">
                            <img src="https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600" 
                                 alt="Luxury Property">
                        </div>
                        <div style="padding: 2rem; background: white;">
                            <h4 style="font-family: var(--font-display); color: var(--primary-blue); margin-bottom: 0.5rem;">Residential Analysis</h4>
                            <p style="color: #64748b;">Comprehensive valuation for homes, apartments, and luxury estates.</p>
                        </div>
                    </div>
                    <div class="property-card reveal-scale" style="animation-delay: 0.1s;">
                        <div class="section-image-overlay">
                            <img src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=600" 
                                 alt="Commercial Property">
                        </div>
                        <div style="padding: 2rem; background: white;">
                            <h4 style="font-family: var(--font-display); color: var(--primary-blue); margin-bottom: 0.5rem;">Commercial Insights</h4>
                            <p style="color: #64748b;">Office buildings, retail spaces, and investment properties analyzed with precision.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def create_premium_divider():
    """Create premium section divider with wave animation"""
    st.markdown("""
        <div class="section-divider">
            <div class="divider-wave"></div>
        </div>
    """, unsafe_allow_html=True)

def apply_premium_enhancements():
    """Apply all premium UI enhancements to the app"""
    load_premium_css()
    create_hero_section()
    create_stats_section()
    create_premium_divider()
    create_analytics_showcase()
    create_premium_divider()
    create_smart_city_section()
    create_premium_divider()
    create_ai_technology_section()
    create_premium_divider()
    create_property_showcase()

def create_premium_metric_card(title, value, icon, color="gold"):
    """Create a premium animated metric card"""
    colors = {
        "gold": "var(--gradient-gold)",
        "blue": "var(--gradient-primary)",
        "emerald": "linear-gradient(135deg, #10b981, #059669)"
    }
    
    st.markdown(f"""
        <div class="glass-card luxury-hover reveal-scale" style="text-align: center;">
            <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
            <div class="stats-counter" style="background: {colors.get(color, colors['gold'])}; -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                {value}
            </div>
            <div class="stats-label">{title}</div>
        </div>
    """, unsafe_allow_html=True)

def create_premium_chart_container(title, chart_html):
    """Wrap a chart in a premium container"""
    st.markdown(f"""
        <div class="chart-container">
            <h3 style="color: var(--primary-gold); font-family: var(--font-display); margin-bottom: 1.5rem;">
                {title}
            </h3>
            {chart_html}
        </div>
    """, unsafe_allow_html=True)

def show_premium_loading():
    """Show premium loading animation"""
    st.markdown("""
        <div style="display: flex; justify-content: center; align-items: center; min-height: 200px;">
            <div class="premium-loader"></div>
        </div>
    """, unsafe_allow_html=True)

