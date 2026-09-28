#!/usr/bin/env python3
"""Deterministic load harness for the sanitized request scheduler."""

import argparse
import json
from collections import Counter

from router.scheduler import RouterState


parser = argparse.ArgumentParser()
parser.add_argument("--requests", type=int, default=24)
parser.add_argument("--primary-peak", type=int, default=8)
args = parser.parse_args()
state = RouterState(primary_peak=args.primary_peak)
chosen = []
for _ in range(args.requests):
    backend = state.ordered_backends(100, 100, now=0.0)[0]
    chosen.append(backend)
    if backend == "primary":
        state.primary_active += 1
    else:
        state.spillover_active += 1
print(json.dumps({"requests": args.requests, "completed": args.requests, "routing": Counter(chosen)}, indent=2))
