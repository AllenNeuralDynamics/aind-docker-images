# Stage 1: get ffmpeg binaries
FROM docker.io/mwader/static-ffmpeg:9.0.2@sha256:7d9bdaaf887f7e6ce6151f67325c344074b5ff1fb75316011c3376503e449a7b AS ffmpeg

# Stage 2: get miniforge
FROM quay.io/condaforge/miniforge3:26.7.2-0@sha256:16eff7459a31bed2d395b1df0dca220c067a3a9527981ec87dbbde2eafe474e5 AS miniforge

# Stage 3: runtime
FROM public.ecr.aws/docker/library/ubuntu:26.04@sha256:f144425ff09be612d6d9ad965196e9cdc23dae1f42110a8a11a3e9a8198759f7

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
