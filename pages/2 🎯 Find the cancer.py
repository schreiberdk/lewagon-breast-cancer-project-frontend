import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import io
import base64
import os
import numpy as np
import matplotlib.pyplot as plt
import glob
import requests

st.set_page_config(
    page_title="Find the cancer",
    page_icon=":dart:",
)

# --- Helper: Convert PIL image to base64-encoded data URI ---
def image_to_data_url(img: Image.Image) -> str:
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    base64_str = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{base64_str}"

# --- Load files ---
st.markdown("## Find the cancer")

# --- List available image files ---
image_files = sorted(glob.glob("images/*.png"))  # or .jpg, etc.

if not image_files:
    st.error("No images found in 'images/' folder.")
    st.stop()

# Extract just filenames for display
image_names = [os.path.basename(path) for path in image_files]

# Dropdown to select image
selected_image_name = st.selectbox("Select an image", image_names)

# Build paths for selected image and corresponding mask
selected_image_path = os.path.join("images", selected_image_name)
selected_mask_path = os.path.join("masks", selected_image_name)  # assumes mask has same filename in 'masks/'

# Check files exist
if not os.path.exists(selected_image_path) or not os.path.exists(selected_mask_path):
    st.error(f"Image or mask not found for selection: {selected_image_name}")
    st.stop()

# Load selected images
image = Image.open(selected_image_path).resize((512, 512))
mask_gt = Image.open(selected_mask_path).convert("L").resize((512, 512))

st.markdown("### Can you find the cancer? Draw on the image:")

# Convert image to data URI
bg_image_url = image_to_data_url(image.convert("RGB"))

# --- Drawing canvas ---
canvas_result = st_canvas(
    fill_color="#EEE0E0",
    stroke_width=6,
    stroke_color="#FF0000",
    background_image=image.convert("RGBA"),
    update_streamlit=True,
    height=512,
    width=512,
    drawing_mode="freedraw",
    key=f"canvas_{selected_image_name}"
)


def overlay_mask_on_image(image_pil, mask_np, mask_color=(255, 0, 0, 100)):
    """
    Overlay a binary mask on top of a PIL image with transparency.

    Args:
        image_pil (PIL.Image): Original RGB image.
        mask_np (np.ndarray): 2D binary mask (0/1 or 0/255).
        mask_color (tuple): RGBA color for mask overlay (default: semi-transparent red).

    Returns:
        PIL.Image: Image with mask overlay.
    """
    # Make sure mask is binary 0 or 255 for alpha
    mask_img = Image.fromarray((mask_np * 255).astype(np.uint8)).convert("L")

    # Create an RGBA version of the original image
    image_rgba = image_pil.convert("RGBA")

    # Create a color image the same size as mask
    color_mask = Image.new("RGBA", image_pil.size, mask_color)

    # Put mask as alpha channel on the color mask
    color_mask.putalpha(mask_img)

    # Composite the mask onto the original image
    combined = Image.alpha_composite(image_rgba, color_mask)

    return combined



if st.button("Submit"):
    if canvas_result.image_data is not None:
        alpha_channel = canvas_result.image_data[:, :, 3]
        if np.any(alpha_channel > 0):
            user_mask = canvas_result.image_data[:, :, 3] > 0
            user_mask = user_mask.astype(np.uint8)

            # Ground truth binary mask
            mask_gt_np = np.array(mask_gt)
            mask_gt_bin = (mask_gt_np > 127).astype(np.uint8)

            # Compute IOU
            intersection = np.logical_and(user_mask, mask_gt_bin).sum()
            union = np.logical_or(user_mask, mask_gt_bin).sum()
            iou = intersection / union if union != 0 else 0.0

            st.subheader(f"🎯 Target Score: **{iou*100:.0f}%**")

            # User and GT overlays
            user_overlay = overlay_mask_on_image(image, user_mask)
            gt_overlay = overlay_mask_on_image(image, mask_gt_bin)

            col1, col2 = st.columns(2)
            with col1:
                st.image(user_overlay, caption="👩‍💻 Your prediction", use_container_width=True)
            with col2:
                st.image(gt_overlay, caption="👩‍⚕️ Radiologist diagnosis", use_container_width=True)

            # --- Call your segmentation API ---
            try:
                col1, col2, col3  = st.columns([1, 3, 1])  # Two equal-width columns
                with col2:
                    api_uri = st.secrets.get("cloud_api_uri", os.environ.get("API_URI"))
                    endpoint = "segmentation"
                    url = api_uri.rstrip("/") + "/" + endpoint

                    with open(selected_image_path, "rb") as f:
                        files = {'img': f}
                        with st.spinner("Sending to segmentation model..."):
                            response = requests.post(url, files=files)

                    if response.status_code == 200:
                        model_mask_img = Image.open(io.BytesIO(response.content)).resize((512, 512))
                        st.image(model_mask_img, caption="🤖 Model prediction", use_container_width=True)
                    else:
                        st.warning(f"Model API failed: {response.status_code} — {response.text}")

            except Exception as e:
                st.error(f"Failed to contact model API: {e}")

        else:
            st.error("Please draw a mask before submitting.")

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

    /* Style the Submit button */
    div.stButton > button {
        background-color: #635088;     /* Button background */
        color: #FFFFFF;                /* Text color */
        border: 3px solid #443366;     /* Border color */
        border-radius: 6px;            /* Optional: rounded corners */
        padding: 0.5em 1.5em;          /* Optional: padding */
        font-weight: bold;
        transition: all 0.2s ease;
    }

    /* Optional: style on hover */
    div.stButton > button:hover {
        background-color: #7a69a0;
        border-color: #32254e;
        color: #ffffff;
    }



    </style>
""", unsafe_allow_html=True)
