import datetime
from flask import jsonify, request
from flask import Flask

from flask import abort

myapp = Flask(__name__)
date = {
'hello': 'Hello World!',
'name': 'My name is Flask Server',
}


@myapp.route("/dictionary/<string:key>", methods=["GET"])
def get_name(key):
    if key not in date.keys():
        abort(404)
    value = date.get(key)
    return jsonify({"your_result":value,"time":datetime.datetime.now()})


@myapp.route("/dictionary/", methods=["POST"])
def my_post():
    if "key" not in request.json() or  "value" not in request.json():
        abort(400)
    key = request.json.get("key")
    value = request.json.get("value")
    if key in date.keys():
        abort(409)
    date.update({key:value})
    return jsonify({"your_result":value,"time":datetime.datetime.now()})


@myapp.route("/dictionary/<string:key>", methods=["PUT"])
def update_key(key):
    if key not in date.keys():
        abort(404)
    new_value = request.json.get("value")
    date.update({key:new_value})
    return jsonify({"you_update":{key:new_value},"time":datetime.datetime.now()})


@myapp.route("/dictionaty/<string:key>", methods=["DELETE"])
def delete_key(key):
    if key not in date.keys():
        return jsonify({"result":"key not found","time":datetime.datetime.now()})
    else:
        del date[key]
        return jsonify({"you delete key":key})

if __name__ == "__main__":
    myapp.run()