#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
python -c "import sys; assert sys.prefix == \"/opt/conda\", sys.prefix; assert sys.version_info[:2] == (3, 13), sys.version"
conda --version
jupyter lab --version
pip check
# Without the CUDA plugin, jax installs and silently runs on CPU.
python - <<'PY'
from importlib.metadata import version
import jax
assert version("jax-cuda13-plugin") == version("jaxlib"), version("jax-cuda13-plugin")
version("jax-cuda13-pjrt")
print("jax", jax.__version__)
PY
