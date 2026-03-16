# eval-server
Evaluation server for coding challenges.

## Setup
* Database: ```docker compose up -d```
* App: ```streamlit run app.py --server.address 0.0.0.0 --server.port 8501```
* Evaluation worker: ```python eval_worker.py```