#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
python -c "import sys; assert sys.prefix == \"/opt/conda\", sys.prefix; assert sys.version_info[:2] == (3, 13), sys.version"
conda --version
ffmpeg -hide_banner -version | sed -n 1p
ffprobe -hide_banner -version | sed -n 1p
