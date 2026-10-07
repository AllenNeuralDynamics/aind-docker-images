# JupyterLab with TensorFlow, on NVIDIA CUDA 13 `base` + Miniforge
# (conda-forge).
#
# Python packages are pinned in requirements.txt. tensorflow[and-cuda]
# wheels bundle their own CUDA 12 libraries, which the host's CUDA 13
# driver runs, so the `base` variant suffices. CUDA 13 needs compute
# capability >=7.5 (T4 and newer); NVIDIA_REQUIRE_CUDA in the base image
# lists the host drivers that pass the check at container start.

# Stage 1: a ready-made /opt/conda, copied into the runtime stage.
FROM docker.io/condaforge/miniforge3:26.7.2-0 AS miniforge

# Stage 2: runtime
FROM docker.io/nvidia/cuda:13.4.2-base-ubuntu26.04

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
RUN conda install -y python=3.13 jupyterlab notebook \
 && conda clean -afy \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> /etc/skel/.bashrc \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> ~/.bashrc

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

# tensorflow 2.21 dlopens libcusolver.so.11 from a library whose RUNPATH
# omits nvidia/cusolver/lib, so without this it silently runs on CPU.
ENV LD_LIBRARY_PATH=${CONDA_DIR}/lib/python3.13/site-packages/nvidia/cusolver/lib:${LD_LIBRARY_PATH}
