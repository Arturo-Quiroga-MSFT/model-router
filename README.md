# Model Router (Azure AI Foundry)

This repo demonstrates the Azure AI Foundry model router: a single, deployable chat model that automatically selects the most suitable underlying model per request to balance quality, cost, and latency. You call one model name (for example, `model-router`) and the router picks the best target behind the scenes.

## What is the Azure model router?

- A composite chat model that routes each prompt to an underlying LLM based on factors like task complexity, reasoning needs, response length, modality (text vs. vision), latency targets, and budget.
- You get one endpoint and one deployment to manage, while still benefiting from multiple foundation models.
- Benefits:
  - Simpler integration (one model name)
  - Better cost control (small/fast models for easy tasks)
  - Consistent quality (larger or reasoning models when needed)
  - Future-ready (router can incorporate new models as they become available in your workspace)

## Which models can it route to?

The exact set depends on what’s enabled in your Azure AI Foundry project and region. Common examples include:

- GPT-4.1 series (e.g., GPT-4.1 2025-04-14)
- GPT-4.1-mini
- GPT-4.1-nano
- o4-mini

Your environment may also include other families (for example, “gpt-5-chat” or “gpt-5 reasoning”) if available. The included examples and prompts are written to exercise a mix of small/fast, general chat, high-capability, and deep-reasoning routes.

### Routed models (from Microsoft Docs)

According to Microsoft documentation, the router’s underlying models depend on the router version you deploy. Examples:

- model-router 2025-08-07
  - Underlying models: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, o4-mini, gpt-5, gpt-5-mini, gpt-5-nano, gpt-5-chat
  - Underlying model versions: 2025-04-14 (4.1 family), 2025-04-16 (o4-mini), 2025-08-07 (gpt-5 family)

- model-router 2025-05-19
  - Underlying models: gpt-4.1, gpt-4.1-mini, gpt-4.1-nano, o4-mini
  - Underlying model versions: 2025-04-14 (4.1 family), 2025-04-16 (o4-mini)

Source: Model router for Azure AI Foundry – Underlying models
https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-router#underlying-models

Notes
- Latest model-router versions that include gpt-5 family may be limited access. See the linked doc for access requirements and availability.
- Region availability varies; check the Models page for your region.
- Context window limits are constrained by the specific model selected at runtime. A larger prompt succeeds only if routed to a model that supports the larger window; otherwise the call may fail.

### Typical routing patterns (per Microsoft Docs)
- Simple tasks (short transforms, extraction, classification) → smaller/cheaper models (for example, o4-mini) to optimize latency and cost.
- Complex tasks (deep reasoning, long structured synthesis) → larger or reasoning-capable models (for example, GPT-4.1 series; gpt-5 reasoning/chat where available) to maintain quality.
- Vision inputs are accepted, but the routing decision is based on the text portion of the request. Models with vision capability may still be selected if indicated by the text and available in your environment.
- Context window caveat: large prompts succeed only if routed to a model that supports the larger context window; otherwise, the call can fail. Consider summarizing/truncating, or using retrieval to reduce prompt size.
- Latency/budget signals: when quality is sufficient, the router prefers smaller, faster models to reduce cost and response time.

Source: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-router#underlying-models

## When to use the model router (per Microsoft Docs)
- You want a single deployment/endpoint that automatically balances quality, cost, and latency across diverse prompts.
- Your workload has wide variability in complexity (some requests are simple, others require deeper reasoning or longer outputs).
- You want to default to smaller/cheaper models but “escalate” automatically for harder prompts.
- You’re okay with routing-driven variability (for example, context window depends on the selected underlying model).
- You plan to take advantage of model updates over time (note: enabling auto-update can change the underlying set and affect cost/performance).

Notes
- If you require a guaranteed underlying model or fixed context window, pin a specific model instead of using the router.
- Billing: today you’re billed for the underlying model usage. Per docs, router usage will also be billed starting September 1, 2025.
- Region/model availability varies by subscription and region; check the Models page for the latest.

Sources
- Model router overview and limitations: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/model-router
- Model availability: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/concepts/models

## Repo structure

- app/
  - gradio_app.py — Gradio chat UI that streams tokens and shows the “Model used” returned by the API
- examples/
  - foundry_sample.py — Minimal script that prints the routed model
  - prompts/ — Prompt sets designed to exercise different routing outcomes
- notebooks/
  - model-router.ipynb — Walkthrough notebook with examples and guidance
- env.sample — Copy to .env and set `azure_openai_endpoint`
- .gitignore — Keeps `.env` and `.venv` out of git

## Quickstart

1) Configure environment
   - Copy `env.sample` → `.env` and set:
     - `azure_openai_endpoint="https://YOUR-RESOURCE.openai.azure.com/"`

2) Install dependencies
   - Create/activate a virtual environment and install packages from `requirements.txt`.

3) Run the Gradio demo
   - `python app/gradio_app.py`
   - The header shows which underlying model the router selected while streaming.

### UI preview

![Gradio chat UI](./images/image.png)

![Gradio chat UI](./images/image-1.png)


Tips to capture:
- macOS screenshot: Shift+Cmd+4
- Quick GIF: QuickTime screen recording + convert to GIF (for example, via gifski or an online converter)

1) Or run the simple sample
   - `python examples/foundry_sample.py`
   - The script prints the assistant’s reply and the model that served it.

## Authentication and config
- Samples use Entra ID via `DefaultAzureCredential` and request a token for scope `https://cognitiveservices.azure.com/.default`.
- Ensure your identity has access to the Azure OpenAI resource behind `azure_openai_endpoint`.
- API version in samples: `2025-01-01-preview`.

## How to verify routing
- Gradio app: the “Model used” field updates during streaming using `chunk.model`.
- Script/notebook: prints `response.model` so you can see which model actually served the request.

## Notes
- Availability of specific routed models varies by region and subscription. Adjust prompts in `examples/prompts/` to steer routing (speed vs. depth, simple vs. complex, text-only vs. multimodal).
