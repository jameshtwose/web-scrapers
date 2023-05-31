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

### Build instructions (terraform-gcp)
- Install [Terraform](https://www.terraform.io/downloads.html)
- Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)
- `cd terraform_gcp_deploy`
- get credentials .json file from GCP if you don't have it already
  - https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started#adding-credentials
  - https://cloud.google.com/docs/authentication/getting-started
- put credentials .json file in `terraform_gcp_deploy` folder
- `terraform init`
- `terraform plan`
- `terraform fmt`
- `terraform apply`
- `gcloud init` (if you haven't already)
- `gcloud app deploy`
- `terraform destroy` (when you're done)