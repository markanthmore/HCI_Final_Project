import streamlit as st
import requests
import pandas as pd  

@st.cache_data  # Saves the data on one API call
def fetch_category_data():
    url_categories = "https://opentdb.com/api_category.php"
    url_numQuestions = "https://opentdb.com/api_count.php"
    
    # Collects categories
    category_response = requests.get(url_categories)
    category_response.raise_for_status()
    categories_data = category_response.json().get("trivia_categories", [])

    category_counts = []
    
    # Collects question counts for each category
    for category in categories_data:
        # Ensure category is a dictionary
        if isinstance(category, dict) and "id" in category and "name" in category:
            category_id = int(category["id"])  # Ensure category ID is an integer

            # Clean the category name at the colon to show only category name
            category_name = category["name"].split(":")[-1].strip()

            # Fetch question count for this category
            question_count_url = f"{url_numQuestions}?category={category_id}"
            question_count_response = requests.get(question_count_url)
            question_count_response.raise_for_status()
            question_count_data = question_count_response.json()

            # Extract total question count
            total_questions = question_count_data.get("category_question_count", {}).get("total_question_count", 0)

            # Append to results
            category_counts.append({"Category Name": category_name, "Total Number of Questions": total_questions})
    
    return category_counts

def api_info_link():
    # TODO Niel was here adding the condition to display the graph with a checkmark
    st.sidebar.title("Get the questions") 
    try:
        # Fetch the category data (cached version)
        category_counts = fetch_category_data()

        # Create a DataFrame from category_counts
        df = pd.DataFrame(category_counts)

        # Display data and bar chart
        st.write("Total Questions per Category")
        st.bar_chart(data=df, x="Category Name", y="Total Number of Questions", use_container_width=True)

    except requests.exceptions.RequestException as e:
        st.write(f"Error fetching data: {e}")

