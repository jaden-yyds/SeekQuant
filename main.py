import streamlit as st
from chatbot import async_send_message

st.set_page_config(page_title="💬 SeekQuant")

def main():
    question = st.chat_input("Say something")
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            st.write_stream(async_send_message(question))

if __name__ == "__main__":
    main()