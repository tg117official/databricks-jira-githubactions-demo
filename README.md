# Databricks CI/CD Demo with GitHub Actions and JIRA

## JIRA mapping
- PIPE-1 Create a pipeline
- PIPE-2 Create source to bronze
- PIPE-3 Create bronze to silver by adding DQ rules

## Flow
- `develop` branch -> deploys to `dev`
- `main` branch -> deploys to `uat`
- `release-*` tag -> deploys to `preprod`, then `prod`

## Local test
```bash
pip install -r requirements-dev.txt
pytest -q