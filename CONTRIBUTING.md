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

## Code Ocean registration

An image offered as a Code Ocean starter environment has an `image.yml` that
holds the fields of Code Ocean's registration form:

```yaml
starter_environment: true   # false keeps the file but skips registration
title: JAX JupyterLab
description: >-
  One or two sentences on what the image holds and who it is for.
tags: [Python, JAX, JupyterLab, CUDA 13, GPU]
key_packages: [jax]         # Python distributions or commands named in the version
language: Python            # Python, R, MATLAB or C/C++
gpu: true                   # Code Ocean machine type
```

Code Ocean groups an image's releases under its title and shows each one's
version in parentheses after it, so keep every version out of `title`, the CUDA
major and Python minor included, and never change it: a new title starts a new
environment. A new CUDA major or Python minor gets a new directory here but
registers as a new version under the same title.

The version is left out of `image.yml`, since it changes with every dependency
update. For the same reason, name a version in `description` or `tags` only
where changing it would mean a new image: the CUDA major and the Python minor.

To request a registration, run

```
uv run scripts/registration_request.py <image>...
```

It prints the form's fields for the image that `latest` points to, named by its
commit tag, since Code Ocean requires each deployed source to be unique. The
version lists the versions of `key_packages` that the image's `FROM` tags,
`requirements.txt` or `uv.lock` pin at that commit, then CUDA, Python and the
release month, which keeps it unique when nothing pinned has changed; an
unpinned package is left out.

## Recipes

Default to conda, since uv is not yet well integrated with Code Ocean: copy
Miniforge to `/opt/conda` and activate `base` in `.bashrc`, as `ubuntu-ffmpeg`
does. Use uv only for images whose users manage packages with uv themselves:
create a venv at `/opt/venv` and point `python`, `python3`, `pip` and `pip3` in
`/usr/local/bin` into it, as `python-slim-uv` does.

In every image:

- Copy tools in with `COPY --from=<pinned image>` rather than downloading
  installers: uv from `ghcr.io/astral-sh/uv`, Miniforge from
  `condaforge/miniforge3`, ffmpeg from `mwader/static-ffmpeg`. Never use
  Miniconda, whose default channel is under Anaconda's commercial terms.
- Pin every `FROM` to a version tag, so Dependabot can bump it.
- Install apt packages with `--no-install-recommends`, then remove
  `/var/lib/apt/lists`.
- If the image installs torch, jax or tensorflow, pin its Python packages in a
  `requirements.txt` beside the `Dockerfile`, so rebuilds reproduce it and bumps
  arrive as reviewable diffs.
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

There are no tests; build the image and run it.

```
docker build -t <image>:dev ./<image>
docker run --rm <image>:dev python -c "import sys; print(sys.version)"
docker run --rm --gpus all <image>:dev nvidia-smi   # needs a GPU and nvidia-container-toolkit
```
