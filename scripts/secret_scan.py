import re
import sys
from pathlib import Path


root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
patterns = {
    "private key": re.compile(r"BEGIN [A-Z ]*PRIVATE KEY"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{16,}"),
    "absolute user path": re.compile(r"/home/[A-Za-z0-9_.-]+/"),
    "authorization header": re.compile(r"Authorization:\s*(Bearer|Basic)\s+\S+", re.I),
}
failures = []
for path in root.rglob("*"):
    if not path.is_file() or ".git" in path.parts:
        continue
    if path.resolve() == Path(__file__).resolve():
        continue
    try:
        text = path.read_text()
    except UnicodeDecodeError:
        continue
    for label, pattern in patterns.items():
        if pattern.search(text):
            failures.append(f"{path}: {label}")
if failures:
    raise SystemExit("\n".join(failures))
print("secret scan: PASS")
