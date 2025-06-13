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
    - Draw their own cancer mask on a mammogram.
    - Compare their mask against the labeled ground truth mask.
    - Evaluate their results using the Intersection over Union (IoU) score.

    **👈 Select a page from the sidebar** to try the diagnosis tool, draw masks, or explore model performance.

    ### Learn more:
    - Explore the [Streamlit documentation](https://docs.streamlit.io) for app building tips.
    - Visit [Breast Cancer Research](https://www.cancer.org/cancer/breast-cancer.html) for more info on mammography.
    """
)
