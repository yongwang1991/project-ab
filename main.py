import streamlit as st  
from helper_functions.utility import check_password  
from helper_functions import llm 

st.title("Streamlit App")

# Check if the password is correct.  
if not check_password():  
    st.stop()

# st.write("hello world!")

## template prompt code ##
# form = st.form(key="form")
# form.subheader("Prompt")

# user_prompt = form.text_area("Enter your prompt here", height=200)

# if form.form_submit_button("Submit"):
#     st.toast(f"User Input Submitted - {user_prompt}")
#     response = llm.get_completion(user_prompt) 
#     st.write(response) 
#     print(f"User Input is {user_prompt}")
## template prompt code ##

col1, col2 = st.columns(2)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a public sector procurement officer in the Singapore public service. You are helping to draft the requirements specifications for a tender."},
        {"role": "assistant", "content": "Hi. What would you like to procure today?"}
    ]

with col1:
    st.container(height=500)

with col2:
    chatcontainer = st.container(height=500)
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with chatcontainer.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("What is up?"):
        # Display user message in chat message container
        chatcontainer.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": f"{prompt}" })

        response = llm.get_completion_by_messages(st.session_state.messages)
        # Display assistant response in chat message container
        with chatcontainer.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})