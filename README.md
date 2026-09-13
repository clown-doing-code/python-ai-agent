# Python AI Agent

A minimal AI coding agent (boot.dev course project) that turns natural-language requests into actual file operations. It connects to an LLM through [OpenRouter](https://openrouter.ai) and lets the model drive a set of sandboxed tools (list files, read files, write files, run Python scripts) to complete coding tasks.

## How it works

1. You pass a prompt like `"Add a division capability to the calculator"` as a CLI argument.
2. The agent calls an LLM (`openrouter/free`) with the four available tools defined in `functions/`.
3. The model responds with a sequence of function calls. Each call is dispatched by `functions/call_function.py` to the matching implementation.
4. Tool results are fed back to the model, and the loop repeats until the model produces a final answer (up to `MAX_ITERATIONS` = 20 turns).
5. All file access is confined to the sandboxed `./calculator` working directory — paths that escape it (e.g. `../`, `/bin`) are rejected.

## Requirements

- Python 3.13+
- [uv](https://docs.astral.sh/uv/) (package manager)
- An [OpenRouter](https://openrouter.ai) API key

## Setup

```bash
uv sync
cp .env.example .env  # or create .env manually
```

Then add your key to `.env`:

```
OPENROUTER_API_KEY=sk-or-v1-...
```

## Usage

```bash
python main.py "<your prompt>" [--verbose]
```

Examples:

```bash
python main.py "List the files in the calculator project"
python main.py "Run the calculator tests"
python main.py "Add a square root function to the calculator" --verbose
```

Pass `--verbose` to see the prompt, token usage per call, and every tool call and result.

## Tools available to the model

| Tool | Description |
|---|---|
| `list_files_info` | List a directory's contents (name, size in bytes, whether it's a directory) |
| `get_file_content` | Read a file's contents (truncated at 10,000 chars) |
| `run_python_file` | Run a `.py` file in a subprocess with optional args (30s timeout) |
| `write_file` | Create or overwrite a file (creates missing parent directories) |

All tools enforce a path-safety check that rejects any path resolving outside the working directory (`./calculator`).

## Project layout

```
├── main.py                 # CLI entry point and agent loop
├── config.py               # Constants (MAX_CHARS, MAX_ITERATIONS) + system prompt
├── functions/              # Tool schemas and implementations
│   ├── call_function.py    # Tool registry / dispatcher
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
└── calculator/             # Sandbox target project the agent operates on
    ├── main.py             # CLI calculator app
    ├── tests.py            # Calculator unittest suite
    └── pkg/
        ├── calculator.py   # Infix expression evaluator
        └── render.py       # JSON output formatter
```

## Configuration

- `OPENROUTER_API_KEY` — API key for OpenRouter (in `.env`).
- `MAX_CHARS` — file-read truncation limit (10,000).
- `MAX_ITERATIONS` — max agent loop iterations before giving up (20).
- The working directory for all tool calls is hardcoded to `./calculator`.

## Running tests

The calculator itself has a unittest suite:

```bash
cd calculator
python -m unittest tests.py
```

The agent's tools also have ad-hoc smoke-test scripts at the repo root (`test_get_files_info.py`, `test_get_file_content.py`, `test_run_python_file.py`, `test_write_file.py`) that exercise happy paths and security cases (path traversal, nonexistent files).