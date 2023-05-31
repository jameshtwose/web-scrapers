## Job Scrape Dashboard
This is a dashboard for the job scrape project. It is built using [Streamlit](https://www.streamlit.io/).

### Build instructions (python) 
- Install [Python](https://www.python.org/downloads/)
- `cd job_scrape`
- `pip install -r requirements.txt`
- `streamlit run dashboard.py`

### Build instructions (docker)
- Install [Docker](https://docs.docker.com/install/)
- `docker compose --env-file=./.env build`
- `docker run -d -p 8501:8501 freelance-nl-i`