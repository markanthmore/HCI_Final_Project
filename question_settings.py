import streamlit as st
import requests
import random
import json
from game_settings import game_settings

#TRIVIA QUESTION FETCH FUNCTION
def fetch_questions(amount=5, category=None, difficulty=None, q_type=None):
    url = "https://opentdb.com/api.php"
    params = {
        "amount": amount,
        "category": category,
        "difficulty": difficulty,
        "type": q_type,
    }
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["response_code"] == 0:
            return data["results"]
        else:
            st.error("No questions available for the selected options.")
    else:
        st.error("Failed to fetch data from the API.")
    return []

#QUESTION SETTINGS FUNCTION
def question_settings():
  #ROUND COUNT CHECK
  if "round_count" not in st.session_state:
        st.error("Round count is not set. Please go back to Game Settings.")
        if st.button("Back to Game Settings"):
            st.session_state.step = "game_settings"
        return
  #ROUND COUNT DECLARATION
  round_count = st.session_state.round_count
  
  #ROUND LOOP
  for i in range(1, round_count):
    #SIDEBAR TITLE
    st.sidebar.title(f"Round {i}")
    st.sidebar.divider()
    st.sidebar.header("Adjust Question Settings")

    #QUESTION SLIDER
    amount = st.sidebar.slider("Number of Questions", 1,20,key=f"slider_round_{i}")

    #CATEGORY LOAD
    with open("categories.json", "r") as f:
        data = json.load(f)

    categories = [item["name"] for item in data["categories"]]
    category = st.sidebar.selectbox("Category", categories,key=f"select_cat_round_{i}")

    #SIDEBAR DIFFICULTY
    diff_mapping = { #LOGIC TO DISPLAY DIFFICULTIES UPPERCASE IN THE APP
        None: None,  
        "Easy": "easy",
        "Medium": "medium",
        "Hard": "hard"
    }
    display_difficulties = list(diff_mapping.keys())
    selected_display_difficulty = st.sidebar.selectbox("Difficulty", display_difficulties,key=f"select_diff_round_{i}")
    difficulty = diff_mapping[selected_display_difficulty]

    #QUESTION TYPE
    q_type_mapping = {
        None: None,
        "Multiple Choice": "multiple",
        "True/False": "boolean"
    }
    display_q_type = list(q_type_mapping.keys())
    selected_display_q_type = st.sidebar.selectbox("Question Type",display_q_type,key=f"select_q_type_round_{i}")
    q_type = q_type_mapping[selected_display_q_type]
    st.sidebar.divider()

    #FETCH QUESTIONS BUTTON LOGIC
    if st.sidebar.button("Start!", key=f"button_round_{i}"):
      category_id = next((item["id"] for item in data["categories"] if item["name"] == category), None)

      questions = fetch_questions(amount, category_id, difficulty, q_type)

      if questions:
          st.subheader("Round Start!")
          st.divider()
          current_round_score = 0

          if f"answers_round_{i}" not in st.session_state:
              st.session_state[f"answers_round_{i}"] = {}

          for j, question in enumerate(questions, start=1):
              st.write(f"**Question {j}:** {question['question']}")
              options = question.get("incorrect_answers", []) + [question["correct_answer"]]
              random.shuffle(options)

              user_answer = st.radio(
                  f"Select an answer for Question {j}",
                  options,
                  key=f"round_{i}_question_{j}",
                  index=st.session_state[f"answers_round_{i}"].get(j)
              )
              st.session_state[f"answers_round_{i}"][j] = user_answer

          # Show all answers at the end
          # st.write("Your current answers:", st.session_state[f"answers_round_{i}"])
