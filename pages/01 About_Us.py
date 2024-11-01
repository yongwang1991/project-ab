import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Specifications Drafter"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("This is a Requirements Specifications Drafter which is designed to help Users/PMTs to develop the first draft of the specifications for their Tender/Quotation.")

with st.expander("Project Scope"):
    st.write("To address the challenges Users/PMTs face in drafting their requirement specifications, an automated Requirement Specifications Generator is created to reduce the time spent to develop the first draft significantly.")
             
with st.expander("Project Objectives"):
    st.write("1. Provide Guidance: To provide guidance for Users/PMTs to develop the first draft of their requirements specifications.")
    st.write("2. Reduce Lead Time: Minimise time taken to develop the draft requirement specifications.")
    st.write("3. User-Friendly Interface: Provide an intuitive interface so that Users/PMTs can easily generate the requirements specifications.")


with st.expander("Data Sources"):
    st.write("1. NA. The idea is to tap on the wide training data of the LLM to develop the requirements specifications.")

with st.expander("Features"):
    st.write("1. Generative Ability. The app is able to generate the Requirements Specifcations based on user prompt, without any additional data provided.")
    st.write("2. Context Awareness. The app is able to generate specifications for the specific section of the Requirements Specifications.")
    st.write("3. User Feedback Mechanism. The app is able to modify or amend its replies based on the user feedback.")
