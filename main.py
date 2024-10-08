import streamlit as st  
from helper_functions.utility import check_password  
from helper_functions import llm 

st.title("Streamlit App")

# Check if the password is correct.  
if not check_password():  
    st.stop()

# st.write("hello world!")

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    response = llm.get_completion(user_prompt) 
    st.write(response) 
    print(f"User Input is {user_prompt}")