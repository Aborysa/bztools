FROM ubuntu:20.04

ENV PATH "/root/Steam:${PATH}"
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get install -y lua5.1 luarocks python3-pip python3 espeak zip curl lib32gcc1 dos2unix
RUN luarocks install moonscript

# python scripts
RUN pip3 install pydub gTTS Pillow vdf
COPY ./pytools /bztools

# squish
WORKDIR /tmp
RUN set -eux && \
    curl --tlsv1.2 -sSLo- https://matthewwild.co.uk/projects/squish/squish-0.2.0.tar.gz | tar xzf - && \
    cd squish-0.2.0 && \
    mv make_squishy /usr/local/bin && \
    make && make install && \
    rm -rf /tmp/*

WORKDIR /root/Steam
RUN set -eux && \
    curl --tlsv1.2 -sSLo- "https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz" | tar xzf - && \
    mv steamcmd.sh steamcmd && \
    steamcmd +quit || true

WORKDIR /
CMD ["/bin/bash"]