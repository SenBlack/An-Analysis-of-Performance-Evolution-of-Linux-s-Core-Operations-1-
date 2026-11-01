.PHONY: env fetch

# Print host OS, kernel, compiler, and Python versions.
env:
	bash scripts/record_environment.sh

# Clone LEBench at the commit recorded in the README.
fetch:
	bash scripts/fetch_lebench.sh
