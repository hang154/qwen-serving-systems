import time
from dataclasses import dataclass, field


@dataclass
class CooldownRegistry:
    seconds: float = 15.0
    failed_until: dict[str, float] = field(default_factory=dict)

    def mark_failed(self, backend: str, now: float | None = None) -> None:
        self.failed_until[backend] = (time.monotonic() if now is None else now) + self.seconds

    def available(self, backend: str, now: float | None = None) -> bool:
        return self.failed_until.get(backend, 0.0) <= (time.monotonic() if now is None else now)
