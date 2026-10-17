#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
R --version | sed -n 1p
# r2u installs CRAN packages as apt binaries through bspm.
Rscript -e 'stopifnot(requireNamespace("bspm", quietly = TRUE))'
rstudio-server version
