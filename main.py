import urllib.request, json
import os
import sys
from urllib.request import urlopen
import urllib.parse
import re
from datetime import datetime
import time

import config


#Media entre dos números
def average(num):
    sum_num = 0
    for t in num:
        sum_num = sum_num + t

    avg = sum_num / len(num)
    return int(avg)

#Comprobar el último mensaje del bot para saber si se tiene que desactivar los avisos
def check_last_message():
    with urllib.request.urlopen("https://api.telegram.org/bot"+config.BOT_ID+"/getUpdates") as url:
        data = json.loads(url.read().decode())
        try:
            result = data['result'][-1]['message']['text']
        except:
            result = ''

        if result.lower() == config.DISABLE_KEYWORD:
            print('Saliendo del programa por estar desactivado')
            sys.exit(0)

#Enviar mensaje por telegram
def send_message(message):
    message = urllib.parse.quote(message)
    with urlopen("https://api.telegram.org/bot"+config.BOT_ID+"/sendMessage?CHAT_ID="+config.CHAT_ID+"&text="+message) as conn:
        print('Mensaje enviado')

#Comprobar si no ha funcionado internet para mostrarlo ahora a través del fichero
def check_offline_log():
    file = open(config.OFFLINE_PATH, 'r')
    content = file.read()
    if len(content) > 0:
        send_message('Internet no ha funcionado en este rango de horas: ' + content)
        open(config.OFFLINE_PATH, 'w').close()
        print('Borrando el fichero de log offline')

#Hacer ping a las DNS de Google para ver el tiempo de respuesta
def ping_server():
    #Primero comprobamos si funciona internet
    response = os.system("ping -c 1 " + config.HOSTNAME)

    #Si funciona internet, comprobar la latencia para mostrar un aviso, del contrario, guardarlo en un fichero para posteriormente enviarlo
    if response == 0:
        output = os.popen('ping '+ config.HOSTNAME +' -c 3 -i 3').read()
        timestr = re.findall("time=[0-9]+\.[0-9]", output)
        nums = []

        for time in timestr:
            #Eliminar para dejar sólo el tiempo como float
            time = float(time.replace('time=', ''))
            nums.append(time)

        num_avg = int(average(nums))
        num_max = int(max(nums))

        if num_avg > config.NOTICE_AVG_PING or num_max > config.NOTICE_MAX_PING:
            send_message('El ping medio es de ' + str(num_avg) + ' y el máximo de ' + str(num_max))

        check_offline_log()

    else:
        now = datetime.now()

        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

        file = open(config.OFFLINE_PATH, 'a')
        file.write(dt_string + '\n')


def main():
    check_last_message()

    ping_server()


while True:
    main()
    time.sleep((config.MINUTES_ITERATION*60))