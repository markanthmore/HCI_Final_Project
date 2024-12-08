import streamlit as st
import requests
from PIL import Image

def game_settings():
    st.title("Welcome to Trivia Time!")
    st.write("To test your knowledge, start by adjusting settings in the sidebar.")

    st.sidebar.title("Game Settings")

    st.sidebar.divider()

    player_name = st.sidebar.text_input("Input Player Name", placeholder="Player Name")
    if player_name:
        st.sidebar.write("**Player Name:**", player_name)

    image = st.sidebar.file_uploader("Upload Player Avatar", type=["jpg", "jpeg", "png"])

    if image:
        player_avatar = Image.open(image)
       
        if player_avatar.size[0] <= 500 and player_avatar.size[1] <= 500: 
            st.sidebar.image(player_avatar, caption="Uploaded Image", use_column_width=True)
            st.session_state.player_avatar = player_avatar
        else:
            st.sidebar.warning("Image dimensions must be at least 500x500.")

    st.sidebar.divider()

    proceed = st.sidebar.button("Proceed to Question Settings")

    st.sidebar.divider()

    if proceed:
        if not player_name:
            st.sidebar.error("Player Name cannot be empty.")
        else:

            st.session_state.player_name = player_name
            st.session_state.step = "question_settings"

    return player_name
