# useful commands/ links to deploy
# https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/getting_started#adding-credentials
# terraform init
# terraform plan
# terraform apply
# terraform destroy

# creating an instance to deploy the app
terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  credentials = file(var.credentials_file)
  project     = var.project
  region      = var.region
  zone        = var.zone
}

resource "google_app_engine_application" "app" {
  project     = var.project
  location_id = "europe-west"
}

