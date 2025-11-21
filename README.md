# LLM Question-and-Answering System

This project delivers both a Python command-line interface (CLI) and a Flask-based web UI that send user questions to an LLM API (OpenAI by default) after basic text preprocessing.

## Project structure

```
LLM_QA_Project_yourName_matricNo/
├── LLM_QA_CLI.py
├── app.py
├── qa_utils.py
├── requirements.txt
├── LLM_QA_hosted_webGUI_link.txt
├── templates/
│   └── index.html
└── static/            # optional (not used yet)
```

## Prerequisites

1. Python 3.10+
2. An LLM API key (default: `OPENAI_API_KEY` for OpenAI)
3. (Optional) A `.env` file at the project root:
   ```
   OPENAI_API_KEY=sk-...
   LLM_MODEL=gpt-4o-mini
   FLASK_SECRET_KEY=change-me
   ```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the CLI (Part A)

```bash
python LLM_QA_CLI.py --question "What is gradient descent?"
```

If you omit `--question`, the script prompts for interactive input.

## Run the web app locally (Part B)

```bash
export FLASK_APP=app.py  # use setx on Windows PowerShell: setx FLASK_APP app.py
flask run --reload
```

Open `http://127.0.0.1:5000` to interact with the GUI.

## Deploying the web app (Part C)

1. Choose a hosting platform (Render, PythonAnywhere, Streamlit Cloud, Vercel).
2. Set the `OPENAI_API_KEY` (and optionally `LLM_MODEL` + `FLASK_SECRET_KEY`) as environment variables on the platform.
3. Use `gunicorn app:app` (Render/Vercel) or the platform’s built-in WSGI runner.
4. Update `LLM_QA_hosted_webGUI_link.txt` with your name, matric number, deployment URL, and GitHub repository link.

## GitHub submission (Part D)

Push the entire folder structure above to your GitHub repository named according to your assignment instructions.

