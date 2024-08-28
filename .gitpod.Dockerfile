FROM gitpod/workspace-full

# Install Docker
USER root

RUN apt-get update && \
    apt-get install -y docker.io docker-compose && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER gitpod
