FROM registry.codeocean.com/codeocean/pytorch:2.1.0-cuda11.8-mambaforge23.1.0-4-python3.10.12-ubuntu22.04

ARG CUDA_VERSION=12.4.0
ARG TORCH_VERSION=2.4.0
ARG TORCHVISION_VERSION=0.19.0

RUN mamba install -c pytorch -y \
   cuda=${CUDA_VERSION} \
   cuda-toolkit=${CUDA_VERSION} \
   pytorch==${TORCH_VERSION} \
   pytorch-cuda=${CUDA_VERSION} \
   torchaudio==${TORCH_VERSION} \
   torchvision==${TORCHVISION_VERSION} \
   && mamba clean -ya

ENV CUDA_HOME=${CONDA_DIR}
ENV CUDA_DIR=${CUDA_HOME}
ENV XLA_FLAGS="--xla_gpu_cuda_data_dir=${CUDA_HOME}"
ENV LD_LIBRARY_PATH="$CUDA_HOME/lib:$LD_LIBRARY_PATH"