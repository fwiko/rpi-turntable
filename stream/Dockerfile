FROM debian:bookworm

RUN apt-get update && apt-get install -y \
    liquidsoap \
    alsa-utils \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /stream
COPY stream.liq .

CMD ["liquidsoap", "stream.liq"]
