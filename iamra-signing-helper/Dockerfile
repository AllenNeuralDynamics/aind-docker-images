FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
RUN curl -o /aws_signing_helper https://rolesanywhere.amazonaws.com/releases/1.1.1/X86_64/Linux/aws_signing_helper \
    && chmod +x /aws_signing_helper
RUN mkdir -p /iamra

WORKDIR /app
COPY init.sh ./
RUN chmod +x init.sh

CMD ["./init.sh"]
