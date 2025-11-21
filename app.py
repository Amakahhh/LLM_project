"""
app.py
------
Flask web UI for the LLM Question-and-Answering system.

Run locally:
    export FLASK_APP=app.py  # or setx on Windows
    flask run --reload
"""

from __future__ import annotations

import os

from flask import Flask, render_template, request

from qa_utils import QAResult, run_qa

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "dev-secret-key")


@app.route("/", methods=["GET", "POST"])
def index():
    result: QAResult | None = None
    error: str | None = None
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "").strip()
        if not question:
            error = "Please enter a question before submitting."
        else:
            try:
                result = run_qa(question)
            except Exception as exc:  # noqa: BLE001
                error = str(exc)

    return render_template(
        "index.html",
        question=question,
        result=result,
        error=error,
    )


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

