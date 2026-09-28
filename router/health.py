from dataclasses import dataclass, field


@dataclass
class Health:
    failures: dict[str, int] = field(default_factory=lambda: {"primary": 0, "spillover": 0})

    def record_failure(self, backend: str) -> None:
        self.failures[backend] = self.failures.get(backend, 0) + 1
