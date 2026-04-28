# Minimal base: NVIDIA CUDA 12 `base` variant + uv-managed Python 3.13.
# No conda, no ML framework, no notebook server baked in — add what
# you need in your capsule.
#
# Variant: `base` — ships only the CUDA driver stub (libcuda.so) and
# env vars; no libcudart/libcublas/libcufft/libcurand/libcusparse/NCCL/
# cuDNN. ~2.3 GB smaller than the `runtime` variant.
#
# Use this when the downstream capsule installs pytorch (or tensorflow,
# jax, cupy) via pip/uv — those wheels bundle their own CUDA runtime
# libraries and don't link against the system copies. If you need
# system cuBLAS/cuDNN/NCCL (rare in modern Python ML stacks), use
# cuda12-runtime-uv instead.
#
# GPU availability is a deployment-time concern: the host driver is
# bind-mounted by nvidia-container-toolkit only when the container is
# run with --gpus (on Code Ocean, controlled by the capsule's machine
# type).

# Stage 1: uv binary, pulled from Astral's distroless image.
FROM ghcr.io/astral-sh/uv:0.11.7 AS uv

# Stage 2: `base` on CUDA 12.8 / Ubuntu 24.04
FROM docker.io/nvidia/cuda:12.8.1-base-ubuntu24.04

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="CUDA 12.8 base (driver stub only) + uv-managed Python 3.13. Minimal GPU base for AIND capsules that install pytorch/jax/cupy via pip."
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
# `--seed` installs pip into the venv so `/opt/venv/bin/pip` exists (and so
# Code Ocean's GUI recognises pip as available).
RUN uv python install 3.13 \
 && uv venv --seed --python 3.13 ${VIRTUAL_ENV} \
 && rm -rf /root/.cache/uv \
 # Shadow python/pip into the venv. python: wrapper, not symlink — a plain
 # symlink leaves sys.executable=/usr/local/bin/python, so CPython's
 # pyvenv.cfg lookup walks /usr/local and misses /opt/venv. The re-exec
 # puts sys.executable inside /opt/venv so activation fires. pip/pip3: a
 # symlink is fine because pip is itself a shebang script that re-execs.
 # `rm -f` is a no-op on this image but guards against future base images
 # that (like python:3.13-slim) ship python/python3 as symlinks to python3.13.
 && rm -f /usr/local/bin/python /usr/local/bin/python3 \
 && printf '#!/bin/sh\nexec /opt/venv/bin/python "$@"\n' > /usr/local/bin/python \
 && chmod +x /usr/local/bin/python \
 && ln -sf python /usr/local/bin/python3 \
 && ln -sf ${VIRTUAL_ENV}/bin/pip /usr/local/bin/pip \
 && ln -sf ${VIRTUAL_ENV}/bin/pip /usr/local/bin/pip3
