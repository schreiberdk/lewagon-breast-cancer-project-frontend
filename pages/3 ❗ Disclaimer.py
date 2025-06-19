import streamlit as st

st.title("Disclaimer")

st.markdown("""
**Disclaimer**

This application is a research project and is **not intended for clinical use or medical diagnosis**.
The classification and segmentation models presented here are experimental and have not been validated in a clinical setting.
The results produced should **not** be used to make healthcare decisions.

If you have any medical concerns, please consult a licensed healthcare professional.

By using this application, you acknowledge that:
- It is for **educational and demonstration purposes only**
- The developers make **no guarantees** about its accuracy
- You are **solely responsible** for how you use the output

""")


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
