# CloudOps AI Assistant — Setup Guide

This guide reflects the actual, working setup: an Azure AI Foundry Agent
(with a connected knowledge base) called from a local Streamlit app via the
Responses API.

## Architecture

```
Sample docs (.md)
      |
      v
Azure AI Search (Foundry IQ Knowledge Base)  <-- vector + semantic hybrid index
      |
      v
Azure AI Foundry Agent (gpt-5-mini + text-embedding-3-small)
      |
      v
Streamlit app (Responses API, Azure AD auth via `az login`)
```

## Prerequisites
- Azure account (free trial credit is enough)
- Python 3.10+
- Azure CLI (for authentication -- this app uses your Azure login, not API keys)

## 1. Create an Azure AI Foundry project
1. Go to https://ai.azure.com
2. Create a new project (pick a region with good model availability --
   Sweden Central and East US both worked during this build; if you hit an
   "InsufficientResourcesAvailable" error, that's a transient capacity issue,
   not a config problem -- just try a different region)

## 2. Deploy two models
In **Deployments**, deploy:
- A chat model (this project used `gpt-5-mini`)
- An embedding model: `text-embedding-3-small`

Both must be deployed in the **same project/region** to avoid cross-resource
complications.

## 3. Create an Azure AI Search resource
1. In portal.azure.com, create an **Azure AI Search** resource
2. **Pricing tier: Free** -- plenty for a small document set, and avoids the
   Basic tier's ~$70/month hourly billing
3. Same region and resource group as your Foundry project

## 4. Build the Knowledge Base (Foundry IQ)
1. In your Foundry project, go to **Knowledge** -> **Knowledge bases** ->
   create new
2. Connect your Azure AI Search resource
3. **Output mode: Extractive data**, **Retrieval reasoning effort: Minimal**
   (cheapest, sufficient for a small doc set)
4. Create a **Knowledge source** (File upload type -- no storage account
   needed), select your embedding model, and upload the docs from
   `sample_docs/`

## 5. Create an Agent
1. In **Deployments** -> your chat model -> **Save as agent**
2. Under **Instructions**, use something like:
   ```
   You are the CloudOps AI Assistant. Only answer using information
   retrieved from the connected knowledge base. If the knowledge base does
   not contain relevant information for a question, say so explicitly
   rather than using general knowledge. Always be specific and cite which
   document the answer came from.
   ```
3. Under **Tools**, make sure **Web Search is disabled** -- otherwise the
   model may answer from the open web instead of your documents
4. Under **Knowledge**, attach the knowledge base you built in step 4
5. Test directly in the agent's chat playground before moving to the app --
   ask a question you know the answer to from your docs, and confirm the
   response cites the right filename

> **Why an Agent, not a raw model call?** Azure OpenAI's older "On Your
> Data" extension (`data_sources` / `extra_body`) is deprecated and doesn't
> support newer models like gpt-5-mini. Microsoft's current recommended
> path is calling a Foundry Agent (with a knowledge base attached) via the
> Responses API instead -- which is what this app does.

## 6. Set up the local app
```bash
cd app
pip install -r requirements.txt
```

Install the Azure CLI and authenticate (this app uses your Azure identity,
not an API key, to call the agent):
```bash
az login
```

Copy `.env.example` to `.env` and fill in:
```
PROJECT_ENDPOINT=https://<your-resource-name>.services.ai.azure.com/api/projects/<your-project-name>
AGENT_NAME=<your-agent-name>
```
Both values are on your agent's **Details** tab in ai.azure.com.

## 7. Run it
```bash
python -m streamlit run app.py
```
Opens at `http://localhost:8501`.

## 8. Test it
Ask questions that only your documents would know the answer to, e.g.:
- "What's the naming convention for Azure access groups?"
- "A Private Endpoint shows Pending, what should I check?"
- "How long can PIM activation be time-boxed for?"

If the app gives specific, correct answers matching your docs (not generic
Azure knowledge), retrieval is working end-to-end.

## Notes on cost
- Azure AI Search Free tier: $0
- Chat + embedding model usage for a small doc set and light testing:
  well under $1 total
- The main thing to avoid: leaving a **Basic-tier** Search resource running
  (bills hourly whether used or not)

## Cleanup
When you're done demoing, delete the resource group to remove everything
and stop any further billing.
