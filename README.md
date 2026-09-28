# Qwen Serving Systems

Sanitized reference implementation and measured evidence for request-level
routing across two resident Qwen3.8-27B backends.

## Policy

- Short requests prefer the primary backend up to eight active completions.
- Above that threshold, short requests spill to the second resident backend.
- Requests beyond the primary context limit route only to the long-context
  backend.
- Backend connection errors and HTTP 5xx responses trigger cooldown and
  fallback.
- Tokenization does not affect completion load balancing.

## Verified outcomes

- 12 concurrent balanced requests: 12/12, split 6/6.
- Eight direct requests to the primary: 8/8.
- 24 requests through the stable adapter: 24/24; primary 8, spillover 16.
- Korean instruction following, named-context handling, JSON Schema output,
  image input, and normalized tool calls passed the preserved test suite.
- Intentional router termination was followed by successful supervisor restart.

The public repository uses generic backend names and loopback example URLs.
It excludes tokens, IP addresses, SSH hosts, usernames, customer data, private
paths, and deployment unit files.

## Test

```bash
python -m unittest discover -s tests -v
python scripts/secret_scan.py .
```

## Capacity boundary

Inference work cannot be migrated live to a GPU without a resident model.
The validated peak-load strategy is therefore request-level spillover, not
cross-device compute migration.

