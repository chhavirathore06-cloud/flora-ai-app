import streamlit as st
from google import genai
from PIL import Image
import time

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
            <h1 class="brand-title">🌿 Flora AI Universal Intelligence</h1>
            <p style="margin:4px 0 0 0; color:#94a3b8; font-size:0.95rem;">AI-Powered Identification, Care & Plant/Crop Disease Doctor</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Helper function to call Gemini API with retry mechanism
def generate_response_with_retry(client, prompt, image, retries=3):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model='gemini-3.6-flash',
                contents=[prompt, image]
            )
            return response
        except Exception as e:
            if "503" in str(e) and attempt < retries - 1:
                time.sleep(2)  # Wait 2 seconds before retrying
                continue
            raise e

# Tabs for separate features
tab1, tab2 = st.tabs(["🌸 Plant, Tree & Crop Identification", "🩺 Disease & Pest Doctor"])

# --- TAB 1: IDENTIFICATION & CARE ---
with tab1:
    col1, col2 = st.columns([1, 1.1], gap="large")

    with col1:
        st.subheader("📷 Upload Any Plant, Flower, Tree or Crop")
        uploaded_file = st.file_uploader("Select JPG or PNG file...", type=["jpg", "jpeg", "png"], key="upload_ident")
        
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption='Uploaded Preview', use_container_width=True)

    with col2:
        st.subheader("📊 AI Identification & Care Guidelines")
        
        if uploaded_file is not None:
            with st.spinner("Analyzing plant details with Universal AI..."):
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    
                    prompt = """
                    Analyze this plant, flower, tree, or crop image and output the details in exact Markdown format:
                    
                    ### [Common Name]
                    
                    **Scientific Name:** *[Scientific Name]*  
                    **Botanical Family:** [Family Name]  
                    **Category:** [Flower / Tree / Indoor Plant / Crop / Herb]  
                    
                    #### 📖 Description
                    [2-3 sentences overview about the plant/crop]
                    
                    #### 🌱 Growth & Care Guidelines
                    - ☀️ **Sunlight:** [Sunlight Requirement]
                    - 💧 **Watering:** [Watering Requirement]
                    - 🟤 **Soil & Fertilizer:** [Soil Preference & Recommended Fertilizer]
                    """
                    
                    response = generate_response_with_retry(client, prompt, image)
                    
                    st.markdown("""
                        <div class="result-card">
                            <span class="status-badge">● Universal AI Identification Active</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(response.text)

                except Exception as e:
                    if "503" in str(e):
                        st.warning("Google AI server temporary busy hai. Kripya 5-10 second baad dobara upload/try karein.")
                    else:
                        st.error(f"Error analyzing image: {str(e)}")
        else:
            st.info("Upload any plant, tree, or crop photo on the left panel to get full identification and care details.")

# --- TAB 2: DISEASE & PEST DOCTOR ---
with tab2:
    col3, col4 = st.columns([1, 1.1], gap="large")

    with col3:
        st.subheader("⚠️ Upload Problematic Plant/Crop Photo")
        st.write("Upload photo showing insects, yellow/damaged leaves, fungus, or pest attacks.")
        uploaded_disease_file = st.file_uploader("Select Affected Image...", type=["jpg", "jpeg", "png"], key="upload_disease")
        
        if uploaded_disease_file is not None:
            disease_image = Image.open(uploaded_disease_file)
            st.image(disease_image, caption='Affected Area Preview', use_container_width=True)

    with col4:
        st.subheader("🩺 Diagnosis & Prevention Report")
        
        if uploaded_disease_file is not None:
            with st.spinner("Diagnosing disease & pest issues..."):
                try:
                    client = genai.Client(api_key=GEMINI_API_KEY)
                    
                    prompt_disease = """
                    Analyze this image of a plant, tree, or crop for health issues, diseases, pest/insect attacks, or nutrient deficiencies.
                    Output the details in exact Markdown format:
                    
                    ### Diagnosis: [Identified Disease/Pest Name or Healthy]
                    
                    **Plant/Crop Name:** [Identified Plant]  
                    **Health Status:** [Healthy / Mild Issue / Severe Disease / Insect Attack]  
                    
                    #### 🔍 Symptoms Detected
                    [List 2-3 visible symptoms observed in the image]
                    
                    #### 🛡️ Prevention & Treatment Plan
                    - ✂️ **Immediate Action:** [First step, e.g., trim infected leaves, isolate]
                    - 🌿 **Organic Treatment:** [Natural remedies, e.g., Neem oil, organic soap spray]
                    - 🧪 **Chemical Treatment:** [Recommended pesticides/fungicides if required]
                    - 🔮 **Future Prevention:** [Tips to avoid this problem in future]
                    """
                    
                    response_disease = generate_response_with_retry(client, prompt_disease, disease_image)
                    
                    st.markdown("""
                        <div class="result-card">
                            <span class="status-badge">● Disease & Pest Analysis Active</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(response_disease.text)

                except Exception as e:
                    if "503" in str(e):
                        st.warning("Google AI server temporary busy hai. Kripya 5-10 second baad dobara try karein.")
                    else:
                        st.error(f"Error diagnosing image: {str(e)}")
        else:
            st.info("Upload an image of a damaged leaf or crop on the left panel to get diagnosis and treatment remedies.")
