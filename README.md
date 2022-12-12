# cripto-dh-arduino
## Descripción y contexto del proyecto.
El problema a solucionar en el proyecto es el siguiente: 

 El centro meteorológico ACME procesa la temperatura recopilada por sensores en distintaslocalidades de Chile. Últimamente el pronóstico general ha sido errático iniciando una investigación. Al indagar, se constata que los sensores registran las muestras diarias correctamente. Los registros son reenviados al menos una vez al día al servidor de aplicaciones publicado en una nube. También, fue posible notar que los datos viajan en texto claro.Además, que el protocolo de seguridad aplicado no fue diseñadopara los sensores, sino que para servidores.

La solución propuesta es la siguiente: Aplicar protocolos criptográficos complejos a los datos enviados por los sensores hacia su remitente, logrando así, encriptar la información sensible transmitida y evitando un ataque instantáneo por parte de terceros en la data. Que según lo identificado, es altamente plausible que sea la causa por la cual los datos puedan entregar resultados erróneos en las predicciones, ya que puede haber intervención de terceros al no haber seguridad.

El sistema criptográfico elegido para utilizar dentro de la solución propuesta es *Diffie Hellman*

Es relevante que para el desarrollo se han hecho algunas asunciones, como por ejemplo, se han establecido la llave publica y privada de manera determinista para establecer combinaciones válidas que permitan el encriptado y el desencriptado.

## Descripción módulos programáticos

En primer lugar se utiliza un sensor de temperatura en conjunto con arduino, que envía los datos del sensor por puerto serial, como se puede ver en el siguiente código.

https://github.com/matiassotose/cripto-dh-arduino/blob/7f8fd08dec0dd14af469dcdd25324cf1fd33d23a/sensor/sensor.ino#L1-L17

Posteriormente, estos se envían mediante un script en python, en texto claro en broadcast a la red mediante UDP/IP, y se programa un sniffer que a través de un header que utilizamos para individualizar estos paquetes, se obtiene la información, también en texto claro.

### Sender
https://github.com/matiassotose/cripto-dh-arduino/blob/7f8fd08dec0dd14af469dcdd25324cf1fd33d23a/legacy/sender_module.py#L1-L42
### Sniffer
https://github.com/matiassotose/cripto-dh-arduino/blob/7f8fd08dec0dd14af469dcdd25324cf1fd33d23a/legacy/sniffer_module.py#L1-L21

### Encriptación.
Se ha detectado entonces que es la intervención de terceros la que puede justificar el comportamiento errático de las predicciones, dicho esto, se crea una biblioteca propia en python que llamamos dhlib y que contiene las funciones necesarias para la creación de llaves parciales y compartidas así como encriptación y desencriptación de un mensaje.

https://github.com/matiassotose/cripto-dh-arduino/blob/7f8fd08dec0dd14af469dcdd25324cf1fd33d23a/auxilary_modules/dhlib.py#L1-L21

A partir de este módulo, se  envían nuevamente usando pySocket, los mensajes encriptados, añadiendo también un espacio de handshake donde el emisor y el receptor comparten sus llaves públicas y compartidas.

### Sender Encrypted
https://github.com/matiassotose/cripto-dh-arduino/blob/7f8fd08dec0dd14af469dcdd25324cf1fd33d23a/sender_module_encrypted.py#L1-L57
### Sniffer Encrypted
https://github.com/matiassotose/cripto-dh-arduino/blob/7f8fd08dec0dd14af469dcdd25324cf1fd33d23a/sniffer_module_encrypted.py#L1-L51
### Compartición de llaves
https://github.com/matiassotose/cripto-dh-arduino/blob/7f8fd08dec0dd14af469dcdd25324cf1fd33d23a/sender_module_encrypted.py#L22-L30

## Envío de muestras a servidor
Finalmente tras 20 muestras, el sniffer enviará un archivo txt con las muestras desencriptadas a un bucket de Amazon Web Services S3
https://github.com/matiassotose/cripto-dh-arduino/blob/7f8fd08dec0dd14af469dcdd25324cf1fd33d23a/auxilary_modules/upload_aws_module.py#L1-L18
## Ejecución.
Para ejecutar este código, clonar el repositorio mediante:
```bash
git clone git@github.com:matiassotose/cripto-dh-arduino.git
```
Luego conectar arduino por usb y editar config.ini con los datos respectivos del arduino:
https://github.com/matiassotose/cripto-dh-arduino/blob/f407224a46e7cd729ba7467182271cd5041b4ff4/config.ini.default#L1-L7

Una vez que se realicen las conexiones respectivas, ejecutar en paralelo y en el orden respectivo:
```bash
python sniffer_module_encrypted.py
```
y luego
```bash
python sender_module_encrypted.py
```
tras 20 muestras, se subirán automáticamente al bucket de S3.

## Conclusiones
Este código realizado en Python, se sustenta en las bases matemáticas explicadas en el informe del proyecto. Además existen algunas situaciones que pueden poner en riesgo la vulnerabilidad del sistema, como un Man in the middle o que por ahora, lo hemos implementado con llaves de tan solo 1 byte.
