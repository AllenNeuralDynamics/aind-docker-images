# Minimal base: NVIDIA CUDA 12 runtime + uv-managed Python 3.13.
# No conda, no ML framework, no notebook server baked in — add what
# you need in your capsule.
#
# Variant: `runtime` — ships the full CUDA userspace (libcudart,
# libcublas, libcufft, libcurand, libcusparse, NCCL, cuDNN) for CUDA
# workloads that use the *system* libs (cupy, rapids, or a plain
# `tensorflow` without [and-cuda]). For the smaller driver-stub variant —
# right for torch and other wheels that bundle their own CUDA — use
# cuda12-base-uv.
#
# Caveat: capsules that install tensorflow[and-cuda] / jax pull their OWN
# nvidia-*-cu12 CUDA wheels even on this image, and those wheels (unlike
# torch) aren't RPATH'd — so this image also puts the wheel lib dirs on
# LD_LIBRARY_PATH (see the ENV near the end). Without it those capsules
# dlopen-fail and silently fall back to CPU despite the system libs.
#
# CUDA version: keep conservative (12.8) — the bundled framework wheels carry
# their own CUDA (tensorflow[and-cuda] 2.21 -> CUDA 12.9 / cuDNN 9; torch ->
# cu126..cu130), and the base CUDA mainly sets the NVIDIA_REQUIRE_CUDA
# host-driver floor; bumping to 13.x just raises that floor and drops Volta, so
# it would break V100 hosts (T4/Turing and newer are unaffected).
#
# GPU availability is a deployment-time concern: the image includes
# CUDA userspace libs but the host driver is bind-mounted by
# nvidia-container-toolkit only when the container is run with --gpus
# (on Code Ocean, controlled by the capsule's machine type).

# Stage 1: uv binary, pulled from Astral's distroless image.
FROM ghcr.io/astral-sh/uv:0.11.7 AS uv

# Stage 2: runtime on CUDA 12.8 / Ubuntu 24.04
FROM docker.io/nvidia/cuda:12.8.1-runtime-ubuntu24.04

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="CUDA 12.8 runtime (cuBLAS/cuDNN/NCCL) + uv-managed Python 3.13. Minimal base for GPU-enabled AIND capsules."
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive
# Matplotlib default: headless-safe for reproducible runs.
ENV MPLBACKEND=Agg
ENV VIRTUAL_ENV=/opt/venv
# /opt/venv/bin wins over anything the base image puts on PATH.
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}

# uv ergonomics — these affect a capsule's `uv pip install` in postInstall (CO's
# UI installs use plain pip, which these don't touch) and this image's own build:
#   - copy link mode: silences "failed to hardlink, falling back to copy" when the
#     uv cache and venv live on different layers/mounts.
#   - bytecode precompile: write .pyc at install time -> faster first import on
#     reproducible-run / pipeline cold starts.
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

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

# Now that the managed interpreter + venv exist, forbid uv from downloading
# ANOTHER Python in a capsule's postInstall / interactive use — always reuse
# /opt/venv. Set AFTER the `uv python install` above, which legitimately needs
# to download the interpreter.
ENV UV_PYTHON_DOWNLOADS=never

# Make pip-wheel CUDA libs discoverable for tensorflow[and-cuda]/jax capsules.
# Even on this runtime variant (which ships system CUDA), those frameworks pull
# their own nvidia-*-cu12 wheels under nvidia/*/lib and, unlike torch, don't
# RPATH them — so without this they dlopen-fail and fall back to CPU. Putting the
# wheel lib dirs on LD_LIBRARY_PATH fixes every execution context (run, pipeline,
# interactive shell). Dirs are skipped by the loader until a capsule installs the
# wheels; plain (system-lib) capsules that install no nvidia wheels are unaffected
# and keep using the system CUDA via the preserved trailing ${LD_LIBRARY_PATH}.
# NOTE: hardcodes the cp313 site-packages path; update python3.13 if it changes.
ARG NVLIB=/opt/venv/lib/python3.13/site-packages/nvidia
ENV LD_LIBRARY_PATH=${NVLIB}/cublas/lib:${NVLIB}/cuda_cupti/lib:${NVLIB}/cuda_nvrtc/lib:${NVLIB}/cuda_runtime/lib:${NVLIB}/cudnn/lib:${NVLIB}/cufft/lib:${NVLIB}/curand/lib:${NVLIB}/cusolver/lib:${NVLIB}/cusparse/lib:${NVLIB}/cusparselt/lib:${NVLIB}/nccl/lib:${NVLIB}/nvjitlink/lib:${NVLIB}/nvtx/lib:${LD_LIBRARY_PATH}
