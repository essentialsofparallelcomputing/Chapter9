FROM ubuntu:18.04 AS builder
WORKDIR /project
RUN apt-get update && \
    apt-get install -y bash cmake git vim gcc apt-utils && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

SHELL ["/bin/bash", "-c"]

RUN groupadd -r chapter10 && useradd -r -s /bin/false -g chapter10 chapter10

WORKDIR /chapter10
RUN chown -R chapter10:chapter10 /chapter10
USER chapter10

RUN git clone --recursive https://github.com/essentialsofparallelcomputing/Chapter9.git

ENTRYPOINT ["bash"]
