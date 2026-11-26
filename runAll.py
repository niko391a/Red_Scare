import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
script = root / "red-scare.py"
files = sorted((root / "data").glob("*.txt"))

if not files:
    sys.exit(f"No .txt files found in {root / 'data'}")

width = max(len("Instance name"), *(len(f.stem) for f in files))

def row(name, values):
    return f"{name:<{width}}" + "".join(f"{v:>8}" for v in values)

with (root / "results.txt").open("w", encoding="utf-8") as out:
    def emit(line):
        print(line, flush=True)
        print(line, file=out, flush=True)

    emit(row("Instance name", ["n", "A", "F", "M", "N", "S"]))
    for f in files:
        result = subprocess.run(
            [sys.executable, str(script), str(f), "--no-draw"],
            stdout=subprocess.PIPE, text=True,
        )
        if result.returncode == 0:
            emit(row(f.stem, result.stdout.splitlines()[-1].split("\t")))
        else:
            emit(row(f.stem, ["ERROR"]))