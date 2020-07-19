FROM ubuntu:18.04 AS builder
WORKDIR /project
RUN apt-get update -q && DEBIAN_FRONTEND=noninteractive \
    apt-get install -q -y cmake git vim gcc g++ software-properties-common && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Installing latest GCC compiler (version 10) for best vectorization
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update -q && \
    apt-get install -q -y gcc-10 g++-10 gfortran-10 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-10 90\
                        --slave /usr/bin/g++ g++ /usr/bin/g++-10\
                        --slave /usr/bin/gfortran gfortran /usr/bin/gfortran-10\
                        --slave /usr/bin/gcov gcov /usr/bin/gcov-10

SHELL ["/bin/bash", "-c"]

RUN groupadd chapter9 && useradd -m -s /bin/bash -g chapter9 chapter9

WORKDIR /home/chapter9
RUN chown -R chapter9:chapter9 /home/chapter9
USER chapter9

RUN git clone --recursive https://github.com/essentialsofparallelcomputing/Chapter9.git

ENTRYPOINT ["bash"]
