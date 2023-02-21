import os
import json
import openai
import flask
from dotenv import load_dotenv
from flask_cors import CORS
from waitress import serve
from serp import get_serp

from openai.error import OpenAIError


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("No OPENAI_API_KEY found in environment variables.")

app = flask.Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))
is_on_heroku = os.environ.get("IS_HEROKU", None)
app.config["DEBUG"] = is_on_heroku is None
CORS(app)

@app.route("/sapi/search", methods=["POST", "GET"])
def search():
    '''Do search'''
    data = flask.request.json if flask.request.method == "POST" else flask.request.args
    try:
        def stream():
            final_prompt = get_serp(data["prompt"], num_results=3, time_period='all', region='us-en')
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=final_prompt,
                temperature=0.4,
                max_tokens=600,
                stop=["\n\n"],
                stream=True,
            )
            for resp in response:
                yield 'data: %s\n\n' % json.dumps(resp)
        # return json as event stream
        return flask.Response(stream(), mimetype="text/event-stream")
    except OpenAIError as err:
        return flask.jsonify({"error": err})

@app.route("/napi/call", methods=["POST", "GET"])
def call():
    '''Do call'''
    data = flask.request.json if flask.request.method == "POST" else flask.request.args
    prompt = data["prompt"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.4,
        max_tokens=60,
    )
    return flask.jsonify(response)

@app.route("/sapi/call", methods=["POST", "GET"])
def stream():
    # Mock response
    #return flask.Response(format_sse(str(flask.jsonify(mock))), mimetype="text/event-stream")
    '''Do call'''
    data = flask.request.json if flask.request.method == "POST" else flask.request.args
    prompt = data["prompt"]
    def stream():
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            temperature=0.4,
            max_tokens=600,
            stream=True,
        )
        for resp in response:
            yield 'data: %s\n\n' % json.dumps(resp)

    return flask.Response(stream(), mimetype="text/event-stream")

if is_on_heroku:
    serve(app, port=PORT)
    print("Server started on port", PORT)
else:
    app.run(port=PORT)