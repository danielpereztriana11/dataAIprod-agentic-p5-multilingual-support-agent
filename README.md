# Multilingual Support Agent

Data & AI Product project: an agent that helps users resolve support questions across languages.

## Status

Initial Python project scaffold. Language detection, knowledge retrieval, response generation, and human handoff are planned; no model provider or support integration is configured yet.

## Local setup

Requires Python 3.11 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

On macOS/Linux, activate with `source .venv/bin/activate` and copy the template with `cp .env.example .env`.

The environment template documents future configuration; the scaffold does not load it yet. Keep credentials in your local `.env` and never commit them.

## Development checks

```shell
ruff check .
ruff format --check .
python -m compileall -q src
```

## Structure

- `src/multilingual_support_agent/`: Python package.
- `docs/`: product scope and design notes.
- `.github/`: pull request template and CI workflow.

See [the product brief](docs/product-brief.md) for the initial scope and [CONTRIBUTING.md](CONTRIBUTING.md) for the contribution workflow.

## License

No license has been selected yet.
