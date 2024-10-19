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

# Initialize assistant
if "background" "message" "stage" not in st.session_state:
    st.session_state.background = [
        {"role": "system", "content": "You are a public sector procurement officer in the Singapore public service. You are helping to draft the requirements specifications for a tender."},
        {"role": "user", "content" : ""}
    ]
    st.session_state.stage = {"current": 0, "max": 0}
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi. What would you like to procure today?"}
    ]


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
        st.session_state.background[1]["content"] = prompt

        # response = llm.get_completion_by_messages(st.session_state.messages)
        # # Display assistant response in chat message container
        # with chatcontainer.chat_message("assistant"):
        #     st.markdown(response)
        # # Add assistant response to chat history
        # st.session_state.messages.append({"role": "assistant", "content": response})

        if st.session_state.stage["current"] == 0:
            system_instructions = [{"role": "system", "content": """
            You are to reply with the key cost components of the user's requirement in an array. For example, for a dinner and dance event, the key cost components are ["venue", "food", "emcee", "photo booth"]. 
            """}]
            built_prompt = st.session_state.messages
            built_prompt.insert(0,st.session_state.background[0]) 
            built_prompt.extend(system_instructions)
            # print(built_prompt)
            response = llm.get_completion_by_messages(built_prompt)
            with chatcontainer.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with col1:
    with st.container(height=500):
        st.session_state

