from allenneuraldynamics/cuda-miniconda-jupyterlab:cuda11-1.0
LABEL maintainer "David Feng <david.feng@alleninstitute.org>"

RUN pip install -U --no-cache-dir tensorflow jax[cuda11_pip] -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html lightning lightning-bolts torchtyping torchvision
RUN conda install cudatoolkit && conda clean --all -y
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/:/opt/conda/lib/python3.10/site-packages/nvidia/cudnn/lib

