# LICENSE UPL 1.0
#
# Copyright (c) 2017 Oracle and/or its affiliates. All rights reserved.
#
FROM oraclelinux:7-slim

ENV JAVA_PKG=serverjre-9.0.4_linux-x64_bin.tar.gz
ENV JAVA_HOME=/usr/java/default

ADD $JAVA_PKG /usr/java/

RUN export JAVA_DIR=$(ls -1 -d /usr/java/*) && \
    ln -s $JAVA_DIR /usr/java/latest && \
    ln -s $JAVA_DIR /usr/java/default && \
    alternatives --install /usr/bin/java java $JAVA_DIR/bin/java 20000 && \
    alternatives --install /usr/bin/javac javac $JAVA_DIR/bin/javac 20000 && \
alternatives --install /usr/bin/jar jar $JAVA_DIR/bin/jar 20000