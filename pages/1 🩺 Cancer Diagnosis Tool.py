import os
import streamlit as st
import requests

st.set_page_config(
    page_title="Cancer Diagnosis Tool",
    page_icon=":stethoscope:",
)

# Load API base URI from secrets or environment
if 'API_URI' in os.environ:
    BASE_URI = st.secrets[os.environ.get('API_URI')]
else:
    BASE_URI = st.secrets['cloud_api_uri']

BASE_URI = BASE_URI if BASE_URI.endswith('/') else BASE_URI + '/'

st.markdown("## B.O.O.B.S. Deep Learning Suite 🍈🍈")
#st.markdown(f"Backend: `{BASE_URI}`")

st.markdown("Upload a medical image and select a task")

# Upload image
uploaded_file = st.file_uploader("Upload an image (PNG/JPG format)", type=['png', 'jpg', 'jpeg'])

# Task selection
task = st.selectbox("Select a task", ["Is there cancer?", "Where is the cancer?"])

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
            try:
                result = response.json()
                prob = float(result.get("probability"))

                if prob is None:
                    st.error("✅ API returned successfully, but no probability was found in the response.")
                    st.write("Full response:", result)
                else:
                    st.success(f"🎯 Prediction: **{prob * 100:.2f}% malignant**")
            except Exception as e:
                st.error(f"❌ Failed to parse prediction response: {e}")
                st.write("Raw response content:", response.text)

        # ✅ Segmentation result (image)
        elif task == "Where is the cancer?":
            st.markdown(
            "🔴 **Red areas** on the mammogram represent the regions predicted by the segmentation model as potentially cancerous."
            )
            st.image(response.content, caption="🩺 Segmentation Output", use_container_width=True)
