import streamlit as st
import pickle
from langchain.llms import OpenAI
import os
import time
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferWindowMemory
# get a token: https://platform.openai.com/account/api-keys





def main():
        # Initialize chats
        if "currentChat" not in st.session_state:
            st.session_state.currentChat = []
            st.session_state.count = 0

            

            llm=OpenAI()

            prompt_template_name = PromptTemplate(
                input_variables =['input'],
                template = '''
                
                {input}

                '''
            )

            st.session_state.memory = ConversationBufferWindowMemory(input_key='input')

            st.session_state.chain = LLMChain(llm=llm, prompt=prompt_template_name, memory=st.session_state.memory)
            


        with st.sidebar:
            #Create a button to increment and display the number
            if st.button('Exit and start new interview'):
                st.session_state.currentChat = []
                st.session_state.count = 0
            
            st.write('Made with ❤️ by Ajeer')

        # st.title("Simple chat")
        # if st.button('New chat+'):
        #         st.session_state.chats.append([])
        # for chat in range(len(st.session_state.chats)):
        #     #button_key = f'button_{i}'
        #     if st.button(f'chat-{chat}'):
        #         st.write(chat)


        # Display chat messages from history on app rerun
        for message in st.session_state.currentChat:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        

        # Accept user input
        

        if prompt := st.chat_input("What is up?"):
            if st.session_state.count == 0:
                st.session_state.intro=prompt
            if st.session_state.count == 1:
                st.session_state.job=prompt
            st.session_state.count=st.session_state.count+1
            # Add user message to chat history
            st.session_state.currentChat.append({"role": "user", "content": prompt})
            # Display user message in chat message container
            with st.chat_message("user"):
                st.markdown(prompt)

            if st.session_state.count >= 2:
                # Display assistant response in chat message container
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    full_response = ""

                    

                    

                    # job= "hr manager"
                    # intro="my name i s aslam"
                    if st.session_state.count==2:
                        response = st.session_state.chain.run({"input":f"You are an interviewer for job role '{st.session_state.intro}'.This is the candiadate introduction '{st.session_state.job}'.Ask him next question as an interviewer"})
                    #response = st.session_state.chain({"input":prompt})
                    if st.session_state.count>2:
                        if st.session_state.count==6:
                            response = st.session_state.chain.run({"input":f"This is answer '{prompt}' for yout last questio.Now you can conlude interview give him a feed back based on the all previous messge in the interview"})
                        else:
                            response = st.session_state.chain.run({"input":f"This is answer '{prompt}' for yout last questio.This is  an interview so first give him a reply after Ask him next question as an interviewer"})
                    
                    assistant_response=response["text"]

                    

                    # Simulate stream of response with milliseconds delay
                    for chunk in assistant_response.split():
                        full_response += chunk + " "
                        time.sleep(0.05)
                        # Add a blinking cursor to simulate typing
                        message_placeholder.markdown(full_response + "▌")
                    message_placeholder.markdown(full_response)
                # Add assistant response to chat history
                st.session_state.currentChat.append({"role": "assistant", "content": full_response})

        if st.session_state.count == 0:
            st.session_state.currentChat.append({"role": "assistant", "content": "Hi, Please introduce yourself"})
            with st.chat_message("assistant"):
                st.markdown("Hi, Please introduce yourself")
    
        if st.session_state.count == 1:
            st.session_state.currentChat.append({"role": "assistant", "content": "What job role are you looking for?"})
            with st.chat_message("assistant"):
                st.markdown("What job role are you looking for?")
            
            
 
if __name__ == '__main__':
    os.environ["OPENAI_API_KEY"] =st.secrets['OPENAI_API_KEY']
    main()