from datetime import datetime
from flask import Flask, request, jsonify
import pickle
import json
from datetime import datetime
import requests

last_update_date = datetime.min
latest_version = 'v0.0.0'
server_version = 'v0.0.3'
model = None
version_file_url = "https://raw.githubusercontent.com/vrjuliao/BCC/master/cloud-computing/tp2/classsifier/VERSION.json"
model_file_url = "https://raw.githubusercontent.com/vrjuliao/BCC/master/cloud-computing/tp2/classsifier/isamerican.pickle"

def get_version():
  global version_file_url
  req = requests.get(version_file_url)
  return json.loads(req.content)

def get_model():
  global model_file_url
  req = requests.get(model_file_url)
  return pickle.loads(req.content)

def load_model():
  global last_update_date, latest_version, model
  model_metadata = get_version()
  if model_metadata is not None:
    current_update_date = datetime.fromisoformat(model_metadata['last_update'])
    if(current_update_date > last_update_date):
      last_update_date = current_update_date
      latest_version = model_metadata['version']
      model = get_model()
    else: return 
  else: return

app = Flask(__name__)
@app.route("/api/american", methods=["POST"])
def api_american():
  global model, last_update_date, server_version
  load_model()
  if model is None:
    return jsonify({'err': 'no predictor model to load'}), 503

  content = request.json
  print(content)
  is_american = model.predict([content['text']])
  return jsonify({
    "is_american": str(is_american[0]),
    "version": server_version,
    "model_date": last_update_date.strftime('%Y-%m-%d')
  })
