# v0.0.1
from node:16

RUN apt-get update && \
    apt-get install -y less

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm awscliv2.zip

RUN npm install -g aws-cdk
