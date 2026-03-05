from pathlib import Path

import pandas as pd
import psycopg
import streamlit as st

from utils import Challenges, Languages, db_connection_string, insert_row, update_row


@st.cache_data(ttl=30)
def load_submissions():
    with psycopg.connect(db_connection_string) as conn:
        return pd.read_sql("SELECT * FROM submissions", conn)


st.set_page_config(
    page_title="Programming Challenges"  # , layout="wide"
)

st.title('Programming challenges')

df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
})

challenge = st.selectbox(
    'Select a challenge',
    [x.value for x in Challenges])

st.header("Task description")
if challenge == Challenges.CHALLENGE_1:
    st.markdown("""
             The CECAD animal facility is keeping a population of naked mole rats. After they are born, they take 1 month to become mature.
             Once mature, they reproduce - each mature naked mole rat produces one offspring per month. Since they never die,
             they quickly accumulate at large quantities in the animal facility. \n
        At **month 1**, the population starts with **2** mature individual. \n
        At **month 2**, there are 2 offsprings (produced by the mature individuals from the last month) + 2 mature individuals = **4** naked mole rats in total.\n
        At **month 3**, there are 2 offsprings + 4 mature individuals = **6** naked mole rats in total.\n       
        Etc. \n        
        Given *n = number of months*, how many naked mole rats will be living at the CECAD animal facility?
""")

    st.image("./images/naked_mole_rat.png", width=400)

    st.subheader('Example input:')
    st.code('{"n": 4}', language="json")
    st.subheader('Example solution:')
    st.code('{"result": 10}', language="json")

    with open("challenge_1.zip", "rb") as file:
        st.download_button(
            label="Download challenge starter pack",
            data=file,
            file_name="challenge_1.zip")

elif challenge == Challenges.CHALLENGE_2:
    st.write("Coffee!")

st.header("Submit a solution")

name = st.text_input("Your name:")
uploaded_file = st.file_uploader('Upload a solution')

clicked_submit = st.button("Submit")

if clicked_submit:
    is_valid_submission = True
    language = None
    if uploaded_file is None:
        is_valid_submission = False
        st.badge("Please select a file (.py or .R script)", color="red")
    else:
        if not name:
            is_valid_submission = False
            st.badge("Please provide your name.", color="red")
        file_suffix = Path(uploaded_file.name).suffix.lower()
        if file_suffix == '.py':
            language = Languages.PYTHON.value
        elif file_suffix == '.r':
            language = Languages.R.value
        else:
            is_valid_submission = False
            st.badge("Please submit either .py or .R script.", color="red")
        if is_valid_submission:
            print(f"{language=}")
            submission_data = {'challenge_id': Challenges(challenge).name,
                               'name': name,
                               'language': language}
            with psycopg.connect(db_connection_string) as conn:
                submission_id = insert_row(conn, submission_data)
                print(f"submission_id=")

            output_folder = Path(f'./submissions/{submission_id}')
            output_folder.mkdir(parents=True, exist_ok=True)
            file_name = 'script.py' if language == Languages.PYTHON.value else 'script.R'

            with open(output_folder / file_name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with psycopg.connect(db_connection_string) as conn:
                update_row(conn, submission_id, {"status": "waiting"})

            st.success(f"File uploaded: {uploaded_file.name}")
            load_submissions.clear()

st.header("Leaderboard")
clicked_refresh = st.button("\U0001F504 Refresh")
if clicked_refresh:
    load_submissions.clear()

df = load_submissions()

mock_results = pd.DataFrame(data={'Time': [1, 2, 3],
                                  'Name': ['Jakub', 'Lara', 'Pavel']})
st.dataframe(df)

st.subheader("All sumbissions")
st.dataframe(df)
