# Model Router

Organized repo for experimenting with Azure OpenAI Model Router.

## Structure

- app/
  - gradio_app.py — Gradio chat UI that shows the routed model while streaming
- examples/
  - foundry_sample.py — Simple script calling the router
  - prompts/ — Prompt sets to exercise different routes
- notebooks/
  - model-router.ipynb — Notebook walkthrough and examples
- env.sample — Copy to .env and set azure_openai_endpoint
- .gitignore — Keeps .env and .venv out of git

## Quickstart

1) Create your .env

Copy env.sample to .env and set:

azure_openai_endpoint="https://YOUR-RESOURCE.openai.azure.com/"

2) Install deps

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

3) Run the Gradio app

python app/gradio_app.py

4) Or run the sample script

python examples/foundry_sample.py

Notes
- Auth uses DefaultAzureCredential + Entra ID. Ensure you can obtain a token for https://cognitiveservices.azure.com/.default
- API version pinned to 2025-01-01-preview in samples
