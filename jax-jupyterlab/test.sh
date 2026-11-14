#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
python -c "import sys; assert sys.prefix == \"/opt/conda/envs/py\", sys.prefix; assert sys.version_info[:2] == (3, 13), sys.version"
conda --version
# A capsule's conda install must land in py and keep the packages uv installed.
test "$(conda info --json | python -c 'import json, sys; print(json.load(sys.stdin)["active_prefix"])')" = /opt/conda/envs/py
conda config --show prefix_data_interoperability | grep -qx 'prefix_data_interoperability: True'
jupyter lab --version
pip check
# jax falls back to CPU with only a warning if the CUDA plugin is missing or
# does not match jaxlib.
python - <<'PY'
from importlib.metadata import version
import jax
assert version("jax-cuda13-plugin") == version("jaxlib"), version("jax-cuda13-plugin")
version("jax-cuda13-pjrt")
print("jax", jax.__version__)
PY
