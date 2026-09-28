from dataclasses import dataclass


@dataclass(frozen=True)
class Backend:
    name: str
    url: str
    context_limit: int
    completion_limit: int


PRIMARY = Backend("primary", "http://127.0.0.1:8203", 32_768, 8)
SPILLOVER = Backend("spillover", "http://127.0.0.1:8202", 131_072, 160)
