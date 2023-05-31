# app/Dockerfile

FROM python:3.10

WORKDIR .

COPY ./requirements.txt ./requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "dashboard.py", "--server.port=8080", "--server.address=0.0.0.0", "--server.headless", "true", "--server.fileWatcherType", "none", "--browser.gatherUsageStats", "false"]