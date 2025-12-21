# Turntable Track Recognition — README

A system that streams audio from a turntable into an Icecast server, segments the stream into short snippets, recognises music from those snippets, updates Icecast metadata, and optionally scrobbles tracks to Last.fm.

This repository contains the following:
- Stream input: [stream/stream.liq](stream/stream.liq) used by the Liquidsoap container.
- Segmenter: [segmenter/Dockerfile](segmenter/Dockerfile) that uses ffmpeg to segment the Icecast stream into snippets and writes them to the shared `/audio` volume.
- Recogniser service: Dockerised Python service in [recogniser/](recogniser) that monitors `/audio`, recognises tracks, updates Icecast and scrobbles to Last.fm.
- Orchestration: [docker-compose.yml](docker-compose.yml)

Quick start
-----------
1. Copy [.env.example](.env.example) -> `.env` and fill in your Last.fm credentials (if you want to use scrobbling).
    * The [get_lastfm_session_token.py](recogniser/recognition_service/helpers/get_lastfm_session_token.py) script can be used to generate a Last.fm session key.
2. Build and run the system: `docker compose up --build -d` (see [docker-compose.yml](docker-compose.yml).)

System overview
-----------------------
1. Liquidsoap (see [stream/stream.liq](stream/stream.liq)) publish ADC input to the Icecast container.
2. The segmenter (see [segmenter/Dockerfile](segmenter/Dockerfile)) runs ffmpeg to save 12s audio snippets in the shared `/audio` volume.
3. The recogniser service (see [recogniser/Dockerfile](recogniser/Dockerfile) and [recogniser/recogniser.py](recogniser/recogniser.py)) monitors the `/audio` directory and processes eligible snippets:
   - Music recognition using Shazam via [`music_recogniser.MusicRecogniser`](recogniser/recognition_service/music_recogniser.py)
   - Icecast metadata updates via [`icecast.Icecast`](recogniser/recognition_service/icecast.py)
   - Last.fm integration via [`lastfm.LastFm`](recogniser/recognition_service/lastfm.py)
   - Main service loop: [`recognition_service.RecognitionService`](recogniser/recognition_service/recognition_service.py)

### Example Output (Recogniser)
```
Now playing: Joy Crookes - Wild Jasmine
Scrobbled: Joy Crookes - Wild Jasmine
Now playing: Joy Crookes - Skin
Scrobbled: Joy Crookes - Skin
Now playing: Joy Crookes - Power
Scrobbled: Joy Crookes - Power
```

### Hardware
- Raspberry Pi 5
- Behringer U-PHONE UFO202
- Audiotechncia AT-LP60X


Configuration
-------------
Configuration values live in [`config.Config`](recogniser/recognition_service/config.py). 

Important values:

- LASTFM_API_KEY, LASTFM_API_SECRET, and LASTFM_SESSION_KEY — set via environment or [.env](.env.example). If any are missing, Last.fm scrobbling is disabled (see `Config.lastfm_enabled`).
  - Example: copy [.env.example](.env.example) to `.env` and fill values.
- audio_dir — default /audio, where the segmenter writes snippets.
- min_file_size — smallest accepted snippet (bytes).
- min_file_age — seconds since modification before a snippet is considered stable.
- silence_rms_threshold — RMS threshold below which a file is considered silent.
- process_interval — how often the main loop sleeps between checks.
- debounce_required — number of consecutive detections required to accept a recognition.