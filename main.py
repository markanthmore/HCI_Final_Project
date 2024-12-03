import streamlit as st
from game_settings import game_settings
from question_settings import question_settings
from api_info_link import  api_info_link

if "step" not in st.session_state:
    st.session_state.step = "game_settings"

if st.session_state.step == "game_settings":
    game_settings()

if st.session_state.step == "question_settings":
    question_settings()

api_info_link()