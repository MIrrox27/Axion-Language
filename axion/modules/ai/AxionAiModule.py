# author https://github.com/MIrrox27/Axion-Language
# Ai Module
# AxionAiModule.py

from openai import OpenAI
import requests, json
import os, time

from pyexpat.errors import messages

from axion.modules.ai.api import MODEL_URL, MODEL_TOKEN, MODEL_NAME # токен и url


"""
    Список функций для реализации:
        
        - загрузка модели в формате ONNX (`var model = `)
        - функция с определенным количеством запросов
        
            # текстовые модели
        - отправка запросов модели и получение ответа
        - создание контекста 
        - очистка контекста 
        
            
            # изображения 
        - 
        -
"""



class Error:
    def __init__(self, module):
        self.module = module

    def raise_error(self,  msg, func):
        raise Exception(f'[{self.module}]: [{func}] {msg}')


class AiModule:
    error = Error('AiModule')








class Ai(AiModule):
    def __init__(self, model_name, temperature=0.5, max_tokens=250):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens







class Client(AiModule): # класс для отправки запросов, хранения контекста

    def __init__(self, api, base_url, context):
        self.default_context = [{}]

        self.api = api
        self.base_url = base_url

        if context == None:
            self.context = self.default_context
        else:
            self.context = context


    def reset_context(self):
        self.context = self.default_context
        return self.context



    def get_context(self):
        return self.context

    def add_msg_to_context(self, role, msg):
        if not self.context[0]:
            self.context = [
                {'role': str(role),
                 'content': str(msg)}
            ]

        else:
            self.context.append({
                'role': str(role),
                'content': str(msg)
            })
        return self.context




class Response(AiModule):
    def __init__(self, client, ai, msg):
        self.client = client
        self.ai = ai
        self.msg = msg


    def send_msg(self):
        full_url = self.client.base_url
        if not full_url.endswith('/chat/completions'):
            full_url = full_url.rstrip('/') + '/chat/completions'

        self.client.context.append(
            {'role': 'user',
             'content': str(self.msg)
             })

        response = requests.post(
            url=full_url,

            headers={
                "Authorization": f"Bearer {str(self.client.api)}",
                "Content-Type": "application/json"
            },

            data=json.dumps({
                "model": str(self.ai.model_name),
                "messages": self.client.context,
                "temperature": self.ai.temperature,
                "max_tokens": self.ai.max_tokens

            })
        )

        result = response.json()
        answer = result['choices'][0]['message']['content']

        self.client.context.append(
            {'role': 'assistant',
             'content': str(answer)
             })

        #print(self.client.context)
        return answer

