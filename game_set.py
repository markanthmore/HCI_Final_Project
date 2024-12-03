import streamlit as st
def game_settings():
    st.title("Welcome to Trivia Time!")
    st.write("To test your knowledge, start by adjusting settings in the sidebar.")

    st.sidebar.title("Game Settings")

    st.sidebar.divider()

    player_name = st.sidebar.text_input("Input Player Name",placeholder="Player Name")
    if player_name:
        st.sidebar.write("**Player Name:**",player_name)
    
    round_count = st.sidebar.selectbox("Select round count",("","1","2","3","4","5"))
    round_count = int(round_count) if round_count else None
    if round_count:
        st.sidebar.write("**Round Count:**",round_count)

    st.sidebar.divider()

    proceed = st.sidebar.button("Proceed to Question Settings")

    if proceed:
      if not player_name:
          st.sidebar.error("Player Name cannot be empty.")
      elif not round_count:
          st.sidebar.error("Round Count must be selected.")
          st.session_state.round_count = round_count
      else:
          st.session_state.player_name = player_name
          st.session_state.step = "question_settings"

    return player_name, round_count


def api_info_link():
    st.sidebar.divider()
    st.sidebar.title("Interested in Learning about our API?")
    proceed = st.sidebar.checkbox("# Questions per Category")

    if proceed:

        
        st.sidebar.link_button("Check API Page", "https://opentdb.com")
        




