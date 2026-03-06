import json
import shutil
import subprocess
from pathlib import Path
from time import sleep

import pandas as pd
import psycopg

from utils import Languages, db_connection_string, update_row

docker_image_python = "quay.io/jupyter/scipy-notebook:2026-03-02"
docker_image_r = "quay.io/jupyter/r-notebook:2026-03-02"

while True:
    with psycopg.connect(db_connection_string) as conn:
        df = pd.read_sql("SELECT * FROM submissions", conn)

    df = df[df["status"] == "waiting"].sort_values("submission_time")
    if len(df) == 0:
        sleep(3)
        continue

    if len(df) > 0:
        job_row = df.iloc[0]
        submission_folder = Path(f"./submissions/{job_row['id']}").resolve()

        script_name = 'script.py' if job_row['language'] == Languages.PYTHON.value else 'script.R'
        docker_image = docker_image_python if job_row['language'] == Languages.PYTHON.value else docker_image_r
        execute_command = 'python' if job_row['language'] == Languages.PYTHON.value else 'Rscript'

        eval_data_folder = Path(f"./eval_data/{job_row['challenge_id']}").resolve()
        shutil.copyfile(eval_data_folder / 'input.json', submission_folder / 'input.json')

        with open(eval_data_folder / 'solution.json') as f:
            reference_json = json.load(f)

        cmd = f"""
        docker run --rm --cpus=1 \
           --stop-timeout 1 \
          -v "{submission_folder}:/work" \
          -w /work \
          --user "$(id -u):$(id -g)" \
          --network none \
          --entrypoint bash {docker_image} \
          -c 'TIMEFORMAT="CPU %6U %6S"; {{ time {execute_command} {script_name} --input_json ./input.json --output_json ./output.json >/dev/null; }} 2>&1 | awk "/^CPU /{{print \\$2+\\$3}}"'
        """

        timed_out = False
        time_limit = 1
        cpu_time = None
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=time_limit,  # wall clock seconds
            )
        except subprocess.TimeoutExpired as e:
            timed_out = True
            print("Timed out")

        output_file = submission_folder / 'output.json'
        produced_output = output_file.exists()

        correct = False
        if produced_output:
            try:
                with open(output_file) as f:
                    output_json = json.load(f)
                correct = output_json.get("result") == reference_json.get("result") or str(
                    output_json.get("result")) == str(reference_json.get("result"))
            except Exception:
                correct = False

        if not timed_out:
            try:
                cpu_time = float(result.stdout.strip())
            except Exception:
                cpu_time = None
                print(f"CPU time undefined for submission ID P{job_row['id']}")

        with psycopg.connect(db_connection_string) as conn:
            update_row(conn, job_row['id'], {"status": "evaluated",
                                             "timed_out": timed_out,
                                             'produced_output': produced_output,
                                             'correct': correct,
                                             'cpu_time': cpu_time})
    sleep(3)
