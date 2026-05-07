# Minimal CPU-only base: python:3.13-slim-trixie + uv.
# No conda, no ML framework, no notebook server baked in — add what
# you need in your capsule.
#
# Debian slim rather than Ubuntu because:
# - ~150 MB smaller than ubuntu:24.04 + uv-install-python, which pays
#   back on every Code Ocean pipeline cold start.
# - Python 3.13 is already installed by the upstream official image;
#   no build-time download via `uv python install`.
# - apt package names and system dependencies are effectively identical
#   to Ubuntu for the packages a capsule actually installs (build-essential,
#   libgl1, libglib2.0-0, ffmpeg, etc.). PPAs are the main thing that
#   won't work, but pipeline capsules don't use PPAs.
#
# For GPU-capable roles use cuda12-runtime-uv or cuda12-base-uv.

# Stage 1: uv binary, pulled from Astral's distroless image.
FROM ghcr.io/astral-sh/uv:0.11.11 AS uv

# Stage 2: Docker Official Python image, Debian trixie slim.
FROM docker.io/python:3.14-slim-trixie

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="python:3.13-slim-trixie + uv. Minimal CPU-only base for AIND capsules."
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive
# Matplotlib default: headless-safe for reproducible runs.
ENV MPLBACKEND=Agg
ENV VIRTUAL_ENV=/opt/venv
# /opt/venv/bin wins over anything the base image puts on PATH.
ENV PATH=${VIRTUAL_ENV}/bin:${PATH}

# Minimal apt packages. No build-essential — cp313 wheels cover the
# common scientific stack (numpy, scipy, pandas, numba). If a
# downstream capsule needs to compile a C extension, it can apt-install
# build-essential in its own postInstall.
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      bzip2 ca-certificates curl git locales unzip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

# uv binary from the Astral distroless image.
COPY --from=uv /uv /uvx /usr/local/bin/

# Create a dedicated venv at /opt/venv using the base image's Python 3.13
# (no `uv python install` — the official python:3.13-slim-trixie image
# already provides the exact interpreter we want).
# `--seed` installs pip into the venv so `/opt/venv/bin/pip` exists (and so
# Code Ocean's GUI recognises pip as available).
RUN uv venv --seed --python python3.13 ${VIRTUAL_ENV} \
 && rm -rf /root/.cache/uv \
 # Shadow python/pip into the venv. python: wrapper, not symlink — a plain
 # symlink leaves sys.executable=/usr/local/bin/python, so CPython's
 # pyvenv.cfg lookup walks /usr/local and misses /opt/venv. The re-exec
 # puts sys.executable inside /opt/venv so activation fires. pip/pip3: a
 # symlink is fine because pip is itself a shebang script that re-execs.
 # `rm -f` first: the slim-trixie base ships python/python3 as symlinks
 # to python3.13; writing through them would clobber the real interpreter.
 && rm -f /usr/local/bin/python /usr/local/bin/python3 \
 && printf '#!/bin/sh\nexec /opt/venv/bin/python "$@"\n' > /usr/local/bin/python \
 && chmod +x /usr/local/bin/python \
 && ln -sf python /usr/local/bin/python3 \
 && ln -sf ${VIRTUAL_ENV}/bin/pip /usr/local/bin/pip \
 && ln -sf ${VIRTUAL_ENV}/bin/pip /usr/local/bin/pip3
