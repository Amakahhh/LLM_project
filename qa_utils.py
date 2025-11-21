"""
Shared helpers for the LLM Question-and-Answering project.

This module performs three core tasks:
1. Preprocess user questions (lowercasing, punctuation removal, tokenization).
2. Build an instructional prompt for the LLM.
3. Send the prompt to the configured LLM provider and return the final answer.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import List, Tuple

from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError

load_dotenv()

SYSTEM_PROMPT = (
    "You are a helpful, step-by-step teaching assistant. "
    "Always explain your reasoning clearly and cite any assumptions."
)
DEFAULT_MODEL = os.getenv("LLM_MODEL", "gemini-1.5-flash")
_GENAI_READY = False


@dataclass
class QAResult:
    """Container for every artifact produced during a QA run."""

    original_question: str
    cleaned_question: str
    tokens: List[str]
    answer: str


def preprocess_question(question: str) -> Tuple[str, List[str]]:
    """
    Lowercase the question, strip punctuation, and return tokens.

    Args:
        question: Raw natural-language input from the user.
    Returns:
        A tuple of (cleaned_question, tokens).
    """
    lowered = question.strip().lower()
    cleaned = re.sub(r"[^\w\s]", "", lowered)
    tokens = [token for token in cleaned.split() if token]
    return cleaned, tokens


def build_prompt(original: str, cleaned: str, tokens: List[str]) -> str:
    """
    Construct a structured prompt for the LLM.

    The prompt reminds the model to keep explanations approachable so
    beginners can follow along.
    """
    token_display = ", ".join(tokens) if tokens else "No tokens detected"
    return (
        "A learner has asked a question. Use the normalized text below, "
        "then reply with a clear, beginner-friendly answer that walks through "
        "the reasoning step-by-step.\n\n"
        f"Original question: {original}\n"
        f"Normalized question: {cleaned}\n"
        f"Tokens: {token_display}\n\n"
        "Answer:"
    )


def _ensure_client() -> None:
    """Configure the Gemini client once using the provided API key."""
    global _GENAI_READY
    if _GENAI_READY:
        return

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is not set. Create a .env file or set the "
            "environment variable with your Gemini API key."
        )

    genai.configure(api_key=api_key)
    _GENAI_READY = True


def ask_llm(prompt: str, *, model: str = DEFAULT_MODEL, temperature: float = 0.2) -> str:
    """Send the prompt to the LLM and return the generated answer."""
    _ensure_client()
    try:
        generative_model = genai.GenerativeModel(
            model_name=model,
            system_instruction=SYSTEM_PROMPT,
        )
        response = generative_model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=600,
            ),
        )
    except GoogleAPIError as exc:
        raise RuntimeError(
            "Unable to reach the Gemini API. Verify your API key, network "
            "connection, and model name."
        ) from exc

    text = (response.text or "").strip()
    if not text:
        raise RuntimeError("The LLM returned an empty response.")
    return text


def run_qa(question: str) -> QAResult:
    """High-level helper that returns every step of the QA pipeline."""
    if not question or not question.strip():
        raise ValueError("Question cannot be empty.")

    cleaned, tokens = preprocess_question(question)
    prompt = build_prompt(question, cleaned, tokens)
    answer = ask_llm(prompt)
    return QAResult(
        original_question=question,
        cleaned_question=cleaned,
        tokens=tokens,
        answer=answer,
    )


__all__ = ["QAResult", "run_qa", "preprocess_question", "build_prompt", "ask_llm"]

