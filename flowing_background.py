# © 2025 Dowek Analytics Ltd.
# ORACLE SAMUEL – Flowing Blue Lines Background
# MD5-Protected AI System. Unauthorized use prohibited.

def get_flowing_background_css():
    """Create the flowing blue lines background CSS"""
    return """
    <style>
    .stApp {
        background: #ffffff;
        background-image: 
            radial-gradient(circle at 20% 20%, rgba(135, 206, 250, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(173, 216, 230, 0.2) 0%, transparent 50%),
            radial-gradient(circle at 40% 60%, rgba(176, 224, 230, 0.25) 0%, transparent 50%),
            linear-gradient(135deg, rgba(135, 206, 250, 0.1) 0%, transparent 30%),
            linear-gradient(45deg, rgba(173, 216, 230, 0.08) 0%, transparent 40%);
        background-size: 
            800px 800px,
            600px 600px,
            1000px 1000px,
            100% 100%,
            100% 100%;
        background-position: 
            -200px -200px,
            100% 100%,
            50% 50%,
            0% 0%,
            0% 0%;
        background-repeat: no-repeat;
        background-attachment: fixed;
        position: relative;
    }
    
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            linear-gradient(45deg, transparent 30%, rgba(135, 206, 250, 0.05) 50%, transparent 70%),
            linear-gradient(-45deg, transparent 20%, rgba(173, 216, 230, 0.03) 40%, transparent 60%),
            linear-gradient(90deg, transparent 10%, rgba(176, 224, 230, 0.04) 30%, transparent 50%);
        background-size: 
            1200px 1200px,
            800px 800px,
            600px 600px;
        background-position: 
            -300px -300px,
            50% 50%,
            100% 0%;
        background-repeat: no-repeat;
        pointer-events: none;
        z-index: -1;
    }
    
    .stApp::after {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(ellipse at 15% 15%, rgba(135, 206, 250, 0.15) 0%, transparent 60%),
            radial-gradient(ellipse at 85% 85%, rgba(173, 216, 230, 0.1) 0%, transparent 70%),
            radial-gradient(ellipse at 30% 70%, rgba(176, 224, 230, 0.12) 0%, transparent 65%);
        background-size: 
            900px 600px,
            700px 500px,
            800px 700px;
        background-position: 
            -100px -100px,
            100% 100%,
            50% 50%;
        background-repeat: no-repeat;
        pointer-events: none;
        z-index: -1;
    }
    
    /* Flowing lines animation */
    @keyframes flow {
        0% { transform: translateX(-100px) translateY(-50px) rotate(0deg); opacity: 0; }
        50% { opacity: 0.3; }
        100% { transform: translateX(100px) translateY(50px) rotate(360deg); opacity: 0; }
    }
    
    .flowing-lines {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: -1;
        overflow: hidden;
    }
    
    .flowing-line {
        position: absolute;
        background: linear-gradient(45deg, rgba(135, 206, 250, 0.2), rgba(173, 216, 230, 0.1));
        border-radius: 2px;
        animation: flow 8s ease-in-out infinite;
    }
    
    .flowing-line:nth-child(1) {
        width: 200px;
        height: 2px;
        top: 20%;
        left: -200px;
        animation-delay: 0s;
        animation-duration: 12s;
    }
    
    .flowing-line:nth-child(2) {
        width: 150px;
        height: 1px;
        top: 40%;
        left: -150px;
        animation-delay: 2s;
        animation-duration: 10s;
    }
    
    .flowing-line:nth-child(3) {
        width: 180px;
        height: 2px;
        top: 60%;
        left: -180px;
        animation-delay: 4s;
        animation-duration: 14s;
    }
    
    .flowing-line:nth-child(4) {
        width: 120px;
        height: 1px;
        top: 80%;
        left: -120px;
        animation-delay: 6s;
        animation-duration: 11s;
    }
    
    .flowing-line:nth-child(5) {
        width: 160px;
        height: 2px;
        top: 30%;
        left: -160px;
        animation-delay: 8s;
        animation-duration: 13s;
    }
    
    /* Enhanced card styling for the flowing background */
    .flowing-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        border: 1px solid rgba(135, 206, 250, 0.2);
        box-shadow: 0 8px 32px rgba(135, 206, 250, 0.1);
        transition: all 0.3s ease;
    }
    
    .flowing-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 40px rgba(135, 206, 250, 0.15);
        border-color: rgba(135, 206, 250, 0.3);
    }
    
    .flowing-header {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 30px;
        margin: 20px 0;
        border: 1px solid rgba(135, 206, 250, 0.2);
        box-shadow: 0 8px 32px rgba(135, 206, 250, 0.1);
        text-align: center;
    }
    
    .flowing-button {
        background: linear-gradient(135deg, rgba(135, 206, 250, 0.8), rgba(173, 216, 230, 0.6));
        border: 1px solid rgba(135, 206, 250, 0.3);
        border-radius: 25px;
        color: #2c3e50;
        font-weight: bold;
        padding: 12px 24px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(135, 206, 250, 0.2);
    }
    
    .flowing-button:hover {
        background: linear-gradient(135deg, rgba(135, 206, 250, 0.9), rgba(173, 216, 230, 0.7));
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(135, 206, 250, 0.3);
    }
    
    .flowing-metric {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        border: 1px solid rgba(135, 206, 250, 0.2);
        text-align: center;
        box-shadow: 0 4px 15px rgba(135, 206, 250, 0.1);
    }
    
    .flowing-text {
        color: #2c3e50;
        text-shadow: 0 1px 2px rgba(255, 255, 255, 0.8);
    }
    
    /* Custom scrollbar for flowing theme */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(135, 206, 250, 0.1);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, rgba(135, 206, 250, 0.6), rgba(173, 216, 230, 0.4));
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, rgba(135, 206, 250, 0.8), rgba(173, 216, 230, 0.6));
    }
    </style>
    """

