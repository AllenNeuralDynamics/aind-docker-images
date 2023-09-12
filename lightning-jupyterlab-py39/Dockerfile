FROM nvidia/cuda:11.8.0-runtime-ubuntu22.04
LABEL maintainer "David Feng <david.feng@alleninstitute.org>"

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      bzip2 \
      ca-certificates \
      curl \
      git \
      gnupg2 \
      less \
      locales \
      nano \
      unzip \
    && rm -rf /var/lib/apt/lists/*
    
ARG MINICONDA_INSTALLER=Miniconda3-py39_23.5.2-0-Linux-x86_64.sh
ARG MINICONDA_SHA256=9829d95f639bd0053b2ed06d1204e60644617bf37dd5cc57523732e0e8d64516
ARG CONDA_DIR=/opt/conda

RUN curl -O https://repo.anaconda.com/miniconda/${MINICONDA_INSTALLER} \
  && echo "$MINICONDA_SHA256  $MINICONDA_INSTALLER" | sha256sum -c \
  && bash ${MINICONDA_INSTALLER} -b -p ${CONDA_DIR} \
  && rm ${MINICONDA_INSTALLER} \
  && ${CONDA_DIR}/bin/conda clean --all -f -y \
  && ln -s "${CONDA_DIR}/etc/profile.d/conda.sh" /etc/profile.d/conda.sh \
  && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh" >> ~/.bashrc \
  && echo "conda activate base" >> ~/.bashrc

ENV MPLBACKEND Agg
ENV PATH "${CONDA_DIR}/bin:$PATH"

# Turn off conda auto update and show channel URLs
RUN conda config --system --set auto_update_conda false \
  && conda config --system --set show_channel_urls true

RUN pip install -U --no-cache-dir jupyterlab jupyter notebook

RUN pip install -U --no-cache-dir --extra-index-url https://developer.download.nvidia.com/compute/redist --upgrade nvidia-dali-cuda110

RUN pip install -U --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 

RUN pip install -U --no-cache-dir lightning tensorboard lightning-bolts 

ENV NVIDIA_DRIVER_CAPABILITIES compute,video,utility