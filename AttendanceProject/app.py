from attendance import recognise
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
app=Flask(__name__)
CORS(app)
@app.route('/', methods = ["POST"])
def index():
    args = json.loads(request.data)
    data_uri = args.get("data_uri")
    return jsonify({"data":recognise(data_uri)})


app.run(debug=True)


