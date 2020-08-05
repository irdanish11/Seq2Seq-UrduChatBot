# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 23:48:28 2019

@author: IrfanDanish
"""

from flask import Flask, render_template, request
from flask import jsonify
from chatbot_serving import chat_fun_english, chat_fun_urdu, model_loading
from API_Configuration import write_response, validate_key 
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

"""'models/cornell_movie_dialog/trained_model_v2/best_weights_training.ckpt'"""


model, chatlog_filepath, chat_settings = model_loading()

  
###################### Flask App ######################

app = Flask(__name__,static_url_path="/static")


###################### Routing For API ###################### 
"""
127.0.0.1:5000/api/urdu-chatbot?key_id=38303&query=
"""
@app.route('/api/urdu-chatbot')
def urdu_api():
    question = request.args.get('query', default = '', type = str)
    key_id = request.args.get('key_id', default = 0, type = int)
    #validate key_id
    flag, response = validate_key(key_id)
    if flag:
        answer = chat_fun_urdu(question, model, chat_settings, chatlog_filepath)
        write_response(question, answer, acs_point='API', language='urdu')
    else:
        answer=response
    return jsonify(answer)

"""
127.0.0.1:5000/api/english-chatbot?key_id=38303&query=
"""
@app.route('/api/english-chatbot')
def english_api():
    question = request.args.get('query', default = '', type = str)
    key_id = request.args.get('key_id', default = 0, type = int)
    #validate key_id
    flag, response = validate_key(key_id)
    if flag:
        answer = chat_fun_english(question, model, chat_settings, chatlog_filepath)
        write_response(question, answer, acs_point='API', language='english')
    else:
        answer=response
    return jsonify(answer)



###################### Routing for WebApp ######################

@app.route('/message_urdu', methods=['POST'])
def reply_urdu():
    question = request.form['msg']
    answer = chat_fun_urdu(question, model, chat_settings, chatlog_filepath)
    write_response(question, answer, acs_point='Web App', language='urdu')
    return jsonify( { 'text':  answer} )

@app.route('/message_english', methods=['POST'])
def reply_english():
    question = request.form['msg']
    answer = chat_fun_english(question, model, chat_settings, chatlog_filepath)
    write_response(question, answer, acs_point='Web App', language='english')
    return jsonify( { 'text':  answer} )

@app.route("/chatbot-urdu")
def index_urdu():
    return render_template("index_urdu.html")

@app.route("/chatbot-english")
def index_english():
    return render_template("index_english.html")


# start app
if (__name__ == "__main__"):
    #Configure the verbosity of UTF-8 chracters.
    app.config['JSON_AS_ASCII'] = False
    app.run(port = 5000)
