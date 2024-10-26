import streamlit as st  
import json
from helper_functions.utility import check_password  
from helper_functions import llm 
from helper_functions import system_prompts

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

col1, col2 = st.columns([2,1])

# Initialize assistant
if "background" not in st.session_state:
    st.session_state.background = [
        {"role": "system", "content": system_prompts.system_prompts["background"]},
        {"role": "system", "content" : "["",""]"}
    ]

if "stage" not in st.session_state:
    st.session_state.stage = {"max": 0, "current": 0, "status": "setup"}

if "current_draft" not in st.session_state:
    st.session_state.current_draft = ""

if "sow" not in st.session_state:
    st.session_state.sow = []

if "messages" not in st.session_state:
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
        ##! first engagement with llm to set up the main headers of the scope of work!##
        if st.session_state.stage["current"] == 0 and st.session_state.stage["status"] == "setup":
            # Display user message in chat message container
            chatcontainer.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": f"{prompt}" })

            # Set up the prompt to llm
            system_instructions = [{"role": "system", "content": system_prompts.system_prompts["setup"]}]
            built_prompt = [st.session_state.background[0]] + st.session_state.messages + system_instructions
            response_json = llm.get_completion_by_messages(built_prompt)
            response = json.loads(response_json)

            # Convert llm response in json back into python dictionary
            st.session_state.background[1]["content"] = json.dumps(response["results"])

            # Update system info with user reqt
            st.session_state.stage["max"] = len(response["results"])
            with chatcontainer.chat_message("assistant"):
                st.markdown(response["reply"])
            st.session_state.messages.append({"role": "assistant", "content": response["reply"]})
            st.session_state.stage["status"] = response["next_step"]
        
        ##! confirmationation of the main headers of the scope of work!##
        elif st.session_state.stage["current"] == 0 and st.session_state.stage["status"] == "setup_confirmation":
            # Display user message in chat message container
            chatcontainer.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": f"{prompt}" })

            # Set up the prompt to llm
            system_instructions = [{"role": "system", "content": system_prompts.system_prompts["setup_confirmation"]}]
            built_prompt = st.session_state.background + st.session_state.messages + system_instructions
            response_json = llm.get_completion_by_messages(built_prompt)

            # Convert llm response in json back into python dictionary 
            response = json.loads(response_json)

            # Update system info with latest user reqt
            st.session_state.stage["max"] = len(response["results"])
            st.session_state.background[1]["content"] = json.dumps(response["results"])
            st.session_state.stage["max"] = len(response["results"])
            with chatcontainer.chat_message("assistant"):
                st.markdown(response["reply"])
            st.session_state.messages.append({"role": "assistant", "content": response["reply"]})

            # If user is satisfied, move to the next section to start drafting
            if response["next_step"] == "confirmed":
                st.session_state.stage["status"] = "draft"
                st.session_state.stage["current"] += 1
        
        ##! first draft of the section
        elif st.session_state.stage["current"] <= st.session_state.stage["max"] and st.session_state.stage["status"] == "draft":
            # Display user message in chat message container
            chatcontainer.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": f"{prompt}" })           

            # Set up the prompt to llm
            section_list = json.loads(st.session_state.background[1]["content"])
            current_section = section_list[st.session_state.stage["current"] - 1]
            system_instructions = [{"role": "system", "content": f"You are currently drafting the requirements specifications for the {current_section} section. " + system_prompts.system_prompts["initial_draft"]}]
            built_prompt = st.session_state.background + st.session_state.messages + system_instructions
            response_json = llm.get_completion_by_messages(built_prompt)

            # Convert llm response in json back into python dictionary 
            response = json.loads(response_json)

            # Append llm reply to messages
            with chatcontainer.chat_message("assistant"):
                st.markdown(response["reply"])
            st.session_state.messages.append({"role": "assistant", "content": response["reply"]})

            # Update draft 
            st.session_state.current_draft = response["results"]

            # Change status to confirmation
            st.session_state.stage['status'] = "confirmation"

        ##! confirmation of draft
        elif st.session_state.stage["current"] <= st.session_state.stage["max"] and st.session_state.stage["status"] == "confirmation":
            # Display user message in chat message container
            chatcontainer.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": f"{prompt}" })

            # Set up the prompt to llm
            section_list = json.loads(st.session_state.background[1]["content"])
            current_section = section_list[st.session_state.stage["current"] - 1]
            system_instructions = [{"role": "system", "content": f"You are currently drafting the requirements specifications for the {current_section} section. " + system_prompts.system_prompts["confirmation"]}]
            built_prompt = st.session_state.background + st.session_state.messages + [{"role" : "assistant", "content" : f"current draft: {st.session_state.current_draft}"}] + system_instructions
            print("built_prompt = ", built_prompt)
            response_json = llm.get_completion_by_messages(built_prompt)

            # Convert llm response in json back into python dictionary 
            response = json.loads(response_json)
            print("response = ", response)

            # Append llm reply to messages
            with chatcontainer.chat_message("assistant"):
                st.markdown(response["reply"])
            st.session_state.messages.append({"role": "assistant", "content": response["reply"]})

            # Update draft  
            st.session_state.current_draft = response["results"]

            # If user is satisfied, move to the next section to start drafting
            if response["next_step"] == "confirmed":
                st.session_state.stage["status"] = "draft"
                st.session_state.stage["current"] += 1
                st.session_state.sow.append({current_section : st.session_state.current_draft})

        else:
            print("skipped till here")

with col1:
    with st.container(height=500):
        # section_list = json.loads(st.session_state.background[1]["content"])
        # current_section = section_list[st.session_state.stage["current"] - 1]
        st.markdown(st.session_state.current_draft)        

with st.container(height=500):
    for section in st.session_state.sow:
        # st.markdown(section)
        st.markdown(f"*{section.keys()}*")
        st.markdown(section.values())


with st.container(height=500):
    st.session_state

