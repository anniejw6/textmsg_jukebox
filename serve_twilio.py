from flask import Flask, request, redirect
import twilio.twiml
import pandas as pd 
import uuid

app = Flask(__name__)
 
# Try adding your own number to this list!
callers = {
    "+14158675309": "Curious George",
    "+14158675310": "Boots",
    "+14158675311": "Virgil",
}
 
@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    """Respond and greet the caller by name."""
 
    #from_number = request.values.get('From', None)
    #if from_number in callers:
    #    message = callers[from_number] + ", thanks for the message!"
    #else:
    #    message = "Monkey, thanks for the message!"

    text_body = request.values.get('Body', None)
    print(text_body)
    #text_body = text_body.encode('ascii', 'ignore')
    #print(text_body)
    if text_body is None:
    	msg = 'Invalid text'
    elif text_body.lower() == 'next628':
    	fd = open('/Users/annie/github/music_text/songs_found.csv','a')
    	fd.write(','.join([str(uuid.uuid1()), '', '', 'NEXT']))
    	fd.write('\n')
    	fd.close()
        msg = 'Song skipped!'
    else:
    	msg = 'TT' + text_body
    	# Add to file
    	fd = open('/Users/annie/github/music_text/to_youtube.csv','a')
    	fd.write(str(uuid.uuid1()) + ',' + text_body)
    	fd.write('\n')
    	fd.close()

    resp = twilio.twiml.Response()
    resp.message(msg)
 
    return str(resp)
 
if __name__ == "__main__":
    app.run(debug=True)