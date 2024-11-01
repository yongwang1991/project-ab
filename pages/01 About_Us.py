import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Specifications Drafter"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("This is a Specifications Drafter which is designed to help PMTs to come out with the first draft of the specifications for the purchase. We hope it will speed up the procurement process for you.")

with st.expander("Project Scope"):
    st.write("To address the challenges PMTs face in drafting requirement specifications, an automated Requirement Specifications Generator is created to reduce the time spent significantly.")
             
with st.expander("Project Objectives"):
    st.write("1. Reduce Lead Time: Minimise time taken to draft requirement specifications.")
    st.write("2. User-Friendly Interface: Provide an intuitive interface so that PMTs to easily generate specifications.")
    st.write("3. Enhance Consistency: Ensure uniformity to draft specifications across different projects.")


with st.expander("Data Sources"):
    st.write("1. Enter your prompt in the text area.")

with st.expander("Features"):
    st.write("1. Enter your prompt in the text area. For example, enter the following: Draft the specifications for establishing a 3 years period contract for purchasing movie tickets.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will generate the draft specfications based on your prompt.")
    st.write("4. If the generated specifications require improvements, add a liner or two to refine the prompt and try again.")
    st.write("5. It is that simple. Give it a try!")