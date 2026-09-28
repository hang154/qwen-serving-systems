SHORT_CONTEXT = 32_768
MAX_CONTEXT = 131_072


def classify(input_tokens: int, output_tokens: int) -> str:
    total = input_tokens + output_tokens
    if min(input_tokens, output_tokens) < 0:
        raise ValueError("token counts must be non-negative")
    if total > MAX_CONTEXT:
        raise ValueError("request exceeds long-context limit")
    return "long" if total > SHORT_CONTEXT else "short"
