FROM debian:bookworm

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /audio
VOLUME /audio

CMD ffmpeg -i http://icecast-stream:8000/live.mp3 \
  -ac 1 -ar 44100 \
  -f segment -segment_time 12 -reset_timestamps 1 \
  snippet_%09d.wav
