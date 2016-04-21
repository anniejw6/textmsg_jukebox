from flask import Flask, request, redirect
from celery import Celery
import twilio.twiml
import pandas as pd
from youtube import YouTube
import uuid
import os

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

wd = '/Users/annie/github/music_text/'
found_file = 'songs_found.csv'

# Remove irrelevant files
if os.path.isfile(wd + found_file):
    os.remove(wd + found_file)


@celery.task
def search_dl_youtube(search_term, youtube,
                      id=str(uuid.uuid1()),
                      wd=wd,
                      found_file=found_file):
    # Search for song
    vid_id = youtube.find_video(search_term)
    # Download song
    if vid_id is not None:
        os.system("youtube-dl -o '%s' -f 140 %s" %
                  (wd + 'music/' + vid_id + '.%(ext)s', vid_id))
    else:
        vid_id = 'COULD_NOT_FIND'
    # Record Output
    fd = open(wd + found_file, 'a')
    fd.write(','.join([id, search_term.encode('ascii', 'ignore'),
                       vid_id, vid_id + '.m4a']))
    fd.write('\n')
    fd.close()
    return('Success')


@celery.task
def skip_song(found_file=found_file, wd=wd):
    fd = open(wd + found_file, 'a')
    fd.write(','.join([str(uuid.uuid1()), '', '', 'NEXT']))
    fd.write('\n')
    fd.close()


@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""
    text_body = request.values.get('Body', None)

    print(text_body)
    #text_body = text_body.encode('ascii', 'ignore')
    # print(text_body)
    if text_body is None:
        msg = 'Invalid text'
    elif text_body.lower() == 'next628':
        msg = 'Song skipped!'
        skip_song.delay()
    else:
        msg = 'Got your song request!'
        # Add to file
        search_dl_youtube.delay(text_body, YouTube())

    resp = twilio.twiml.Response()
    resp.message(msg)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
