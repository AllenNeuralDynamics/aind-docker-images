#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
# The /usr/local/bin shims must resolve into the /opt/venv venv.
/usr/local/bin/python -c "import sys; assert sys.version_info[:2] == (3, 13), sys.version; assert sys.prefix == \"/opt/venv\", sys.prefix"
/usr/local/bin/pip --version | grep -q /opt/venv
uv --version
ldconfig -p | grep -q libcublas.so.12
ldconfig -p | grep -q libnccl.so.2
