from allenneuraldynamics/cuda-miniconda-jupyterlab:cuda11-2.0
LABEL maintainer "David Feng <david.feng@alleninstitute.org>"

RUN pip install -U --extra-index-url https://developer.download.nvidia.com/compute/redist --upgrade nvidia-dali-cuda110

RUN pip install -U --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118 

RUN pip install -U --no-cache-dir lightning tensorboard lightning-bolts 

ENV NVIDIA_DRIVER_CAPABILITIES compute,video,utility