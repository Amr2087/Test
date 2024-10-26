import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage
from datetime import datetime
import os

st.title("GROQ LLaMA Chatbot")

os.environ["GROQ_API_KEY"] = st.secrets["my_cool_secrets"]["GROQ_API_KEY"][0]


model = ChatGroq(model="llama3-8b-8192",)


if "msgs" not in st.session_state:
    st.session_state.msgs = []

placeholder = "Type your message here..."
prompt = "You are a helpful assistant."



for message in st.session_state.msgs:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if query := st.chat_input(placeholder):

    st.session_state.msgs.append({"role": "user", "content": query})


    with st.chat_message("user"):
        st.markdown(query)

    full_messages = [
                        {"role": "system", "content": prompt},
                    ] + [{"role": m["role"], "content": m["content"]} for m in st.session_state.msgs]


    with st.chat_message("assistant"):

        messages_for_groq = [
            HumanMessage(content=msg["content"]) if msg["role"] == "user"
            else AIMessage(content=msg["content"]) for msg in full_messages
        ]


        response = model.invoke(messages_for_groq)


        st.markdown(response.content)


    st.session_state.msgs.append({"role": "assistant", "content": response.content})

