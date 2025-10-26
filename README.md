(The file `d:\IMP_JOB_SEARCH\coding-challanges\07-charles-huang-challenge\code\README.md` exists, but is empty)
# Robot Driver — MCP + LLM Planner

This project demonstrates an architecture where an LLM generates a step-by-step
plan (JSON) based on structured page context provided by a Playwright MCP
server (or a local Playwright snapshot). The plan is executed by Playwright.

Key files:
- `main.py`: orchestration entry point. Provide a plain-English goal (or URL) and the program will:
	1. fetch page context from MCP server (if `MCP_URL` is set) or snapshot locally,
	2. call a local/open-source LLM (Transformers) to generate a JSON plan,
	3. execute the plan using Playwright.
- `mcp_client.py`: MCP client + local Playwright snapshot helper.
- `llm_planner.py`: wraps a seq2seq model (default: `google/flan-t5-small`) to produce JSON plans.
- `executor.py`: maps plan actions to Playwright operations.

Requirements:
- Python 3.8+
- See `requirements.txt` for Python dependencies.

Quick start (Windows, cmd.exe):

1) Install dependencies and Playwright browsers:

```cmd
pip install -r requirements.txt
python -m playwright install
```

2) Run the autonomous runner with a goal or URL:

```cmd
python main.py "Buy the cheapest blue shirt on this site"
```

Notes and configuration:
- To use an external MCP server, set the `MCP_URL` environment variable, e.g.
	`set MCP_URL=http://localhost:3000`.
- The default LLM is `google/flan-t5-small`. It will be downloaded by `transformers` on first run. You can change the model by setting `LLM_MODEL` environment variable.
- This implementation avoids OpenAI and uses an open-source transformer model locally.

Limitations:
- Small sequence-to-sequence models may not reliably produce perfectly-structured JSON; inspect the generated plan before running against critical websites.
- Creating robust CSS selectors from snapshots is best-effort. For production use, add better selector extraction and verification.
