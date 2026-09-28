from dataclasses import dataclass, field

from .context_policy import classify
from .cooldown import CooldownRegistry


@dataclass
class RouterState:
    primary_active: int = 0
    spillover_active: int = 0
    primary_peak: int = 8
    cooldowns: CooldownRegistry = field(default_factory=CooldownRegistry)

    def ordered_backends(self, input_tokens: int, output_tokens: int, now: float | None = None) -> list[str]:
        request_class = classify(input_tokens, output_tokens)
        if request_class == "long":
            return ["spillover"] if self.cooldowns.available("spillover", now) else []
        preferred = "primary" if self.primary_active < self.primary_peak else "spillover"
        fallback = "spillover" if preferred == "primary" else "primary"
        return [name for name in (preferred, fallback) if self.cooldowns.available(name, now)]


def choose_backend(input_tokens: int, output_tokens: int, primary_active: int, *, limit: int = 32768, peak: int = 8) -> str:
    if limit != 32_768:
        total = input_tokens + output_tokens
        if total > 131_072:
            raise ValueError("request exceeds long-context limit")
        if total > limit:
            return "long_context"
    state = RouterState(primary_active=primary_active, primary_peak=peak)
    selected = state.ordered_backends(input_tokens, output_tokens)
    if not selected:
        raise RuntimeError("no healthy backend")
    return "long_context" if classify(input_tokens, output_tokens) == "long" else selected[0]
