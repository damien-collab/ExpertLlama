import os
import openai
import streamlit as st
import threading
import time
import random

# Import ChatBot class from chat
from chat import ChatBot

# Set API keys
openai.api_key = st.text_input("OpenAI API Key", value=os.getenv("OPENAI_API_KEY"), type="password")
os.environ['GROQ_API_KEY'] = st.text_input("GROQ API Key", value=os.getenv("GROQ_API_KEY"), type="password")


def stream_data(text_data, df_data):

    if text_data:
        for word in text_data.split(" "):
            yield word + " "
            time.sleep(0.02)

    if df_data:
        st.dataframe(df_data)




system_prompt = """
You are my expert assistant (and my bro) that is highly intelligent and applies first principle thinking with a positive and efficient mindset. We talk informally and you are very knowledgeable about every topic, and critical but helpful in my ideas.
Use your expertise in well-written intellectual responses (with optionally a little bit of witty humor or an analogy, if that helps in the response and is appropriate).
If you are not familiar with the topic or need additional info, just say it! Keep your responses very short and very concise.
"""

chatbot = ChatBot("GROQ_API_KEY", "llama3-8b-8192", max_tokens=1024, system_prompt=system_prompt)

def main():
    st.title("Chat")

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    user_input = st.chat_input("Enter your message:", key="chat_input")
    if user_input:
        user_message = {"role": "user", "content": user_input}
        st.session_state.messages.append(user_message)

        # Fetch and display assistant's response
        with st.spinner('Thinking.. 💭'):
            response = chatbot.chat(user_input)
            assistant_message = {"role": "assistant", "content": response}
            st.session_state.messages.append(assistant_message)

    # Display previous messages in an expander
    last_user_msg_index = None
    for i, message in enumerate(st.session_state.messages):
        if message["role"] == "user":
            last_user_msg_index = i

    if last_user_msg_index is not None and last_user_msg_index > 0:
        with st.expander("See Previous Messages"):
            for message in st.session_state.messages[:last_user_msg_index]:
                st.markdown(f"**{message['role']}**: {message['content']}")

    # Display the latest user message and all following assistant messages
    if last_user_msg_index is not None:
        for message in st.session_state.messages[last_user_msg_index:]:
            st.markdown(f"**{message['role']}**: {message['content']}")
            # st.markdown(stream_data(message['content'], None))

if __name__ == "__main__":
    main()