#!/usr/bin/env bash
# Smoke test run inside the built image by .github/workflows/test_images.yml.
set -euo pipefail
python -c "import sys; assert sys.prefix == \"/opt/conda\", sys.prefix; assert sys.version_info[:2] == (3, 13), sys.version"
conda --version
uv --version
code-server --version
claude --version
code-server --extensions-dir=/.vscode/extensions --list-extensions | grep -x ms-toolsai.jupyter
code-server --extensions-dir=/.vscode/extensions --list-extensions | grep -x ms-python.python
code-server --extensions-dir=/.vscode/extensions --list-extensions | grep -x meta.pyrefly
code-server --extensions-dir=/.vscode/extensions --list-extensions | grep -x anthropic.claude-code
codeocean-mcp-server --help > /dev/null
python -c "import ipykernel"
pip check
