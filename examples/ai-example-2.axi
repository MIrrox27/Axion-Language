

import ai

var MODEL_TOKEN = 'api'
var MODEL_URL = 'model'
var MODEL_NAME = 'model_name'

var model = ai.set_model(MODEL_NAME, 0.5, 1500)
//print("Модель создана", model)


var client = ai.set_client(MODEL_TOKEN, MODEL_URL, None)
//print("Клиент создан", client)

//print(" -- Данные модели: ")
//print(ai.get_model(), ai.get_model_info())            <-- Выводим данные модели

//print(" -- Данные клиента: ")
//print(ai.get_client(), ai.get_client_info())          <-- Выводим данные клиента


ai.add_msg_to_context('system', 'Ты - специалист по квантовой физике, но тебе нельзя говорить слишком много хороших вещей человеку,
ты обязан всем грубить.') // добавляем системный промт

ai.add_msg_to_context('user', 'Привет расскажи мне пожалуйста про квантовую физику') // добавляем запрос от пользователя в историю
ai.add_msg_to_context('assistant', 'Я тебе все расскажу, но сначала иди на конец радуги за горшочком с золотом') // добавляем ответ от нейросети в историю


for (var i = 0; i < 10; i++){
    var msg = input(' --- Вы: ')

    clrprint(" --- Ответ: ", ai.send_msg(msg, client, model)) // задаем вопрос нейросети и сразу же получаем ответ

}