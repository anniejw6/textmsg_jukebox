# Virtual Environment - Python
```
virtualenv -p python2.7 rpi
source rpi/bin/activate

pip install --upgrade pip
pip install --upgrade setuptools
pip install -r requirements.txt 

# pip freeze >> requirements.txt
```

# Twilio Code
Follow [these docs](https://www.twilio.com/docs/quickstart/python/sms/sending-via-rest)
`serve_twilio.py` tries to listen for texts
* Run `python serve_twilio.py` to set up the server
* In a separate terminal window, also run `./ngrok http 5000`
    * Grab the forwarding URL

# What's Going On

* Server listening in for texts (`serve_twilio.py`)
    - Write to list of incoming texts
    - If text is NEXT_CODE, gets written to `playlist.txt` directly (skips next part)
* In a loop on a separate script (`search_youtube_dl.py`)
    - Read in texts
    - Search on youtube for URL
    - Download m4a
    - `youtube-dl -f 140 https://www.youtube.com/watch?v=iRYvuS9OxdA`
    - Add list to `playlist.txt`
* Every two seconds, a python script (`music_play.py`) reads in `playlist.txt` and adds the next song to the queue
    * TODO: Every ten songs, delete the files of those songs

# TODO
* Figure out order in which scripts should be run and who erases what files.
* Stop hard-coding file path
* Celery async