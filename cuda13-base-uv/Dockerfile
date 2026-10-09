# Minimal base: NVIDIA CUDA 13 `base` variant + uv-managed Python 3.13.
# No conda, no ML framework, no notebook server baked in — add what
# you need in your capsule.
#
# Variant: `base` — ships libcudart and the CUDA env vars, but no
# cuBLAS, cuFFT, cuRAND, cuSPARSE, NCCL or cuDNN; about 2 GB smaller
# than `runtime`. pytorch, jax, cupy and tensorflow wheels bundle their
# own CUDA libraries, and a capsule that needs another one can install
# its nvidia-*-cu13 pip package.
#
# CUDA 13 needs compute capability >=7.5 (T4 and newer);
# NVIDIA_REQUIRE_CUDA in the base image lists the host drivers that pass
# the check at container start.
#
# GPU availability is a deployment-time concern: the host driver is
# bind-mounted by nvidia-container-toolkit only when the container is
# run with --gpus (on Code Ocean, controlled by the capsule's machine
# type).

# Stage 1: uv binary, pulled from Astral's distroless image.
FROM ghcr.io/astral-sh/uv:0.12.23@sha256:61d393e44e249f2e4b526b6c7ddcecce245946826e608e11c93ad4f5bba55b21 AS uv

# Stage 2: `base` on CUDA 13.4 / Ubuntu 26.04
FROM nvcr.io/nvidia/cuda:13.4.2-base-ubuntu26.04@sha256:ac2289b83fba0b38cddf6513f3703d132135ae070cc1b7c63234b90dca4c60f2

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="CUDA 13.4 base + uv-managed Python 3.13. Minimal GPU base for AIND capsules that install pytorch/jax/cupy via pip."
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive
ENV VIRTUAL_ENV=/opt/venv
# /opt/venv/bin wins over anything the base image puts on PATH.
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}
# Hardlinking fails wherever the uv cache is mounted apart from the venv;
# copy without uv's warning on every install.
ENV UV_LINK_MODE=copy
# The base image mounts only compute and utility; video adds NVDEC/NVENC.
ENV NVIDIA_DRIVER_CAPABILITIES=compute,video,utility

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
