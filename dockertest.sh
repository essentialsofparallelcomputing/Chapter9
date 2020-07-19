#!/bin/sh
docker build --no-cache -t chapter9 .
#docker run -it --entrypoint /bin/bash chapter9
docker build --no-cache -f Dockerfile.Ubuntu20.04 -t chapter9 .
#docker run -it --entrypoint /bin/bash chapter9
docker build --no-cache -f Dockerfile.debian -t chapter9 .
#docker run -it --entrypoint /bin/bash chapter9
