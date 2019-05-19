# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 04:59:18 2019

@author: IrfanDanish
"""
#Study
import requests
from googletrans import Translator
import json
import random
import re

class weather_time:
    def __init__(self):
        print('Checking Services!')
    
    def time_token_check(self, question):
        with open('Token.json') as f:
            token = json.load(f)
        if (token[11] in question) or (token[12] in question) or (token[13] in question):
            if (token[14] in question) or (token[15] in question) or (token[16] in question) or (token[24] in question) or (token[25] in question) or (token[26] in question)  or (token[27] in question):
                return True
        else:
            return False
            
    def joke_token_check(self, question):
        with open('Token.json') as f:
            token = json.load(f)
        if (token[17] in question) or (token[18] in question) or (token[19] in question) or (token[20] in question) or (token[21] in question) or (token[43] in question) or (token[44] in question) or (token[45] in question) or (token[46] in question): 
            if (token[22] in question) or (token[23] in question) or (token[24] in question) or (token[25] in question) or (token[26] in question)  or (token[27] in question) or (token[30] in question) or (token[31] in question) or (token[40] in question) or (token[45] in question) or (token[44] in question) or (token[46] in question):
                return True
        else:
            return False
    
    def poetry_token_check(self, question):
        with open('Token.json') as f:
            token = json.load(f)
        if (token[28]in question) or (token[29] in question) or (token[37] in question) or (token[38] in question) or (token[39] in question):
            if (token[22] in question) or (token[23] in question) or (token[24] in question) or (token[25] in question) or (token[26] in question)  or (token[27] in question) or (token[30] in question) or (token[31] in question) or (token[37] in question) or (token[40] in question) or (token[41] in question) or (token[42] in question):
                return True
        else:
            return False
        
    def weather_token_check(self, question):
        with open('Token.json') as f:
            token = json.load(f)
        if (token[0] in question) or (token[1] in question) or (token[2] in question) or (token[3] in question) or (token[4] in question) or (token[5] in question)  or (token[7] in question) or (token[8] in question) or (token[32] in question) or (token[33] in question) or (token[34] in question):
            #or (token[6] in question)
            return True
        elif token[9] and token[10] in question:
            return True
        else:
            return False
            
    def time_response(self, city, city_ur, chk): 
        url='http://api.openweathermap.org/data/2.5/weather?q={}&appid=ed645315d45b5b05b4d3256a6bc90f22&units=metric'.format(city)
        res = requests.get(url)
        data = res.json()
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        url='http://api.timezonedb.com/v2.1/get-time-zone?key=WCAW5Y2OTSTX&format=json&by=position&lat={}&lng={}'.format(latitude, longitude)
        res = requests.get(url)
        data = res.json()
        if chk:
            time = city_ur + ' میں وقت ہے : ' + data['formatted']
            return time
        else:
            time = ' وقت ہے : ' + data['formatted']
            return time
    
    def serve_poetry(self):
        with open('Poetry.json') as f:
            response = json.load(f)
        reader = random.choice(response)
        return reader['1st_line'][0]+'<br>'+reader['2nd_line'][0]+'<br>'+reader['poet_name'][0]
            
    def weather_forecast(self, city):
        url='http://api.openweathermap.org/data/2.5/weather?q={}&appid=ed645315d45b5b05b4d3256a6bc90f22&units=metric'.format(city)
        res = requests.get(url)
        data = res.json()
        temp = data['main']['temp']
        wind_speed = data['wind']['speed']
        latitude = data['coord']['lat']
        longitude = data['coord']['lon']
        description = data['weather'][0]['description']
#        t = Translator()
#        answer = t.translate([description], dest='ur')
#        for get_answer in answer:
#            description_ur=get_answer.text
        tup='درجہ حرارت : {} ڈگری سیلسیس'.format(temp),'<br>ہوا کی رفتار : {} میٹر فی سیکنڈ'.format(wind_speed),'<br>طول بلد : {}'.format(latitude),'<br>عرض بلد : {}'.format(longitude),'<br>تفصیل : {}'.format(description)
        #The <br> is added in the above tupple so that every line prints on new line flask.jsonify() does not take \n as a newline chracter.
        st =  ''.join(tup)
        return st, latitude, longitude
    
    def get_joke(self):
        with open('Jokes.json') as f:
            jokes = json.load(f)
        joke = random.choice(jokes)
        return joke
    
    def city_check(self, question):
        with open('Cities.json') as f:
            data = json.load(f)
        tmp = {'City':'Random','Ur_City': 'Random'}
        data.append(tmp)
        #The tmp dictionary is appended to data to make the check on data[] if the value of iteration variable 'i' is
        #less than (len(data)-1) it means we have found the city in the list, otherwise city is not in the list.
        for i in range(len(data)):
            if data[i]['Ur_City'] in question:
                break
        if i<len(data)-1:
            return True, data[i]['City'], data[i]['Ur_City']
        else:
            #change the 2nd return argument to your Current city if it is not islamabad
            return False, 'Islamabad', 'اسلام آباد'    
    
    def general_query(self, question):
        with open('Questions.json') as f:
                que = json.load(f)
        for i in range(len(que)):
            if question in que[i]:
                print(i)
                return True, i
                break
            elif (i+1) >= len(que):
                return False, i
        
    
    def serve_general_query(self, count):
        with open('Answers.json') as f:
            ans = json.load(f)
        return random.choice(ans[count])  
            
    def query_check(self, query):
        #weather_lines = open('weather_response.txt', encoding = 'utf-8', errors = 'ignore').read().split('\n')
        question = re.sub(r"؟", "", query)
        question = re.sub(r"۔", "", question)
        resp_chk, count = self.general_query(question)
        with open('Weather_Response.json') as f:
            weather_lines = json.load(f)
        if question in weather_lines:
            city = 'islamabad'
            weather, _, __ = self.weather_forecast(city)
            return True, weather
        elif self.weather_token_check(question):
            with open('Token.json') as f:
                token = json.load(f)
            if (token[35] in question) or (token[36] in question):
                chk_city, city, _ = self.city_check(question)
                if chk_city:
                    weather, _,__ = self.weather_forecast(city)
                    return True, weather
                else:
                    return True, random.choice(['میں سمجھ نہیں سکا کہ آپ کیا کہنا چاہتے ہیں، <br>  مختلف طریقے سے کوشش کریں. جیسے کے: <br> آج موسم کیسا ہے <br> کیا وقت ہے','.میں معزرت خواہ ہوں بیان کردہ شہر کے لیے موسم ک سہولت میسر نہیں ہے'])
            else:
                city = 'islamabad'
                weather, _, __ = self.weather_forecast(city)
                return True, weather
                #return True, 
        elif self.time_token_check(question):
            #print('time')
            chk_city, city, city_ur = self.city_check(question)
            if chk_city:
                time = self.time_response(city, city_ur, True)
                return True, time    
            else:
                city = 'islamabad'
                city_ur = 'اسلام آباد'
                time = self.time_response(city, city_ur, False) 
                return True, time
        elif self.joke_token_check(question):
            return True, self.get_joke()
        elif self.poetry_token_check(question):
            return True, self.serve_poetry()
        elif resp_chk:
            return True, self.serve_general_query(count)
        else:
            print('else')
            weather = 0
            return False, weather
                
        