# code-server (VS Code in the browser) for Code Ocean's VS Code environment.
#
# Ubuntu + Miniforge (conda-forge) with Python 3.13 at /opt/conda, the same
# recipe as ubuntu-ffmpeg. No CUDA: code-server and its extensions need no GPU.
#
# code-server is installed at /usr/lib/code-server and its Jupyter, Python and
# Pyrefly extensions at /.vscode/extensions; Code Ocean starts code-server itself.
# files/ holds the VS Code machine settings and Code Ocean MCP server config
# that setup.sh links into the capsule on login, and installs the user's
# dotfiles if $DOTFILES_REPO is set.

# Stage 1: uv, kept in the image for capsules that manage packages with it.
FROM ghcr.io/astral-sh/uv:0.13.4@sha256:9f130421e930bfbdc563c00740466603f8723158e90297d07957c2294640262b AS uv

# Stage 2: a ready-made /opt/conda, copied into the runtime stage.
FROM quay.io/condaforge/miniforge3:26.7.2-0@sha256:16eff7459a31bed2d395b1df0dca220c067a3a9527981ec87dbbde2eafe474e5 AS miniforge

# Stage 3: code-server's release image, which holds its bundled Node.
FROM ghcr.io/coder/code-server:4.129.0@sha256:49d5e176224523b0c924ee35b05c51e9a87f9c170f650ee0f7da05a4581a79ff AS code-server

# Stage 4: runtime
FROM public.ecr.aws/docker/library/ubuntu:26.04@sha256:c098726dd9b9733f3e885f8de0ef375206a311b0a317eadc40d347b1115fb944

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="code-server + Miniforge + Jupyter, Python and Code Ocean MCP tooling."
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive
ENV CONDA_DIR=/opt/conda
ENV PATH=/root/.local/bin:${CONDA_DIR}/bin:${PATH}
ENV PYTHONPATH=/code
ENV UV_NO_CACHE=1
ENV IS_SANDBOX=1

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
RUN mkdir -p /.vscode/extensions \
 && code-server --extensions-dir=/.vscode/extensions \
      --install-extension ms-toolsai.jupyter \
      --install-extension ms-python.python \
      --install-extension meta.pyrefly

COPY files /.files
RUN echo "bash /.files/setup.sh" >> /root/.profile
