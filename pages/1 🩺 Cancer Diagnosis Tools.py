import os
import streamlit as st
import requests

st.set_page_config(
    page_title="Cancer Diagnosis Tools",
    page_icon=":stethoscope:",
)

# Load API base URI from secrets or environment
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']

BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'

st.markdown("## Cancer Diagnosis Tools")
#st.markdown(f"Backend: `{BASE_URI}`")

st.markdown("Upload a medical image and select a task")


st.markdown("""
    <style>
    /* Target the file uploader label */
    .stFileUploader label {
        color: #545454;  /* Tomato red, change to your preferred color */
        font-weight: bold;  /* Optional */
    }

    .stFileUploader div[data-baseweb="select"] > div:first-child {
        background-color: #f7b2a5;  /* change to desired bar color */
        color: black;  /* change to desired text color */
    }
    </style>
""", unsafe_allow_html=True)

# Upload image
uploaded_file = st.file_uploader("Upload an image (PNG/JPG format)", type=['png', 'jpg', 'jpeg'])

# Task selection
task = st.selectbox("Select a task", ["Is there cancer?", "Where is the cancer?"])

threshold = 0.13450709

if uploaded_file and task:
    endpoint = "classification" if task == "Is there cancer?" else "segmentation"
    url = BASE_URI + endpoint

    #st.markdown(f"**Sending request to:** `{url}`")

    with st.spinner("Processing..."):
        try:
            files = {'img': uploaded_file}
            response = requests.post(url, files=files)
        except Exception as e:
            st.error(f"❌ Failed to contact API: {e}")
            st.stop()

        if response.status_code != 200:
            st.error(f"❌ API error {response.status_code}: {response.text}")
            st.stop()

        # ✅ Classification result
        if task == "Is there cancer?":
            col1, col2, col3  = st.columns([1, 3, 1])  # Two equal-width columns

            with col2:
                st.markdown("### 📷 Input Image")
                st.image(uploaded_file, caption="Uploaded Mammogram", use_container_width=True)

            try:
                result = response.json()
                prob = float(result.get("probability"))
                with col2:
                    if prob is None:
                        st.error("✅ API returned successfully, but no probability was found in the response.")
                        st.write("Full response:", result)
                    else:
                        if prob > threshold:
                            #st.success(f"🎯 Predicted probability of cancer presence: **{prob * 100:.2f}%**")
                            st.error(f"Cancer is likely present.")
                        else:
                            st.success(f"Image is likely cancer free!")
            except Exception as e:
                st.error(f"❌ Failed to parse prediction response: {e}")
                st.write("Raw response content:", response.text)

        # ✅ Segmentation result (image)
        elif task == "Where is the cancer?":
            col1, col2, col3  = st.columns([1, 3, 1])  # Two equal-width columns
            with col2:
                st.markdown(
                "🔴 **Red areas** are predicted as possibly cancerous 🔴"
                )
                st.image(response.content, caption="🩺 Segmentation Output", use_container_width=True)


st.markdown("""
    <style>
    /* Set background color for entire page */
    .stApp {
        background-color: #EEE0E0;
        color: #545454;  /* default text color */
        font-family: 'Malik', sans-serif;  /* change font */
    }

    /* Optional: style headings */
    h1, h2, h3, h4, h5, h6 {
        color: #635088;  /* dark blue headings */
    }

    /* Sidebar container */
    section[data-testid="stSidebar"] {
        color: #545454;              /* Text color */
        background-color: #EEE0E0;   /* Optional: change sidebar background */
    }

    /* Make sure links and other text are also white */
    section[data-testid="stSidebar"] * {
        color: #545454 !important;
    }

    /* Optional: change default font size */
    html, body, [class*="css"] {
         font-size: 16px;
    }

    /* Change background color of the top bar */
    header[data-testid="stHeader"] {
        background-color: #EEE0E0;  /* Replace with your preferred color */
        color: #545454;
    }

    /* Optional: change the menu text color */
    header[data-testid="stHeader"] * {
        color: #545454; !important;
    }

    </style>
""", unsafe_allow_html=True)
