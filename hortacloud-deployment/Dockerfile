from node:16

RUN apt-get update 

RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install
RUN rm awscliv2.zip

RUN npm install -g aws-cdk

RUN git clone https://github.com/JaneliaSciComp/hortacloud/
WORKDIR /hortacloud
ADD .env .
