# Minimal base: NVIDIA CUDA 12 runtime + uv-managed Python 3.13.
# No conda, no ML framework, no notebook server baked in — add what
# you need in your capsule.
#
# GPU availability is a deployment-time concern: the image includes
# CUDA userspace libs (libcudart, libcublas, libcudnn, NCCL) but the
# host driver is bind-mounted by nvidia-container-toolkit only when
# the container is run with --gpus (on Code Ocean, controlled by the
# capsule's machine type).

# Stage 1: uv binary, pulled from Astral's distroless image.
FROM ghcr.io/astral-sh/uv:0.11.7 AS uv

# Stage 2: runtime on CUDA 12.8 / Ubuntu 24.04
FROM docker.io/nvidia/cuda:12.8.1-runtime-ubuntu24.04

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="CUDA 12.8 runtime + uv-managed Python 3.13. Minimal base for GPU-enabled AIND capsules."
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive
# Matplotlib default: headless-safe for reproducible runs.
ENV MPLBACKEND=Agg
ENV VIRTUAL_ENV=/opt/venv
# /opt/venv/bin wins over anything the base image puts on PATH.
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}

# Minimal apt packages. No build-essential — cp313 wheels cover the
# common scientific stack (numpy, scipy, pandas, torch, numba). If a
# downstream capsule needs to compile a C extension, it can apt-install
# build-essential in its own postInstall.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      bzip2 ca-certificates curl git locales unzip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# uv binary from the Astral distroless image.
COPY --from=uv /uv /uvx /usr/local/bin/

# Install a managed Python 3.13 and create a dedicated venv at /opt/venv.
RUN uv python install 3.13 \
 && uv venv --python 3.13 ${VIRTUAL_ENV} \
 && rm -rf /root/.cache/uv \
 # Shadow any system python/pip so scripts that say `python3` or `pip`
 # resolve to the venv regardless of how they're invoked.
 && ln -sf ${VIRTUAL_ENV}/bin/python /usr/local/bin/python \
 && ln -sf ${VIRTUAL_ENV}/bin/python /usr/local/bin/python3 \
 && ln -sf ${VIRTUAL_ENV}/bin/pip /usr/local/bin/pip \
 && ln -sf ${VIRTUAL_ENV}/bin/pip /usr/local/bin/pip3
