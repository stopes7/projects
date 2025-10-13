import json

def json_response(data, status=200):
    return json.dumps(data), status, {"Content-Type": "application/json"}
