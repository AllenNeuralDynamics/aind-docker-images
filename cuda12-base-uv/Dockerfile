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
# libraries under site-packages/nvidia/*/lib and don't link the system
# copies. Caveat: torch RPATHs those bundled libs so they load with no
# config, but tensorflow/jax do NOT — on a bare base they fail to dlopen
# their CUDA libs and silently fall back to CPU. This image therefore puts
# the wheel lib dirs on LD_LIBRARY_PATH (see the ENV near the end) so TF/JAX
# find them too. If you need system cuBLAS/cuDNN/NCCL (rare in modern Python
# ML stacks), use cuda12-runtime-uv instead.
#
# CUDA version: the framework wheels bundle their own CUDA userspace
# (tensorflow[and-cuda] 2.21 -> CUDA 12.9 / cuDNN 9; torch -> cu126..cu130),
# so the base CUDA below is NOT what they run against — it mainly sets the
# host-driver floor via NVIDIA_REQUIRE_CUDA. Keep it conservative (12.8) for
# the widest driver compatibility; bumping to 13.x would only raise that floor
# with no payoff for wheel-based capsules — and CUDA 13 drops Volta, so it would
# also break any V100 host (T4/Turing and newer are unaffected).
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

# Make the pip-wheel CUDA libs discoverable. tensorflow[and-cuda]/jax install
# their CUDA userspace as nvidia-*-cu12 wheels under nvidia/*/lib but (unlike
# torch) don't RPATH them, so TF/JAX can't dlopen them and fall back to CPU.
# Putting the wheel lib dirs on LD_LIBRARY_PATH fixes that for every execution
# context (reproducible run, pipeline node, AND interactive workstation shell) —
# a per-capsule code/run shim would miss the workstation case. Entries are
# skipped by the loader until a capsule actually installs the wheels.
# NOTE: hardcodes the cp313 site-packages path; update the python3.13 segment
# if the base interpreter version changes. The system driver libs the CUDA base
# image puts on LD_LIBRARY_PATH are preserved by the trailing ${LD_LIBRARY_PATH}.
ARG NVLIB=/opt/venv/lib/python3.13/site-packages/nvidia
ENV LD_LIBRARY_PATH=${NVLIB}/cublas/lib:${NVLIB}/cuda_cupti/lib:${NVLIB}/cuda_nvrtc/lib:${NVLIB}/cuda_runtime/lib:${NVLIB}/cudnn/lib:${NVLIB}/cufft/lib:${NVLIB}/curand/lib:${NVLIB}/cusolver/lib:${NVLIB}/cusparse/lib:${NVLIB}/cusparselt/lib:${NVLIB}/nccl/lib:${NVLIB}/nvjitlink/lib:${NVLIB}/nvtx/lib:${LD_LIBRARY_PATH}
