# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 23:48:28 2019

@author: Danish
"""

from flask import Flask, render_template, request
from flask import jsonify

"""'models/cornell_movie_dialog/trained_model_v2/best_weights_training.ckpt'"""
###Chat .py

"""
Script for chatting with a trained chatbot model
"""
import datetime
from os import path
from services import weather_time, check_connectivity
import general_utils
import chat_command_handler
from chat_settings import ChatSettings
from chatbot_model import ChatbotModel
from vocabulary import Vocabulary
import sys

check_connectivity()
#Read the hyperparameters and configure paths
_, model_dir, hparams, checkpoint, _, _ = general_utils.initialize_session("chat")

#Load the vocabulary
print()
print("Loading vocabulary...")
if hparams.model_hparams.share_embedding:
    shared_vocab_filepath = path.join(model_dir, Vocabulary.SHARED_VOCAB_FILENAME)
    input_vocabulary = Vocabulary.load(shared_vocab_filepath)
    output_vocabulary = input_vocabulary
else:
    input_vocab_filepath = path.join(model_dir, Vocabulary.INPUT_VOCAB_FILENAME)
    input_vocabulary = Vocabulary.load(input_vocab_filepath)
    output_vocab_filepath = path.join(model_dir, Vocabulary.OUTPUT_VOCAB_FILENAME)
    output_vocabulary = Vocabulary.load(output_vocab_filepath)

# Setting up the chat
chatlog_filepath = path.join(model_dir, "chat_logs", "chatlog_{0}.txt".format(datetime.datetime.now().strftime("%Y%m%d_%H%M%S")))
chat_settings = ChatSettings(hparams.model_hparams, hparams.inference_hparams)

wt = weather_time()
def chat_fun(n_query):
    terminate_chat = False
    reload_model = False
    chk, response = wt.query_check(n_query)
    
    
    while not terminate_chat:
        #Create the model
        print()
        print("Initializing model..." if not reload_model else "Re-initializing model...")
        print()
        with ChatbotModel(mode = "infer",
                          model_hparams = chat_settings.model_hparams,
                          input_vocabulary = input_vocabulary,
                          output_vocabulary = output_vocabulary,
                          model_dir = model_dir) as model:
    
            #Load the weights
            print()
            print("Loading model weights...")
            print()
            model.load(checkpoint)
    
            #Show the commands
            if not reload_model:
                #Uncomment the following line if you want to print commands.
                #chat_command_handler.print_commands()
                print('Model Reload!')
    
            while True:
                #Get the input and check if it is a question or a command, and execute if it is a command
                #question = input("You: ")
                question=n_query
                is_command, terminate_chat, reload_model = chat_command_handler.handle_command(question, model, chat_settings)
                if terminate_chat or reload_model:
                    break
                elif is_command:
                    continue
                elif chk:
                    return response
                else:
                    question = n_query
                    #If it is not a command (it is a question), pass it on to the chatbot model to get the answer
                    question_with_history, answer = model.chat(question, chat_settings)
                    
                    #Print the answer or answer beams and log to chat log
                    if chat_settings.show_question_context:
                        print("Question with history (context): {0}".format(question_with_history))
                    
                    if chat_settings.show_all_beams:
                        for i in range(len(answer)):
                            print("ChatBot (Beam {0}): {1}".format(i, answer[i]))
                    else:
                        n_answer = answer
                        print("ChatBot: {0}".format(n_answer))
                        
                    print()
                    
                    
                    
                    return n_answer
                    if chat_settings.inference_hparams.log_chat:
                        chat_command_handler.append_to_chatlog(chatlog_filepath, question, answer)
                


##chat.py ends here


app = Flask(__name__,static_url_path="/static")

#############
# Routing
#
@app.route('/message', methods=['POST'])
def reply():
    return jsonify( { 'text': chat_fun(request.form['msg']) } )

@app.route("/")
def index():
    return render_template("index.html")
#############

'''
Init seq2seq model

    1. Call main from execute.py
    2. Create decode_line function that takes message as input
'''
#_________________________________________________________________
import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
import tensorflow as tf



#_________________________________________________________________

# start app
if (__name__ == "__main__"):
    app.run(port = 5000)
