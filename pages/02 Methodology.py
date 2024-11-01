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
    st.write("1. NA. The app uses the training data of the llm to generate the Requirements Specifications. There is no specific data provided as the intention is to tap on the generative ability of the llm to draft the Requirements Specifications.")

with st.expander("Implementation Details"):
    st.write("1. Enter your prompt in the text area. For example, enter the following: Draft the specifications for establishing a 3 years period contract for purchasing movie tickets.")
    st.write("2. Click the 'Submit' button.")
    st.write("3. The app will first generate the list of main sections based on your prompt.")
    st.write("4. If the generated specifications require improvements, add a liner or two to try again. For example, enter the following prompt: Remove the last section.")
    st.write("5. Once you are happy with the main sections, the app will start developing the draft of the Requirements Specifications section by section.")
    st.write("6. You may iterate with the app to refine the drafts of each section. Once you are happy, the draft section will be committed to the finalised version.")
    st.write("7. Once all the sections are completed, you may go to the 'Finalised' tab to extract the entire Requirements Specifications.")


with st.expander("Flowchart"):
    st.image("app/assets/Detailed Process Workflow.png")
