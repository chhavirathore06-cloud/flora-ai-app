import streamlit as st
from google import genai
from PIL import Image
import time
import io

st.set_page_config(
    page_title="Flora AI - Universal Botanical Intelligence",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fetch all available API Keys from Secrets
api_keys = []
if "GEMINI_API_KEY_1" in st.secrets:
    api_keys.append(st.secrets["GEMINI_API_KEY_1"])
if "GEMINI_API_KEY_2" in st.secrets:
    api_keys.append(st.secrets["GEMINI_API_KEY_2"])
if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"] not in api_keys:
    api_keys.append(st.secrets["GEMINI_API_KEY"])

if not api_keys:
    api_keys = ["YOUR_FALLBACK_API_KEY"]

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    * { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background-color: #0b0f19; color: #f1f5f9; }
    
    .brand-header {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.6) 0%, rgba(15, 23, 42, 0.6) 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 28px;
    }

    .brand-title {
        font-size: 1.8rem; font-weight: 700;
        background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin: 0;
    }

    .result-card {
        background: #151c2c; border: 1px solid #1e293b;
        border-radius: 16px; padding: 16px; margin-bottom: 20px;
    }

    .status-badge {
        background: rgba(34, 197, 94, 0.15); color: #4ade80;
        border: 1px solid rgba(34, 197, 94, 0.3);
        padding: 4px 12px; border-radius: 20px; font-size: 0.85rem;
        font-weight: 600; display: inline-block;
    }

    .stImage > img { border-radius: 14px; border: 1px solid #1e293b; }
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

# Smart Cached API Processor to avoid redundant API hits & rate limit bugs
@st.cache_data(show_spinner=False)
def process_ai_request(image_bytes, prompt):
    image = Image.open(io.BytesIO(image_bytes))
    last_err = None
    
    for key in api_keys:
        client = genai.Client(api_key=key)
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt, image]
                )
                return response.text
            except Exception as e:
                last_err = str(e)
                if "429" in last_err or "503" in last_err or "RESOURCE_EXHAUSTED" in last_err:
                    time.sleep(3)
                    continue
                else:
                    raise e
    raise Exception(last_err)

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
                    
                    file_bytes = uploaded_file.getvalue()
                    result_text = process_ai_request(file_bytes, prompt)
                    
                    st.markdown("""
                        <div class="result-card">
                            <span class="status-badge">● Universal AI Identification Active</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(result_text)

                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        st.warning("⏱️ Rate limit hit. Please wait 15-20 seconds before analyzing a new photo!")
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
                    
                    disease_bytes = uploaded_disease_file.getvalue()
                    disease_result_text = process_ai_request(disease_bytes, prompt_disease)
                    
                    st.markdown("""
                        <div class="result-card">
                            <span class="status-badge">● Disease & Pest Analysis Active</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(disease_result_text)

                except Exception as e:
                    if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                        st.warning("⏱️ Rate limit hit. Please wait 15-20 seconds before analyzing a new photo!")
                    else:
                        st.error(f"Error diagnosing image: {str(e)}")
        else:
            st.info("Upload an image of a damaged leaf or crop on the left panel to get diagnosis and treatment remedies.")
