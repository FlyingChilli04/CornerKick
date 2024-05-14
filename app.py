import streamlit as st
from predictor_page import show_predict_page

show_predict_page()


footer_html = """
<hr>
<p style="text-align:center;">
    Disclaimer: Please do not use for betting purposes |
    Data for the model was extracted from <a href="https://fbref.com/en/comps/9/Premier-League-Stats">FBref</a>
</p>
"""
st.markdown(footer_html, unsafe_allow_html=True)