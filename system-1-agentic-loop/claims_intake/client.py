"""Anthropic client factory and model config."""

import os

from anthropic import Anthropic


def make_client() -> Anthropic:
    """Construct an Anthropic client from env. Fails fast if API key is missing."""
    api_key = os.environ.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_AUTH_TOKEN")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set. Export it before running, e.g.:\n"
            "    export ANTHROPIC_API_KEY=sk-ant-..."
        )
    base_url = os.environ.get("ANTHROPIC_BASE_URL")
    if base_url:
        return Anthropic(api_key=api_key, base_url=base_url)
    return Anthropic(api_key=api_key)


DEFAULT_MODEL = "claude-haiku-4-5-20251001"
