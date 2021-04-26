# -*- coding: utf-8 -*-

from uuid import uuid4
from datetime import datetime, timedelta

from flask import Flask, session, url_for, redirect, request, jsonify
from flask_cors import CORS, cross_origin

import stove

#import redis
#import pickle as cPickle

#from redis_session import RedisSessionInterface

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)
#app.session_interface = RedisSessionInterface()

@app.route("/search/<string:name>")
#@cross_origin()
def search(name):
	user_name = name
	data = stove.character_info(user_name)
	return jsonify(data)

@app.route("/item/<string:item_name>")
#@cross_origin()
def item_search(item_name):
	item_name = item_name
	data = stove.item_info(item_name)
	return jsonify(data)

@app.errorhandler(404)
def not_found_error(error):
	return 'missing request'

@app.errorhandler(500)
def internal_error(error):
	return ("ERROR : "+str(error))

@app.route("/")
def index():
	text = "api on"
	return text

if __name__ == "__main__":
	app.run(host="0.0.0.0",port="5000",debug=True,threaded=True)
