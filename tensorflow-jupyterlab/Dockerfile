# JupyterLab with TensorFlow, on NVIDIA CUDA 13 `base` + Miniforge
# (conda-forge).
#
# Python packages are locked in uv.lock. tensorflow[and-cuda]
# wheels bundle their own CUDA 12 libraries, which the host's CUDA 13
# driver runs, so the `base` variant suffices. CUDA 13 needs compute
# capability >=7.5 (T4 and newer); NVIDIA_REQUIRE_CUDA in the base image
# lists the host drivers that pass the check at container start.

# Stage 1: uv, mounted only while installing the locked packages.
FROM ghcr.io/astral-sh/uv:0.13.6@sha256:af22a52f5eafef3d78e551599d405c02df61919d18028f0cea8eda93bc9986d0 AS uv

# Stage 2: a ready-made /opt/conda, copied into the runtime stage.
FROM quay.io/condaforge/miniforge3:26.9.4-0@sha256:0a0bbf068fc591c719d7594f513cc0f2411988b1f6bddcdfa2095584585873f6 AS miniforge

# Stage 3: runtime
FROM nvcr.io/nvidia/cuda:13.4.3-base-ubuntu26.04@sha256:e2eb43e25d404e2c48716f80afdb8989a84c4da588f5509330322842084d97b0

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="CUDA 13.4 base + Miniforge + JupyterLab, with TensorFlow."
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
RUN conda install -y python=3.13 \
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

# tensorflow 2.21 dlopens libcusolver.so.11 from a library whose RUNPATH
# omits nvidia/cusolver/lib, so without this it silently runs on CPU.
ENV LD_LIBRARY_PATH=${CONDA_DIR}/lib/python3.13/site-packages/nvidia/cusolver/lib:${LD_LIBRARY_PATH}
