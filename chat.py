# -*- coding: utf-8 -*-
"""
Created on Sun May 12 16:34:49 2019

@author: Danish
"""

"""
Script for chatting with a trained chatbot model
"""
import datetime
from os import path

import general_utils
import chat_command_handler
from chat_settings import ChatSettings
from chatbot_model import ChatbotModel
from vocabulary import Vocabulary
from services import weather_time, check_connectivity

""" 
    "models/cornell_movie_dialog/trained_model_v2/best_weights_training.ckpt"
"""
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
def chat_fun():
    terminate_chat = False
    reload_model = False
    
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
                question = input("You: ")
                chk, response = wt.query_check(question)
                is_command, terminate_chat, reload_model = chat_command_handler.handle_command(question, model, chat_settings)
                if terminate_chat or reload_model:
                    break
                elif is_command:
                    continue
                elif chk:
                    print(response.replace('<br>', ' '))
                else:
                    #If it is not a command (it is a question), pass it on to the chatbot model to get the answer
                    question_with_history, answer = model.chat(question, chat_settings)
                    
                    #Print the answer or answer beams and log to chat log
                    if chat_settings.show_question_context:
                        print("Question with history (context): {0}".format(question_with_history))
                    
                    if chat_settings.show_all_beams:
                        for i in range(len(answer)):
                            print("ChatBot (Beam {0}): {1}".format(i, answer[i]))
                    else:
                        print("ChatBot: {0}".format(answer))
                
                    #return n_answer
                    if chat_settings.inference_hparams.log_chat:
                        chat_command_handler.append_to_chatlog(chatlog_filepath, question, answer)
                


chat_fun()