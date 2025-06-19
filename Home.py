import streamlit as st


st.set_page_config(
    page_title="B.O.O.B.S.",
    page_icon="🏠",
)

st.write("# Welcome to B.O.O.B.S. 👋")
st.write("#### Better Oncology Outcomes from Binary and Segmentation")

st.markdown(
    """
    This LeWagon Data Science and AI Coding Bootcamp project focuses on improving breast cancer detection and localization using AI models on mammography images.

    We develop two core models:
    - **Classification model:** Determines whether cancer is present in a mammogram.
    - **Segmentation model:** Identifies the precise location of cancer by segmenting the affected areas.

    Additionally, we provide an interactive tool where users can:
    - Draw their own cancer prediction on a mammogram,
    - Compare their prediction against a radiologist diagnosis,
    - Evaluate their results using the Intersection over Union (IoU) score,
    - and finally see our segmentation model's prediction.

    **👈 Select a page from the sidebar** to try the diagnosis tool or try to find cancer in mammograms.

    ### Learn more:
    - Explore the [Streamlit documentation](https://docs.streamlit.io) for app building tips.
    - Visit [Breast Cancer Research](https://www.cancer.org/cancer/breast-cancer.html) for more info on mammography.
    """
)



# Custom CSS injection
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
