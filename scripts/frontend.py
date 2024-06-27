import streamlit as st
import time

st.title("Welcome to the OER Assistant")

with st.chat_message("assistant"):
    st.write("Hello 👋 I'm Reo. I'm here to help you browse OER content. You can use voice or text.")

query = st.chat_input("How can I help you today?", key="query")

if query:
    with st.chat_message("user"):
      st.write(query)
    with st.status("Working on it..."):
      st.write("Searching for data...")
      time.sleep(2)
      st.write("Found data!")
      time.sleep(1)
    with st.chat_message("assistant"):
      st.write("Marvelous Magnets: Exploring the Power and Attraction of Magnets")
      st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum non lobortis nisl. In venenatis finibus mauris, et pellentesque nunc egestas id. Integer hendrerit egestas maximus. Ut sed elementum velit. Aenean pulvinar nisl vitae pellentesque condimentum. Donec nec iaculis magna. Donec ornare nisl sed justo euismod, in sagittis quam efficitur.")
      st.button("Play Audio")

