# PlatePerfect
Calorie traking made easy - Food Image Recognition

Format of link to use the Google Cloud Run Container:
# https://plateperfect-qo3jjoz2na-ew.a.run.app/predict?image_paths=https://www.handelshof.de/fileadmin/user_upload/Verschiedene_Sushi_Varianten.jpg&serving_size_grams=450
- the image link/path has to be publicly available (local links/paths of images won't work)

Docker & Google Cloud
CLI command to build docker image locally:
# docker build --platform linux/amd64 -t  $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/plateperfect/$GAR_IMAGE:prod .

CLI command to create Google Artifact Registry:
# gcloud artifacts repositories create plateperfect --repository-format=docker \                                  [🐍 PlatePerfect]
# --location=$GCP_REGION --description="Repository for storing plateperfect images"

CLI command to push docker image to Google Artifact Registry:
# docker push $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/plateperfect/$GAR_IMAGE:prod

CLI command to deploy docker image on Google Artifact Registry onto Google Cloud Run (making it available to the public):
# gcloud run deploy --image $GCP_REGION-docker.pkg.dev/$GCP_PROJECT/plateperfect/$GAR_IMAGE:prod --memory $GAR_MEMORY --region $GCP_REGION

After usage of Google Cloud Run - delete otherwise cost will occur (can't pause)

Streamlit
CLI command to run:
# streamlit run PlatePerfect/app.py
