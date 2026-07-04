# ☁️ CloudOps AI Assistant

A RAG-based AI assistant that answers natural-language questions about
cloud architecture, migration runbooks, troubleshooting guides, and
identity governance standards — grounded in an indexed knowledge base,
not generic AI knowledge.

Built to solve a real, recurring problem: engineers repeatedly asking the
same questions that are already documented somewhere, and new joiners
needing fast answers without a full knowledge-transfer session.

## How it works

```
Sample docs (.md)
      |
      v
Azure AI Search (Foundry IQ Knowledge Base)  <- vector + semantic hybrid index
      |
      v
Azure AI Foundry Agent (gpt-5-mini + text-embedding-3-small)
      |
      v
Streamlit app (Responses API, Azure AD auth)
```

The agent is grounded to **only** answer from the indexed documents and
cites which source file each answer came from — reducing hallucination
and keeping answers traceable back to real documentation.

## Demo

**"What's the naming convention for Azure access groups?"**
> The standard is: `az-<subscription>-<role>-<environment>` (example:
> `az-prod-contributor-eastus`). Groups must map to a single Azure RBAC
> role at a single scope (no nesting of multiple roles in one group).

**"A Private Endpoint shows Pending status, what should I check?"**
> Check the following (from the Private Endpoint troubleshooting runbook):
> confirm the connection state is Approved, verify DNS resolution to the
> private IP, check NSGs/route tables on the subnet, and validate hub
> firewall rules if traffic transits a firewall.

See `screenshots/` for the full working chat interface.

## Tech stack

- **Azure AI Foundry** — Agent Service, Foundry IQ Knowledge Base
- **Azure OpenAI** — `gpt-5-mini` (chat), `text-embedding-3-small` (embeddings)
- **Azure AI Search** — vector + semantic hybrid retrieval
- **Python / Streamlit** — chat UI
- **Azure Identity** — Azure AD authentication (no API keys in the client)

## Notable engineering decision

This project originally used Azure OpenAI's "On Your Data" extension for
retrieval, but that feature is deprecated and doesn't support newer chat
models like `gpt-5-mini`. After tracing a persistent, opaque validation
error back to that deprecation, the integration was migrated to Microsoft's
current recommended pattern: calling a Foundry Agent (with a knowledge
base attached) directly via the Responses API.

## Setup

See [SETUP_GUIDE.md](./SETUP_GUIDE.md) for full step-by-step instructions,
including Azure resource creation, knowledge base configuration, and
running the app locally.

## Project structure

```
app/             Streamlit app (app.py, requirements.txt)
sample_docs/     Synthetic knowledge base content (architecture,
                 runbooks, troubleshooting, governance standards)
screenshots/     Working demo screenshots
SETUP_GUIDE.md   Full setup walkthrough
```

## Related project

[IaC Compliance Assistant](https://github.com/jjohn09/iac-compliance-assistant)
— a companion project using the same Azure OpenAI resource, but with a
direct-prompting architecture instead of RAG, reviewing Terraform code
against governance policy.
