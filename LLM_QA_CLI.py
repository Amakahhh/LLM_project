"""
LLM_QA_CLI.py
--------------
Command-line interface for the LLM-powered question-and-answering system.

Usage:
    python LLM_QA_CLI.py --question "What is machine learning?"

If --question is omitted, the script will prompt for input interactively.
"""

from __future__ import annotations

import argparse
import sys
from textwrap import fill

from qa_utils import QAResult, run_qa


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ask a natural-language question and receive an LLM answer."
    )
    parser.add_argument(
        "-q",
        "--question",
        type=str,
        help="Question to send to the LLM. If omitted, you will be prompted.",
    )
    return parser.parse_args()


def display_result(result: QAResult) -> None:
    print("\n=== Step-by-step processing ===")
    print(f"1. Original question:\n   {result.original_question}")
    print(f"2. Lowercased & punctuation removed:\n   {result.cleaned_question or '(empty)'}")
    print(f"3. Tokenized words:\n   {', '.join(result.tokens) if result.tokens else '(no tokens)'}")
    print("\n=== LLM answer ===")
    print(fill(result.answer, width=88))


def main() -> int:
    args = parse_args()
    question = args.question or input("Enter your question: ").strip()

    if not question:
        print("Please provide a question before running the CLI.")
        return 1

    try:
        result = run_qa(question)
    except Exception as exc:  # noqa: BLE001
        print(f"Something went wrong: {exc}")
        return 1

    display_result(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())

