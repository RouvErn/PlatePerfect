# Build Docker image locally
docker-build:
    docker build --platform linux/amd64 -t  $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT)/plateperfect/$(GAR_IMAGE):prod .

# Create Google Artifact Registry
create-artifact-repo:
    gcloud artifacts repositories create plateperfect --repository-format=docker \
    --location=$(GCP_REGION) --description="Repository for storing plateperfect images"

# Push Docker image to Google Artifact Registry
docker-push:
    docker push $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT)/plateperfect/$(GAR_IMAGE):prod

# Deploy Docker image on Google Artifact Registry onto Google Cloud Run
deploy-cloud-run:
    gcloud run deploy --image $(GCP_REGION)-docker.pkg.dev/$(GCP_PROJECT)/plateperfect/$(GAR_IMAGE):prod \
    --memory $(GAR_MEMORY) --region $(GCP_REGION)

# Run Streamlit app
run-streamlit:
    streamlit run PlatePerfect/app.py
