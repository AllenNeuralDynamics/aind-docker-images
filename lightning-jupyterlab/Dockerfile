from allenneuraldynamics/cuda-miniconda-jupyterlab:cuda12-1.0
LABEL maintainer "David Feng <david.feng@alleninstitute.org>"

RUN pip install -U --extra-index-url https://developer.download.nvidia.com/compute/redist --upgrade nvidia-dali-cuda120

RUN pip install -U --no-cache-dir lightning tensorboard lightning-bolts torchtyping torchvision

ENV NVIDIA_DRIVER_CAPABILITIES compute,video,utility