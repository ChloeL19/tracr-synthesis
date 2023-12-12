'''
For future reference with downloading model files:

import streamlit as st
import pickle
import base64

x = {"my": "data"}

def download_model(model):
    output_model = pickle.dumps(model)
    b64 = base64.b64encode(output_model).decode()
    href = f'<a href="data:file/output_model;base64,{b64}" download="myfile.pkl">Download Trained Model .pkl File</a>'
    st.markdown(href, unsafe_allow_html=True)


download_model(x)
'''