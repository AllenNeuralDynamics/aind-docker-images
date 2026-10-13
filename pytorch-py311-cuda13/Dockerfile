# JupyterLab with PyTorch on Python 3.11, for capsules whose dependencies
# do not yet support newer Python; otherwise use lightning-jupyterlab.
# Built on NVIDIA CUDA 13 `base` + Miniforge (conda-forge).
#
# Python packages are pinned in requirements.txt. torch wheels from PyPI
# bundle their own CUDA 13 libraries, so the `base` variant suffices.
# CUDA 13 needs compute capability >=7.5 (T4 and newer);
# NVIDIA_REQUIRE_CUDA in the base image lists the host drivers that pass
# the check at container start.

# Stage 1: a ready-made /opt/conda, copied into the runtime stage.
FROM quay.io/condaforge/miniforge3:26.7.2-0@sha256:16eff7459a31bed2d395b1df0dca220c067a3a9527981ec87dbbde2eafe474e5 AS miniforge

# Stage 2: runtime
FROM nvcr.io/nvidia/cuda:13.4.2-base-ubuntu26.04@sha256:ac2289b83fba0b38cddf6513f3703d132135ae070cc1b7c63234b90dca4c60f2

LABEL org.opencontainers.image.source="https://github.com/AllenNeuralDynamics/aind-docker-images"
LABEL org.opencontainers.image.description="CUDA 13 base + Miniforge + JupyterLab, with PyTorch on Python 3.11."
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
RUN conda install -y python=3.11 jupyterlab notebook \
 && conda clean -afy \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> /etc/skel/.bashrc \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> ~/.bashrc

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt
