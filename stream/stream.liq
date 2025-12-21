settings.init.allow_root.set(true)

set("log.stdout", true)

stream =
  input.alsa(
    device="hw:0,0",
    clock_safe=true
  )

stream = mksafe(stream)

output.icecast(
  %mp3(bitrate=128, samplerate=44100, stereo=true),
  host="icecast-stream",
  port=8000,
  password="hackme",
  mount="live.mp3",
  public=true,
  icy_metadata="true",
  stream
)
