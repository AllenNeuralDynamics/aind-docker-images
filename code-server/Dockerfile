# code-server (VS Code in the browser) for Code Ocean's VS Code environment.
#
# Ubuntu + Miniforge (conda-forge) with Python 3.13 at /opt/conda, the same
# recipe as ubuntu-ffmpeg. No CUDA: code-server and its extensions need no GPU.
#
# code-server is installed at /usr/lib/code-server and its Jupyter, Python,
# Pyrefly and Claude Code extensions at /.vscode/extensions; Code Ocean starts
# code-server itself. The Claude Code CLI is installed at /usr/local/bin/claude.
# files/ holds the VS Code machine settings and Code Ocean MCP server config
# that setup.sh links into the capsule on login, and installs the user's
# dotfiles if $DOTFILES_REPO is set.

# Stage 1: uv, kept in the image for capsules that manage packages with it.
FROM ghcr.io/astral-sh/uv:0.13.4@sha256:9f130421e930bfbdc563c00740466603f8723158e90297d07957c2294640262b AS uv

# Stage 2: a ready-made /opt/conda, copied into the runtime stage.
FROM quay.io/condaforge/miniforge3:26.7.2-0@sha256:16eff7459a31bed2d395b1df0dca220c067a3a9527981ec87dbbde2eafe474e5 AS miniforge

# Stage 3: code-server's release image, which holds its bundled Node.
FROM ghcr.io/coder/code-server:4.145.2@sha256:09565f9e07f5624554e295e8bab0e2fec4a7c533eb3cff459ed6596a4d3d7c1c AS code-server

# Stage 4: runtime
FROM public.ecr.aws/docker/library/ubuntu:26.04@sha256:c098726dd9b9733f3e885f8de0ef375206a311b0a317eadc40d347b1115fb944

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="code-server + Miniforge, Python, Claude Code and Code Ocean MCP tooling."
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive
ENV CONDA_DIR=/opt/conda

# update PATH for uv tool usage
ENV PATH=/root/.local/bin:${CONDA_DIR}/bin:${PATH}
ENV UV_NO_CACHE=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential bzip2 ca-certificates curl git gnupg2 locales unzip \
 && rm -rf /var/lib/apt/lists/*

COPY --from=uv /uv /uvx /usr/local/bin/

COPY --from=miniforge ${CONDA_DIR} ${CONDA_DIR}
# Pin conda to the Miniforge release so that swapping Python does not upgrade it.
RUN echo "conda ==$(conda --version | cut -d' ' -f2)" >> ${CONDA_DIR}/conda-meta/pinned \
 && conda install -y python=3.13 \
 && conda clean -afy \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> /etc/skel/.bashrc \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> ~/.bashrc

# pyproject.toml lists the direct dependencies and uv.lock pins the full
# tree with hashes; conda provides only the interpreter.
COPY pyproject.toml uv.lock /tmp/env/
RUN --mount=from=uv,source=/uv,target=/bin/uv \
    uv export --frozen --no-cache --project /tmp/env -o /tmp/env/requirements.txt \
 && uv pip install --no-cache --python ${CONDA_DIR}/bin/python --require-hashes -r /tmp/env/requirements.txt \
 && rm -rf /tmp/env /tmp/uv-*.lock

COPY --from=code-server /usr/lib/code-server /usr/lib/code-server
COPY --from=code-server /usr/bin/code-server /usr/bin/code-server

# Install the latest native CLI at build time (unpinned, so Dependabot cannot
# track it), verified against the checksum in the release manifest. CI builds
# linux/amd64 only; build locally with --platform linux/amd64.
RUN platform=linux-x64 \
 && base=https://downloads.claude.ai/claude-code-releases \
 && version="$(curl -fsSL ${base}/latest)" \
 && checksum="$(curl -fsSL ${base}/${version}/manifest.json \
      | python -c "import json,sys; print(json.load(sys.stdin)['platforms']['${platform}']['checksum'])")" \
 && curl -fsSL "${base}/${version}/${platform}/claude" -o /usr/local/bin/claude \
 && echo "${checksum}  /usr/local/bin/claude" | sha256sum -c - \
 && chmod 755 /usr/local/bin/claude

RUN mkdir -p /.vscode/extensions \
 && code-server --extensions-dir=/.vscode/extensions \
      --install-extension ms-toolsai.jupyter \
      --install-extension ms-python.python \
      --install-extension meta.pyrefly \
      --install-extension anthropic.claude-code

COPY files /.files
RUN echo "bash /.files/setup.sh" >> /root/.profile
