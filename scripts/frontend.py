import streamlit as st
import time
import asyncio

from chat import create_chatcontroller

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

@st.cache_resource()
def first_run():
  controller, _ = loop.run_until_complete(create_chatcontroller())
  return controller

controller = first_run()

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def swipe_up():
    if not st.session_state.clicked:
      st.session_state.clicked = True
    else:
      st.session_state.clicked = False

def clear_chat():
    controller.History = []

col1, col2, col3, col4 = st.columns([10, 1, 1, 1], vertical_alignment="center")

with col1:
   st.image('images/logo.png')

with col2:
   st.image('images/flag-icon.png')

with col3:
   st.image('images/alpha-icon.png')
with col4:
   st.button("\+", on_click=clear_chat)

with st.chat_message("assistant"):
    with st.container(height=200):
      st.header("Hello 👋 I'm Reo. I'm your tutoring buddy. You can use voice or text.")

left, center, right = st.columns([5, 3, 5], vertical_alignment="center")

with center: 
  icon = st.image('images/mic-icon.png')

with center: 
  st.button("Swipe up to type", on_click=swipe_up)
  # st.write("Swipe up to type")

# query = st.chat_input("How can I help you today?", key="query")

if st.session_state.clicked:
  query = st.chat_input("How can I help you today?", key="query")

  if query:
    with st.chat_message("user"):
      st.write(query)
    with st.status("Working on it..."):
      st.write("Searching for data...")
      inmsg, outmsg = loop.run_until_complete(controller.achat(query))
      st.write("Found data!")
      time.sleep(1)
    with st.chat_message("assistant"):
      st.write(outmsg.Message)
      # st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum non lobortis nisl. In venenatis finibus mauris, et pellentesque nunc egestas id. Integer hendrerit egestas maximus. Ut sed elementum velit. Aenean pulvinar nisl vitae pellentesque condimentum. Donec nec iaculis magna. Donec ornare nisl sed justo euismod, in sagittis quam efficitur.")
  
# if query:
#   with st.chat_message("user"):
#     st.write(query)
#   with st.status("Working on it..."):
#     st.write("Searching for data...")
#     loop = st.session_state["loop"]
#     inmsg, outmsg = loop.run_until_complete(controller.achat(query))
#     st.write("Found data!")
#     time.sleep(1)
#   with st.chat_message("assistant"):
#     st.write(outmsg.Message)
    # st.write("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum non lobortis nisl. In venenatis finibus mauris, et pellentesque nunc egestas id. Integer hendrerit egestas maximus. Ut sed elementum velit. Aenean pulvinar nisl vitae pellentesque condimentum. Donec nec iaculis magna. Donec ornare nisl sed justo euismod, in sagittis quam efficitur.")



