# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:34:01 2020

@author: danis
"""
import datetime
from os import path
import general_utils
import chat_command_handler
from chat_settings import ChatSettings
from vocabulary import Vocabulary
from services import weather_time
from chatbot_model import ChatbotModel



"""'models/cornell_movie_dialog/trained_model_v2/best_weights_training.ckpt'"""

def model_loading():
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
    
    ############# Loading Model #############
    
    reload_model = False
    print()
    print("Initializing model..." if not reload_model else "Re-initializing model...")
    print()
    model = ChatbotModel(mode = "infer",
                      model_hparams = chat_settings.model_hparams,
                      input_vocabulary = input_vocabulary,
                      output_vocabulary = output_vocabulary,
                      model_dir = model_dir)
    
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
    return model, chatlog_filepath, chat_settings

def chat_fun_english(question, model, chat_settings, chatlog_filepath):
    #Get the input and check if it is a question or a command, and execute if it is a command
    #question = input("You: ")
    is_command, terminate_chat, reload_model = chat_command_handler.handle_command(question, model, chat_settings)
    if is_command:
        pass
    else:
        #If it is not a command (it is a question), pass it on to the chatbot model to get the answer
        question_with_history, answer = model.chat(question, chat_settings)
        
        #Print the answer or answer beams and log to chat log
        if chat_settings.show_question_context:
            print("Question with history (context): {0}".format(question_with_history))
            print("\n1st if")
        
        if chat_settings.show_all_beams:
            for i in range(len(answer)):
                print("ChatBot (Beam {0}): {1}".format(i, answer[i]))
                print("\n2nd if")
        else:
            print("ChatBot: {0}".format(answer))
            #print("\n else")
            
        print()
        
        if chat_settings.inference_hparams.log_chat:
            chat_command_handler.append_to_chatlog(chatlog_filepath, question, answer)
        return answer
    
wt = weather_time()
def chat_fun_urdu(n_query, model, chat_settings, chatlog_filepath):
    chk, response = wt.query_check(n_query)
    terminate_chat = False
    #Get the input and check if it is a question or a command, and execute if it is a command
    #question = input("You: ")
    question=n_query
    is_command, terminate_chat, reload_model = chat_command_handler.handle_command(question, model, chat_settings)
    if is_command:
        pass
    elif chk:
        return response
    else:
        question = ChatSettings.To_query(n_query)
        #If it is not a command (it is a question), pass it on to the chatbot model to get the answer
        question_with_history, answer = model.chat(question, chat_settings)
        
        #Print the answer or answer beams and log to chat log
        if chat_settings.show_question_context:
            print("Question with history (context): {0}".format(question_with_history))
        
        if chat_settings.show_all_beams:
            for i in range(len(answer)):
                print("ChatBot (Beam {0}): {1}".format(i, answer[i]))
        else:
            n_answer = ChatSettings.To_answer(answer) 
            print("ChatBot: {0}".format(n_answer))     
        print()
        return n_answer
        if chat_settings.inference_hparams.log_chat:
            chat_command_handler.append_to_chatlog(chatlog_filepath, question, answer)
                
