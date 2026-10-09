#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
python -c "import sys; assert sys.prefix == \"/opt/conda\", sys.prefix; assert sys.version_info[:2] == (3, 13), sys.version"
conda --version
jupyter lab --version
pip check
python - <<'PY'
import lightning
import torch
assert torch.version.cuda.startswith("13."), torch.version.cuda
print("torch", torch.__version__, "lightning", lightning.__version__)
PY
tensorboard --version
