#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
python -c "import sys; assert sys.prefix == \"/opt/conda\", sys.prefix; assert sys.version_info[:2] == (3, 13), sys.version"
conda --version
jupyter lab --version
pip check
python - <<'PY'
import ctypes
import tensorflow as tf
assert tf.test.is_built_with_cuda()
# Resolved through LD_LIBRARY_PATH, which names the Python version.
ctypes.CDLL("libcusolver.so.11")
print("tensorflow", tf.__version__)
PY
