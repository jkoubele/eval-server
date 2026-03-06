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

    # st.subheader('Example input:')
    # st.code('{"n": 4}', language="json")
    # st.subheader('Example solution:')
    # st.code('{"result": 10}', language="json")

    st.subheader('Starter pack')
    st.markdown('Download a starter pack with script templates and test inputs.')
    with open("./starter_packs/challenge_1.zip", "rb") as file:
        st.download_button(
            label="Download challenge starter pack",
            data=file,
            file_name="challenge_1.zip")

elif challenge == Challenges.CHALLENGE_2:
    st.write("Coffee!")

st.header("Submit a solution")
st.markdown('Upload R or Python script with your solution, following the template from the starter pack.')

name = st.text_input("Your name:")
uploaded_file = st.file_uploader('Upload a solution')

clicked_submit = st.button("Submit", type="primary")

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
            
st.header("Evaluation")

st.markdown("""
            Your script will be automatically evaluated by running it and comparing its output versus a reference solution.
            * The following docker images are used to execute the code: ```quay.io/jupyter/r-notebook``` for R scripts and 
            ```quay.io/jupyter/scipy-notebook``` for Python script. These images should contain most of the standard scientific tools
            (tidyverse for R, pandas/numpy/scipy for Python). Additionally, packages *gmp* (for representing large integers) and 
            *jsonlite, rjson, argparse* (for CLI and JSON parsing) were installed into the R image.
            * Installing other packages during the runtime is not allowed.
            * The script should produce JSON file *output.json* according to the template.
            * The *output.json* is compared against reference solution. The result can be either a number or a string (both options are accepted).
            * Scripts running for more than 60s during the evaluation are timed out.
            """)

st.header("Leaderboard")
clicked_refresh = st.button("\U0001F504 Refresh")
if clicked_refresh:
    load_submissions.clear()

df = load_submissions()

leaderboard = (
    df[df['challenge_id'] == Challenges(challenge).name]
    .query("correct == True")
    .sort_values("cpu_time")
    .drop_duplicates(subset="name", keep="first")
    [["name", "cpu_time", "language", "submission_time"]]
    .reset_index(drop=True)
)

leaderboard.insert(0, "Position", leaderboard.index + 1)
leaderboard["submission_time"] = pd.to_datetime(leaderboard["submission_time"]).dt.strftime("%Y-%m-%d %H:%M:%S")

st.dataframe(leaderboard, hide_index=True)

st.subheader("All sumbissions")

all_submissions = df[df['challenge_id'] == Challenges(challenge).name]
all_submissions = all_submissions.drop(columns=['challenge_id', 'metadata'])
all_submissions = all_submissions[
    ['id', 'name', 'submission_time', 'status', 'cpu_time', 'language', 'produced_output', 'correct', 'timed_out']]
all_submissions = all_submissions.sort_values("id", ascending=False)
st.dataframe(all_submissions, hide_index=True)
