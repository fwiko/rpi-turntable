import time
import webbrowser
import pylast

API_KEY = ""
API_SECRET = ""

network = pylast.LastFMNetwork(API_KEY, API_SECRET)
skg = pylast.SessionKeyGenerator(network)
url = skg.get_web_auth_url()
session_key = ""

print(f"Authorise this script to access your account here: {url}\n")

webbrowser.open(url)

while True:
    try:
        session_key = skg.get_web_auth_session_key(url)
        with open(SESSION_KEY_FILE, "w") as f:
            f.write(session_key)
        break
    except pylast.WSError:
        time.sleep(1)

print(f"Session key: {session_key}")
