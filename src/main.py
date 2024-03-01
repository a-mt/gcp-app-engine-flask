import datetime
import os

from flask import Flask, render_template, request
from google.cloud import datastore
from google.auth.transport import requests
import google.oauth2.id_token

app = Flask(__name__)

# Database
datastore_client = datastore.Client()

# Firebase authentication
firebase_request_adapter = requests.Request()

#+-------------------------------------
#| MODELS
#+-------------------------------------

def store_time(email, dt):
    entity = datastore.Entity(
        key=datastore_client.key("User", email, "visit"), # instead of key=datastore_client.key("visit")
    )
    entity.update({"timestamp": dt})

    datastore_client.put(entity)

def fetch_times(email, limit):
    query = datastore_client.query(
        kind="visit",
        ancestor=datastore_client.key("User", email), # add 
    )
    query.order = ["-timestamp"]

    times = query.fetch(limit=limit)

    return times

#+-------------------------------------
#| VIEWS
#+-------------------------------------

@app.route("/")
def root():
    times = None

    # Check if the user is authenticated
    id_token = request.cookies.get("token")
    claims = None
    error_message = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter
            )
            email = claims["email"]

            # Store the current access time in Datastore.
            store_time(email, datetime.datetime.now(tz=datetime.timezone.utc))

            # Fetch the most recent 10 access times from Datastore.
            times = fetch_times(email, 10)

        except ValueError as exc:
            # This will be raised if the token is expired or any other
            # verification checks fail.
            error_message = str(exc)

    return render_template(
        "index.html",
        times=times, user_data=claims, error_message=error_message,
    )

#+-------------------------------------
#| ENTRYPOINT
#+-------------------------------------

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    HOST = os.environ.get('HOST', '127.0.0.1')
    PORT = int(os.environ.get('PORT', '8080'))

    app.run(host=HOST, port=PORT, debug=True)
