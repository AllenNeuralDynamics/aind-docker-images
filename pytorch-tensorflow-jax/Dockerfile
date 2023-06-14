from allenneuraldynamics/cuda-miniconda-jupyterlab:cuda11-2.0
LABEL maintainer "David Feng <david.feng@alleninstitute.org>"

RUN conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia
RUN conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit && conda clean --all -y
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/:/opt/conda/lib/python3.10/site-packages/nvidia/cudnn/lib

RUN pip install -U --no-cache-dir tensorflow jax[cuda11_pip] -f https://storage.googleapis.com/jax-releases/jax_cuda_releases.html 


