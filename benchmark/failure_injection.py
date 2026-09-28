#!/usr/bin/env python3
import json

from router.scheduler import RouterState


state = RouterState()
before = state.ordered_backends(100, 100, now=0.0)
state.cooldowns.mark_failed("primary", now=0.0)
during = state.ordered_backends(100, 100, now=1.0)
after = state.ordered_backends(100, 100, now=16.0)
print(json.dumps({"before": before, "during_cooldown": during, "after_cooldown": after}, indent=2))
