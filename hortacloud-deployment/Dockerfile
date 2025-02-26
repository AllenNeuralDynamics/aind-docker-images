from node:18

RUN apt-get update && \
    apt-get install -y less

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm awscliv2.zip

RUN npm install -g aws-cdk

RUN mkdir /horta_build
