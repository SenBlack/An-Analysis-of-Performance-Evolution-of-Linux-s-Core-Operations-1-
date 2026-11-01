#!/usr/bin/env bash
# Clone the pinned LEBench commit into third_party/LEBench.
# The destination is gitignored. Re-running keeps the same commit.

set -eu

UPSTREAM_URL="https://github.com/LinuxPerfStudy/LEBench.git"
UPSTREAM_COMMIT="6aa7801a107d26e45eb65c7d827c7ea08059a3d3"
DEST="third_party/LEBench"

mkdir -p third_party

if [[ ! -d "${DEST}/.git" ]]; then
  git clone "${UPSTREAM_URL}" "${DEST}"
fi

git -C "${DEST}" fetch --tags origin
git -C "${DEST}" checkout --detach "${UPSTREAM_COMMIT}"

echo "LEBench is at $(git -C "${DEST}" rev-parse HEAD)"
echo "License: ${DEST}/LICENSE (Apache License 2.0)"
echo "Next: read ${DEST}/README.md and ${DEST}/EXPERIMENTS.md"
