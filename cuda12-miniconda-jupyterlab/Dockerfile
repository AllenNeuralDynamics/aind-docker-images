FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04
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
    
ARG MINICONDA_INSTALLER=Miniconda3-py310_23.1.0-1-Linux-x86_64.sh
ARG MINICONDA_SHA256=32d73e1bc33fda089d7cd9ef4c1be542616bd8e437d1f77afeeaf7afdb019787
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

