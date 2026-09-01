import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(
    page_title="Flora AI - Universal Botanical Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Read API key securely from Streamlit Secrets or code fallback
try:
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except Exception:
    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    * {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }

    .stApp {
        background-color: #0b0f19;
        color: #f1f5f9;
    }

    .brand-header {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 28px;
    }

    .brand-title {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .result-card {
        background: #151c2c;
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 20px;
    }

    .status-badge {
        background: rgba(34, 197, 94, 0.15);
        color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }

    .stImage > img {
        border-radius: 14px;
        border: 1px solid #1e293b;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="brand-header">
        <div>
            <h1 class="brand-title">🌿 Flora AI Universal Identifier</h1>
            <p style="margin:4px 0 0 0; color:#94a3b8; font-size:0.95rem;">AI-Powered Universal Species Identification & Care Engine</p>
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 1.1], gap="large")

with col1:
    st.subheader("📷 Upload Any Flower Image")
    uploaded_file = st.file_uploader("Select JPG or PNG file...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Preview', use_container_width="stretch")

with col2:
    st.subheader("📊 AI Identification & Botanical Care")
    
    if uploaded_file is not None:
        with st.spinner("Analyzing flower features with Universal AI..."):
            try:
                client = genai.Client(api_key=GEMINI_API_KEY)
                
                prompt = """
                Analyze this flower image and output the details in exact Markdown format as follows:
                
                ### [Flower Common Name]
                
                **Scientific Name:** *[Scientific Name]*  
                **Botanical Family:** [Family Name]  
                
                #### 📖 Description
                [2-3 sentences overview]
                
                #### 🌱 Care Guidelines
                - ☀️ **Sunlight:** [Sunlight Requirement]
                - 💧 **Watering:** [Watering Requirement]
                - 🟤 **Soil:** [Soil Preference]
                """
                
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=[prompt, image]
                )
                
                st.markdown("""
                    <div class="result-card">
                        <span class="status-badge">● Universal AI Identification Active</span>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown(response.text)

            except Exception as e:
                st.error(f"Error analyzing image: {str(e)}")
    else:
        st.info("Upload any flower photo on the left panel to get full botanical identification and care details.")
