import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="Specifications Drafter"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write("This is a Specifications Drafter which is designed to help PMTs to come out with the first draft of the specifications for the purchase. We hope it will speed up the procurement process for you.")

with st.expander("Data Flows"):
    st.write("1. Enter your prompt in the text area.")

with st.expander("Implementation Details"):
    st.write("1. Enter your prompt in the text area.")   


with st.expander("Flowchart"):
    st.image("Detailed Process Workflow.png")