#!/usr/bin/env python3
import json

from router.scheduler import RouterState


state = RouterState(primary_peak=8)
short = []
for _ in range(24):
    chosen = state.ordered_backends(100, 100, now=0.0)[0]
    short.append(chosen)
    if chosen == "primary":
        state.primary_active += 1
    else:
        state.spillover_active += 1
long_route = state.ordered_backends(40_000, 1_000, now=0.0)
print(json.dumps({"primary": short.count("primary"), "spillover": short.count("spillover"), "long_route": long_route}, indent=2))
