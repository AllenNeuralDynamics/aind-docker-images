# Stage 1: get ffmpeg binaries
FROM docker.io/mwader/static-ffmpeg:8.0.1 AS ffmpeg

# Stage 2: get miniforge
FROM docker.io/condaforge/miniforge3:25.11.0-1 AS miniforge

# Stage 3: runtime
FROM docker.io/ubuntu:24.04

ENV CONDA_DIR=/opt/conda
ENV PATH=${CONDA_DIR}/bin:${PATH}

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential bzip2 ca-certificates curl git gnupg2 locales unzip \
 && rm -rf /var/lib/apt/lists/*

# Miniforge3 (conda + mamba, conda-forge channel)
COPY --from=miniforge ${CONDA_DIR} ${CONDA_DIR}
RUN conda install -y python=3.13 \
 && conda clean -afy \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> /etc/skel/.bashrc \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> ~/.bashrc

# ffmpeg/ffprobe
COPY --from=ffmpeg /ffmpeg /usr/local/bin/ffmpeg
COPY --from=ffmpeg /ffprobe /usr/local/bin/ffprobe
