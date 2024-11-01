import streamlit as st  
import json
from helper_functions.utility import check_password  
from helper_functions import llm 
from helper_functions import system_prompts

st.title("Specs Agent")

# Check if the password is correct.  
if not check_password():  
    st.stop()

tab1, tab2 = st.tabs([":pencil2: **Draft**", ":white_check_mark: Finalised"])

with tab1:
    # Initialize assistant
    if "background" not in st.session_state:
        st.session_state.background = [
            {"role": "system", "content": system_prompts.system_prompts["background"]},
            {"role": "system", "content" : "["",""]"}
        ]

    if "stage" not in st.session_state:
        st.session_state.stage = {"max": 0, "current": 0, "status": "setup", "chat_disabled" : False}

    if "current_draft" not in st.session_state:
        st.session_state.current_draft = ""

    if "sow" not in st.session_state:
        st.session_state.sow = []

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hi. What would you like to procure today?"}
        ]

    with st.container(height=75):
        progress_status = {
            "setup" : 0,
            "setup_confirmation" : 0,
            "completed": 100,
            "draft": st.session_state.stage["current"] / (st.session_state.stage["max"] + 1),
            "confirmation": st.session_state.stage["current"] / (st.session_state.stage["max"] + 1)
        }
        st.progress(progress_status[st.session_state.stage["status"]], "## :hourglass: Your Progress: :hourglass:")

    col1, col2 = st.columns([2,1])

    with col2:
        st.markdown("##### Agent")
        chatcontainer = st.container(height=400)
        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with chatcontainer.chat_message(message["role"]):
                st.markdown(message["content"])

        # React to user input
        if prompt := st.chat_input("What is up?", disabled=st.session_state.stage["chat_disabled"]):
            # Display user message in chat message container
            chatcontainer.chat_message("user").markdown(prompt)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": f"{prompt}" })

            if st.session_state.stage["current"] <= st.session_state.stage["max"]:

                ##! first engagement with llm to set up the main headers of the scope of work !##
                if st.session_state.stage["status"] == "setup":
                    ## print("setup")
                    # Set up the prompt to llm
                    system_instructions = [{"role": "system", "content": system_prompts.system_prompts["setup"]}]
                    built_prompt = [st.session_state.background[0]] + st.session_state.messages + system_instructions
                    response_json = llm.get_completion_by_messages(built_prompt)
                    
                    # Convert llm response in json back into python dictionary
                    response = json.loads(response_json)

                    # Update system info with user reqt
                    st.session_state.background[1]["content"] = json.dumps(response["results"])
                    st.session_state.stage["max"] = len(response["results"])
                    with chatcontainer.chat_message("assistant"):
                        st.markdown(response["reply"])
                    st.session_state.messages.append({"role": "assistant", "content": response["reply"]})
                    st.session_state.stage["status"] = response["next_step"]
                    
                ##! check if user is agreeable with llm suggestions for the main headers !##
                elif st.session_state.stage["status"] == "setup_confirmation":
                    ## print("setup confirmation")
                    user_prompt = [{"role" : "user", "content" : prompt}]
                    system_instructions = [{"role": "system", "content": system_prompts.system_prompts["confirmation"]}, {"role" : "assistant" , "content": st.session_state["background"][1]["content"]}]
                    prompt_for_decision = system_instructions + user_prompt
                    decision_json = llm.get_completion_by_messages(prompt_for_decision)
                    decision = json.loads(decision_json)
                    proceed_decision = decision["proceed"] #retrieve proceed decision
                    ## print("proceed_decision =", proceed_decision)

                    #* if user is agreeable with the main headers *#
                    if proceed_decision == "True":
                        ## print("setup confirmation true")
                        response_json = llm.get_completion_by_messages([{"role" : "system", "content" : system_prompts.system_prompts["proceed"]}])
                        response = json.loads(response_json)
                        ## print("setup confirmation reply: ", response)
                        
                        # Append llm reply to the chat messages
                        with chatcontainer.chat_message("assistant"):
                            st.markdown(response["reply"])
                        st.session_state.messages.append({"role": "assistant", "content": response["reply"]})

                        # Update stage and status
                        st.session_state.stage["status"] = "draft"
                        st.session_state.stage["current"] += 1
                    
                    #* if user is NOT agreeable with the main headers *#
                    else:
                        ## print("setup confirmation false")
                        system_instructions = [{"role": "system", "content": system_prompts.system_prompts["setup_amendment"]}]
                        built_prompt = st.session_state.background + st.session_state.messages + system_instructions
                        response_json = llm.get_completion_by_messages(built_prompt) 
                        response = json.loads(response_json)
                        ## print("setup amendment reply: ", response)

                        # Update system info with user reqt
                        st.session_state.background[1]["content"] = json.dumps(response["results"])
                        st.session_state.stage["max"] = len(response["results"])
                        with chatcontainer.chat_message("assistant"):
                            st.markdown(response["reply"])
                        st.session_state.messages.append({"role": "assistant", "content": response["reply"]})
                        st.session_state.stage["status"] = response["next_step"]

                ##! initial drafting of each section !##  
                elif st.session_state.stage["status"] == "draft":
                    section_list = json.loads(st.session_state.background[1]["content"])
                    current_section = section_list[st.session_state.stage["current"] - 1] #get current section header
                    system_instructions = [{"role": "system", "content": f"You are currently drafting the requirements specifications for the {current_section} section. " + system_prompts.system_prompts["draft"]}]
                    built_prompt = st.session_state.background + st.session_state.messages + system_instructions
                    response_json = llm.get_completion_by_messages(built_prompt) 
                    response = json.loads(response_json)

                    # Append llm reply to messages
                    with chatcontainer.chat_message("assistant"):
                        st.markdown(response["reply"])
                    st.session_state.messages.append({"role": "assistant", "content": response["reply"]})

                    # Update draft to session state for display in the draft section
                    st.session_state.current_draft = response["results"]

                    # Change status to confirmation
                    st.session_state.stage['status'] = response["next_step"]

                ##! confirmation of drafting of each section !##
                elif st.session_state.stage["status"] == "confirmation":
                    ## print("setup confirmation")
                    user_prompt = [{"role" : "user", "content" : prompt}]
                    system_instructions = [{"role": "system", "content": system_prompts.system_prompts["confirmation"]},{"role" : "assistant", "content" : st.session_state["current_draft"]}]
                    prompt_for_decision = system_instructions + user_prompt
                    decision_json = llm.get_completion_by_messages(prompt_for_decision)
                    decision = json.loads(decision_json)
                    proceed_decision = decision["proceed"] #retrieve proceed decision
                    ## print("proceed_decision =", proceed_decision)

                    #* if user is agreeable with the current draft of the section *#
                    if proceed_decision == "True":
                        response_json = llm.get_completion_by_messages([{"role" : "system", "content" : system_prompts.system_prompts["proceed"]}])
                        response = json.loads(response_json)
                        
                        # Append llm reply to the chat messages
                        with chatcontainer.chat_message("assistant"):
                            st.markdown(response["reply"])
                        st.session_state.messages.append({"role": "assistant", "content": response["reply"]})

                        # Update SOW with the confirmed draft
                        st.session_state.sow.append(st.session_state.current_draft)
                        st.session_state.current_draft = ""

                        # Update stage and status
                        st.session_state.stage["status"] = "draft"
                        st.session_state.stage["current"] += 1

                        # Disable chat if the job is completed
                        if st.session_state.stage["current"] > st.session_state.stage["max"]:
                            st.session_state.stage["chat_disabled"] = True


                    #* if user is NOT agreeable with the current draft of the section *#
                    else:
                        section_list = json.loads(st.session_state.background[1]["content"])
                        current_section = section_list[st.session_state.stage["current"] - 1]
                        system_instructions = [{"role": "system", "content": f"You are currently amending the requirements specifications for the {current_section} section. The current draft in demarcated by the tag <draft></draft> below. <draft>{st.session_state.current_draft}</draft> " + system_prompts.system_prompts["draft_amendment"]}]
                        built_prompt = st.session_state.background + st.session_state.messages + system_instructions
                        response_json = llm.get_completion_by_messages(built_prompt)
                        response = json.loads(response_json)

                        # Append llm reply to messages
                        with chatcontainer.chat_message("assistant"):
                            st.markdown(response["reply"])
                        st.session_state.messages.append({"role": "assistant", "content": response["reply"]})

                        # Update draft to session state for display in the draft section
                        st.session_state.current_draft = response["results"]

                        # Change status to confirmation
                        st.session_state.stage['status'] = response["next_step"]

                else: 
                    st.session_state.messages.append({"role": "assistant", "content": system_prompts.system_prompts["error"]})

            else:
                # print("end")
                st.session_state.stage["status"] = "completed"
                system_instructions = [{"role": "system", "content": system_prompts.system_prompts["completed"]}]
                built_prompt = st.session_state.messages + system_instructions
                response = llm.get_completion_by_messages(built_prompt)

                with chatcontainer.chat_message("assistant"):
                    st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    with col1:
        st.markdown("##### Current Draft")
        with st.container(height=450):
            st.markdown(st.session_state.current_draft)        

    with st.expander("Disclaimer"):
        st.write("""
            IMPORTANT NOTICE: This web application is developed as a proof-of-concept prototype. The information provided here is NOT intended for actual usage and should not be relied upon for making any decisions, especially those related to financial, legal, or healthcare matters.

            Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. You assume full responsibility for how you use any generated output.

            Always consult with qualified professionals for accurate and personalized advice.

            """)


    # with st.container(height=500):
    #     st.session_state

with tab2: 
    st.markdown("### Requirements Specification ")

    with st.expander("Important Notice"):
        st.write("""
            The Requirements Specifications drafted by the agent is not based on training data of specifications drafted by any agencies within WOG. Use the Requirements Specifications with care. Officers are reminded to check for accuracy of the contents to ensure they meet the user's requirements, and are aligned with the principles of Government Procurement.
            """)

    with st.container(height=500):
        for section in st.session_state.sow:
            st.markdown(section)
        