#!/usr/bin/env bash
# Print versions that affect a later LEBench run.
# No absolute paths. Safe to re-run; writes nothing.

set -eu

echo "date: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo "uname: $(uname -a)"

if [[ -r /etc/os-release ]]; then
  # shellcheck disable=SC1091
  . /etc/os-release
  echo "os: ${PRETTY_NAME:-unknown}"
else
  echo "os: unknown"
fi

if command -v gcc >/dev/null 2>&1; then
  echo "gcc: $(gcc --version | head -n 1)"
else
  echo "gcc: not installed"
fi

if command -v cc >/dev/null 2>&1; then
  echo "cc: $(cc --version | head -n 1)"
else
  echo "cc: not installed"
fi

if command -v python3 >/dev/null 2>&1; then
  echo "python3: $(python3 --version)"
else
  echo "python3: not installed"
fi

if command -v git >/dev/null 2>&1; then
  echo "git: $(git --version)"
else
  echo "git: not installed"
fi

if command -v make >/dev/null 2>&1; then
  echo "make: $(make --version | head -n 1)"
else
  echo "make: not installed"
fi
