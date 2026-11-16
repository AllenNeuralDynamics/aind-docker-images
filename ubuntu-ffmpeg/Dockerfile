# Stage 1: get ffmpeg binaries
FROM docker.io/mwader/static-ffmpeg:9.0.2-1@sha256:f5d100184884eb3e82b0eb14bb5ebf98da99826ac824989720297fb9ef21c822 AS ffmpeg

# Stage 2: get miniforge
FROM quay.io/condaforge/miniforge3:26.9.4-2@sha256:dd37613f34cef9ff9953667e83ec743851499db51ed641911e12b860b2e439b5 AS miniforge

# Stage 3: runtime
FROM public.ecr.aws/docker/library/ubuntu:26.04@sha256:c098726dd9b9733f3e885f8de0ef375206a311b0a317eadc40d347b1115fb944

ENV CONDA_DIR=/opt/conda
ENV PATH=${CONDA_DIR}/bin:${PATH}

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential bzip2 ca-certificates curl git gnupg2 locales unzip \
 && rm -rf /var/lib/apt/lists/*

# Miniforge3 (conda + mamba, conda-forge channel)
COPY --from=miniforge ${CONDA_DIR} ${CONDA_DIR}
# Pin conda to the Miniforge release so that swapping Python does not upgrade it.
RUN echo "conda ==$(conda --version | cut -d' ' -f2)" >> ${CONDA_DIR}/conda-meta/pinned \
 && conda install -y python=3.13 \
 && conda clean -afy \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> /etc/skel/.bashrc \
 && echo ". ${CONDA_DIR}/etc/profile.d/conda.sh && conda activate base" >> ~/.bashrc

# ffmpeg/ffprobe
COPY --from=ffmpeg /ffmpeg /usr/local/bin/ffmpeg
COPY --from=ffmpeg /ffprobe /usr/local/bin/ffprobe
