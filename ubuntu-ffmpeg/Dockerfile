# Stage 1: get ffmpeg binaries
FROM docker.io/mwader/static-ffmpeg:9.0.2-1@sha256:f5d100184884eb3e82b0eb14bb5ebf98da99826ac824989720297fb9ef21c822 AS ffmpeg

# Stage 2: get miniforge
FROM quay.io/condaforge/miniforge3:26.9.4-0@sha256:0a0bbf068fc591c719d7594f513cc0f2411988b1f6bddcdfa2095584585873f6 AS miniforge

# Stage 3: runtime
FROM public.ecr.aws/docker/library/ubuntu:26.04@sha256:0e73b71479e7bc5f006bca872e25c3cd680dc052a0116f90d63ae363537db0dd

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
