# En qué consiste Internet Status
Este programa hace un ping a Google o a la dirección especificada para comprobar la lantencia y enviar un aviso por telegram en caso de tener una alta latencia o no funcionar internet. En caso de no funcionar internet, guarda en un fichero de log la fecha para enviarla posteriormente.

# Cómo configurar Internet Status
Para configurar el programa, hay que crear tanto un grupo de telegram para avisos como un bot para que avise. Posteriormente hay que modificar el fichero config.py para asignar estos valores

# Crear un bot de telegram
https://core.telegram.org/bots  Con BotFather podemos crear el bot y posteriormente añadirlo al grupo de telegram que hemos creado. Con BotFather podemos ver el ID del bot, necesario para configurar el programa.
  https://stackoverflow.com/questions/32423837/telegram-bot-how-to-get-a-group-chat-id  Con este hilo también podemos ver cómo obtener el chat id, configurable desde el fichero del programa.

# Cómo funciona Internet Status
El programa se ejecuta siempre, y cada 5 minutos realiza la comprobación de latencia y funcionalidad de internet. Si hablamos con nuestro bot y le decimos 'desactivar', no enviará ningún aviso.