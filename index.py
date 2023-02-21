import os
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
#{prompt: r, license_key: s}
def search():
    '''Do search'''
    data = flask.request.json if flask.request.method == "POST" else flask.request.args
    try:
        final_prompt = get_serp(data["prompt"], num_results=3, time_period='all', region='us-en')
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=final_prompt,
            temperature=0.4,
            max_tokens=600,
            stop=["\n\n"]
        )
        return flask.jsonify(response)
    except OpenAIError as err:
        return flask.jsonify({"error": err})

@app.route("/sapi/call", methods=["POST"])
#{prompt: r, license_key: s}
def call():
    '''Do call'''
    data = flask.request.json
    prompt = data["prompt"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.4,
        max_tokens=600,
    )

    return flask.jsonify(response)

@app.route("/api/call", methods=["GET"])
#{prompt: r, license_key: s}
def callget():
    '''Do call'''
    query = flask.request.args
    prompt = query["prompt"]
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.4,
        max_tokens=600,
    )

    return flask.jsonify(response)
# Listen on PORT

if is_on_heroku:
    serve(app, port=PORT)
    print("Server started on port", PORT)
else:
    app.run(port=PORT)