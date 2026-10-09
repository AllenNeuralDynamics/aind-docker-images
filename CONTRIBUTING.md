# Contributing

Each top-level directory with a `Dockerfile` is one image, published as
`ghcr.io/allenneuraldynamics/<directory>`. Every `FROM` names a public upstream
image; no image builds on another from this repository.

## Publishing

On a push to `main`, `.github/workflows/publish_images.yml` rebuilds each
changed image and tags it `<short-sha>` and `latest`. To rebuild an unchanged
image, run that workflow with `image_name`, and check `publish_latest` to move
`latest` as well. `aind-airflow` and `hortacloud-deployment` publish through
their own workflows, which bump the `# vX.Y.Z` comment on line 1 of the
`Dockerfile` first.

To add an image, create its directory, list it under `docker` in
`.github/dependabot.yml`, and give it an owner in `.github/CODEOWNERS`. Do not
add a workflow.

## Recipes

Default to conda, since uv is not yet well integrated with Code Ocean: copy
Miniforge to `/opt/conda` and activate `base` in `.bashrc`, as `ubuntu-ffmpeg`
does. Use uv only for images whose users manage packages with uv themselves:
create a venv at `/opt/venv` and point `python`, `python3`, `pip` and `pip3` in
`/usr/local/bin` into it, as `python-slim-uv` does.

In every image:

- Copy tools in with `COPY --from=<pinned image>` rather than downloading
  installers: uv from `ghcr.io/astral-sh/uv`, Miniforge from
  `quay.io/condaforge/miniforge3`, ffmpeg from `mwader/static-ffmpeg`. Never use
  Miniconda, whose default channel is under Anaconda's commercial terms.
- Avoid Docker Hub where an image has another registry: `nvcr.io/nvidia/cuda`,
  `quay.io/condaforge/miniforge3`, and `public.ecr.aws/docker/library/` for
  Docker's official images. Docker Hub rate-limits anonymous pulls, and CI and
  Dependabot pull anonymously.
- Pin every `FROM` to a version tag and its digest (`image:tag@sha256:...`).
  Upstreams rebuild tags in place, so only the digest fixes what a rebuild
  gets; Dependabot bumps both.
- Install apt packages with `--no-install-recommends`, then remove
  `/var/lib/apt/lists`.
- If the image installs Python packages, list its direct dependencies in a
  `pyproject.toml` beside the `Dockerfile` as lower bounds (`torch>=2.14.1`),
  commit the `uv.lock` that `uv lock` writes, and install the lock with hashes
  into the conda environment, as `jax-jupyterlab` does. conda installs only the
  interpreter. Rebuilds then reproduce the whole tree. Dependabot groups minor
  and patch updates into one PR and opens a separate PR for each major. Leave
  apt packages unpinned: Ubuntu drops superseded versions, so pins break the
  build.
- Open the `Dockerfile` with a comment saying what the image is for and why its
  base was chosen, and keep it current.
- Set the OCI labels `org.opencontainers.image.source`, `.description` and
  `.licenses`, and write `ENV KEY=value`.
- Leave `MPLBACKEND` unset. Matplotlib falls back to Agg without a display, and
  a set value stops Jupyter kernels, Code Ocean's JupyterLab included, from
  plotting inline.

## CUDA

Build GPU images on the NVIDIA `base` variant (`nvidia/cuda:*-base-*`). pytorch,
jax and cupy wheels and conda-forge's CUDA packages bring their own CUDA
libraries, so the image's CUDA version only sets the driver check at container
start. A capsule that needs another CUDA library can install its `nvidia-*-cu13`
pip package.

Target CUDA 13 on Ubuntu 26.04 for GPU images. CUDA 13 needs compute capability
7.5 or newer (T4 and later), which Code Ocean's default GPU machines meet;
`NVIDIA_REQUIRE_CUDA` in the NVIDIA base image lists the host drivers that pass
that check. Check a machine with
`nvidia-smi --query-gpu=name,driver_version,compute_cap --format=csv`.

Set `ENV NVIDIA_DRIVER_CAPABILITIES=compute,video,utility`. The NVIDIA base
images mount only `compute` and `utility`, so without `video` GPU video decoding
and encoding fail for lack of the driver's NVDEC and NVENC libraries.

Give a new CUDA major a new directory, since image names encode it; Dependabot
skips `nvidia/cuda` majors for that reason.

Never touch the GPU at build time: the host driver is mounted only when a
container starts with a GPU.

## Testing

A Code Ocean image has a `test.sh` that runs inside the built image and checks
what a capsule relies on: the interpreter and environment, the bundled tools,
and for a GPU framework image, that the framework is its CUDA build. On a pull
request, `.github/workflows/test_images.yml` builds every changed image and runs
its `test.sh`. Hosted runners have no GPU, so check a GPU image on a GPU machine
before merging a change to its CUDA or framework versions.

```
docker build -t <image>:dev ./<image>
docker run --rm -i <image>:dev bash -s < <image>/test.sh
docker run --rm --gpus all <image>:dev nvidia-smi   # needs a GPU and nvidia-container-toolkit
```
