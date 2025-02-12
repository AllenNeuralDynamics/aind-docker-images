FROM rocker/r2u:22.04

RUN wget --no-verbose https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2024.12.0-467-amd64.deb  \
        && apt-get update \
        && apt-get install -y --no-install-recommends ./rstudio-server-2024.12.0-467-amd64.deb 
