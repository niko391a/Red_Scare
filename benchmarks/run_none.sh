#!/usr/bin/env bash
# Runs the None benchmark on the selected datasets and writes
# benchmarks/none-<timestamp>.txt. Usage: benchmarks/run_none.sh [dataset ...]
# (dataset names without data/ and .txt, e.g. wall-n-1000). No args = default set.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

# Activate the virtualenv if there is one
for v in venv .venv; do
    [ -f "$v/bin/activate" ] && source "$v/bin/activate" && break
done

OUT="benchmarks/none-$(date +%Y%m%d-%H%M%S).txt"
PROFILE="$(powerprofilesctl get 2>/dev/null || echo unknown)"

{
    echo "# None benchmark"
    echo "Date: $(date -Iseconds)"
    echo "Power profile: $PROFILE"
    echo "Python: $(python --version 2>&1) | networkx $(python -c 'import networkx; print(networkx.__version__)')"
    echo
    python benchmark_none.py "$@"
} | tee "$OUT"

echo "Wrote $OUT" >&2