def add_flowing_lines():
    """Add animated flowing lines"""
    return """
    <div class="flowing-lines">
        <div class="flowing-line"></div>
        <div class="flowing-line"></div>
        <div class="flowing-line"></div>
        <div class="flowing-line"></div>
        <div class="flowing-line"></div>
    </div>
    """

def apply_flowing_background():
    """Apply the flowing blue lines background to Streamlit"""
    import streamlit as st
    
    st.markdown(get_flowing_background_css(), unsafe_allow_html=True)
    st.markdown(add_flowing_lines(), unsafe_allow_html=True)

def flowing_header(title, subtitle=""):
    """Create a flowing-themed header"""
    return f"""
    <div class="flowing-header">
        <h1 style="color: #2c3e50; font-size: 3rem; margin: 0; text-shadow: 0 2px 4px rgba(255,255,255,0.8);">
            {title}
        </h1>
        {f'<h3 style="color: #34495e; font-size: 1.5rem; margin: 10px 0; text-shadow: 0 1px 2px rgba(255,255,255,0.8);">{subtitle}</h3>' if subtitle else ''}
    </div>
    """

def flowing_card(content, title=""):
    """Create a flowing-themed card"""
    return f"""
    <div class="flowing-card">
        {f'<h3 style="color: #2c3e50; margin-bottom: 15px; text-shadow: 0 1px 2px rgba(255,255,255,0.8);">{title}</h3>' if title else ''}
        <div class="flowing-text">
            {content}
        </div>
    </div>
    """

def flowing_metric(label, value, delta=""):
    """Create a flowing-themed metric"""
    return f"""
    <div class="flowing-metric">
        <div style="color: #2c3e50; font-size: 1.2rem; font-weight: bold; margin-bottom: 5px;">{label}</div>
        <div style="color: #3498db; font-size: 2rem; font-weight: bold; margin-bottom: 5px;">{value}</div>
        {f'<div style="color: #e74c3c; font-size: 1rem;">{delta}</div>' if delta else ''}
    </div>
    """

if __name__ == "__main__":
    print("Flowing Blue Lines Background Module for Oracle Samuel")
    print("Ready for integration with main application")
