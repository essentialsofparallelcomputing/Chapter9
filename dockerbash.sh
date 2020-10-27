#!/bin/sh
XSOCK=/tmp/.X11-unix
XAUTH=/tmp/.docker.xauth
docker run -it --gpus all -v $XSOCK:$XSOCK -v $XAUTH:$XAUTH -e XAUTHORITY=$XAUTH \
	--security-opt seccomp=unconfined --cap-add=SYS_PTRACE \
        --entrypoint /bin/bash essentialsofparallelcomputing/chapter9
