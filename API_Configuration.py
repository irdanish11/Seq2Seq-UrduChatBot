# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 19:32:58 2020

@author: Danish
"""


import json
import os
import numpy as np

def key_id_generator(id_type, allowed_counts=50):
    if id_type=='LifeTime':
        if allowed_counts<int(10e8):
            raise ValueError('Invalid value given to argument `allowed_counts`, it cannot be less than 1000000000, while using LifeTime.')
        allowed_counts=int(10e8)
    elif id_type=='CustomCounts':
        if allowed_counts==0:
            raise ValueError('Invalid value given to argument `allowed_counts`, it should be atleast greater than 100, while using custom counts.')
    elif id_type=='Trial':
        if allowed_counts>50:
            raise ValueError('Invalid value given to argument `allowed_counts`, it should not be greater than 50, while using Trial.')
        allowed_counts=50
    else:
        raise ValueError('Invalid value given to argument `id_type`, it can be either `LifeTime`, `CustomCounts` or `Trial`!')
    #Reading Keys Database
    key_path = './API_KeysData/Keys_Database.json'
    with open(key_path, 'r') as f:
        keys_data = json.load(f)
    key_id = np.random.randint(10000,99999)
    #While loop ensures that the generated key does not exist already in the database, 
    #if key exist it creates new one.
    while key_id in keys_data['Keys_ID']:
        key_id = np.random.randint(10000,99999)
    #Storing to database
    key_id = str(key_id)
    keys_info = {'Type':id_type, 'UsedCounts': 0, 'AllowedCounts':allowed_counts}
    keys_data['Keys_ID'].append(key_id)
    keys_data['Keys_Info'][key_id] = keys_info
    with open(key_path, 'w') as f3:
        json.dump(keys_data, f3)
    print('Successfully added the new key, Key ID: {0}, Key ID Configurations: {1}'.format(key_id, keys_info))
    return key_id, keys_info

def get_key_info(key_id):
    if type(key_id)!=str:
        key_id = str(int(key_id))
    #Reading Keys Database
    key_path = './API_KeysData/Keys_Database.json'
    with open(key_path, 'r') as f:
        keys_data = json.load(f)
    if key_id not in keys_data['Keys_ID']:
        keys_data=None
        keys_info = 'Given Key ID is not valid, either buy a new Key ID or carefully check your Key ID and retry!'
    else:
        keys_info = keys_data['Keys_Info'][key_id]
    return keys_info, keys_data
        
def update_id_type_counts(key_id, update='Type', id_type=None, count=None):
    if type(key_id)!=str:
        key_id = str(int(key_id))
    #Reading Keys Database
    key_path = './API_KeysData/Keys_Database.json'
    with open(key_path, 'r') as f:
        keys_data = json.load(f)
    keys_info = keys_data['Keys_Info'][key_id]
    if update=='Type':
        if id_type==None:
            raise TypeError('Invalid value given to argument `id_type`, it can be either `LifeTime`, `CustomCounts` or `Trial`')
        keys_info['Type'] = id_type
    elif update=='Count':
        if count==None:
            raise TypeError('Invalid value given to argument `count`, provide a valid integer greater than 100')
        keys_info['AllowedCounts']=count
    else:
        raise ValueError('Invalid value given to argument `update`, it can be either, `Type` or `Count`.')
    keys_data['Keys_Info'][key_id] = keys_info
    with open(key_path, 'w') as f3:
        json.dump(keys_data, f3)
    print('Update of Key ID: {0} successful with Update type: {1}'.format(key_id, update))

def create_response_files():
    path = './responses'
    os.makedirs(path, exist_ok=True)
    response = {'Questions':[], 'Answers':[], 'Access_Point':[]}
    with open(path+'/response_log_urdu.json', 'w') as f:
        json.dump(response, f)
    with open(path+'/response_log_english.json', 'w') as f2:
        json.dump(response, f2)
    #Creating File for API Keys Database
    key_path = './API_KeysData'
    os.makedirs(key_path, exist_ok=True)
    key_id = '38303'
    keys_info = {key_id:{'Type':'LifeTime', 'UsedCounts': 0, 'AllowedCounts':int(10e8)}}
    keys_data = {'Keys_ID':[key_id], 'Keys_Info':keys_info}
    with open(key_path+'/Keys_Database.json', 'w') as f3:
        json.dump(keys_data, f3)
        
def write_response(question, answer, acs_point, language='urdu', verbose=True):
    if language=='urdu':
        path = './responses/response_log_urdu.json'
    elif language=='english':
        path = './responses/response_log_english.json'
    else:
        raise ValueError('Invalid value for argument `language`, it can be either `urdu` or `english`.')
    with open(path, 'r') as f:
        response = json.load(f)
    response['Questions'].append(question)
    response['Answers'].append(answer)
    response['Access_Point'].append(acs_point)
    #writing back to Json file
    with open(path, 'w') as f:
        response = json.dump(response, f)
    print('Responses Added')

def validate_key(key_id):
    key_info, keys_data = get_key_info(key_id)
    if keys_data==None:
        flag = False
        response = key_info
    else:
        key_path = './API_KeysData/Keys_Database.json'
        if key_info['UsedCounts'] >= key_info['AllowedCounts']:
            flag = False
            response = 'You have consumed all the allowed calls to the Chatbot API either update your plan or contact your App/Service Provider.'
        else:
            flag = True
            response = None
            key_info['UsedCounts'] += 1
            #keys_data['Keys_Info'][key_id] = key_info
            #Updating the Database
            with open(key_path, 'w') as f3:
                json.dump(keys_data, f3)
    return flag, response
    
        