import streamlit as st
import time

col1, col2, col3 = st.columns([10, 1, 1], vertical_alignment="center")


with col1:
   st.image('images/logo.png')

with col2:
   st.image('images/flag-icon.png')

with col3:
   st.image('images/alpha-icon.png')

with st.chat_message("assistant"):
    with st.container(height=200):
      st.header("Hello 👋 I'm Reo. I'm your tutoring buddy. You can use voice or text.")

left, right = st.columns([1, 11], vertical_alignment="center")

with left:
    st.image('images/mic-icon.png')

with right:
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

