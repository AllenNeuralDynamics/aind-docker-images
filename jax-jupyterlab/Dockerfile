# JupyterLab with JAX, on NVIDIA CUDA 13 `base` + Miniforge (conda-forge).
#
# Python packages are locked in uv.lock. jax[cuda13] wheels
# bundle their own CUDA 13 libraries, so the `base` variant suffices.
# CUDA 13 needs compute capability >=7.5 (T4 and newer);
# NVIDIA_REQUIRE_CUDA in the base image lists the host drivers that pass
# the check at container start.

# Stage 1: uv, mounted only while installing the locked packages.
FROM ghcr.io/astral-sh/uv:0.13.8@sha256:5cc1805e2426484abca4ad46ea783bab281fdb225fd82d8ce6d66a81254bac85 AS uv

# Stage 2: a ready-made /opt/conda, copied into the runtime stage.
FROM quay.io/condaforge/miniforge3:26.9.4-2@sha256:dd37613f34cef9ff9953667e83ec743851499db51ed641911e12b860b2e439b5 AS miniforge

# Stage 3: runtime
FROM nvcr.io/nvidia/cuda:13.5.0-base-ubuntu26.04@sha256:2b8fc7b402eb045b809c3bb6296853e7d6e99a5acaded62b28f9494b357fbb4f

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="CUDA 13.4 base + Miniforge + JupyterLab, with JAX."
LABEL org.opencontainers.image.licenses="MIT"

ENV DEBIAN_FRONTEND=noninteractive
ENV CONDA_DIR=/opt/conda
ENV PATH=${CONDA_DIR}/bin:${PATH}
# The base image mounts only compute and utility; video adds NVDEC/NVENC.
ENV NVIDIA_DRIVER_CAPABILITIES=compute,video,utility

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      bzip2 ca-certificates curl git locales unzip \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

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
