"""Small, dependency-free policy core extracted from a production router."""


def choose_backend(input_tokens, output_tokens, primary_active, *, limit=32768, peak=8):
    total = input_tokens + output_tokens
    if total > 131072:
        raise ValueError("request exceeds long-context limit")
    if total > limit:
        return "long_context"
    return "primary" if primary_active < peak else "spillover"

