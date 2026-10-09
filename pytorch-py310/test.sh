#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
python -c "import sys; assert sys.prefix == \"/opt/conda\", sys.prefix; assert sys.version_info[:2] == (3, 10), sys.version"
conda --version
jupyter lab --version
pip check
python - <<'PY'
import torch
import torchaudio
import torchvision
assert torch.version.cuda.startswith("13."), torch.version.cuda
# torchaudio releases lag torch; exercise its ops to catch an ABI mismatch.
torchaudio.functional.resample(torch.randn(1, 16000), 16000, 8000)
torchvision.ops.nms(torch.tensor([[0.0, 0.0, 1.0, 1.0]]), torch.tensor([1.0]), 0.5)
print("torch", torch.__version__, "torchvision", torchvision.__version__, "torchaudio", torchaudio.__version__)
PY
