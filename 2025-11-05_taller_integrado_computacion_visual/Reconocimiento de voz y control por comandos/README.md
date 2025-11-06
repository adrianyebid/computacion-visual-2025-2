# Punto 8 – Reconocimiento de voz y control por comandos

## Objetivo  
Escuchar al usuario mediante micrófono, reconocer comandos de voz en español o inglés, responder mediante voz (TTS) y disparar acciones visuales o enviar mensajes OSC a otro sistema (por ejemplo, Unity o Processing).

## Herramientas utilizadas  
- Python 3.12.0
- SpeechRecognition para reconocimiento de voz.  
- pocketsphinx como motor offline (opcional) y Google Web Speech API como fallback.  
- pyttsx3 para respuesta hablada.  
- python-osc (opcional) para enviar mensajes OSC.

## Cómo ejecutar  
1. Instala los paquetes con:  
```
pip install -r requirements.txt
```
2. Conecta un micrófono funcional al equipo y permite acceso.  
3. Ejecuta el script:  
```
python main.py
```
4. El sistema dice “Reconocimiento de voz listo.” y espera comandos. Algunos ejemplos:  
- “iniciar”, “play”, “empieza” → `/cv/start_anim`  
- “pausa”, “stop” → `/cv/pause_anim`  
- “más grande”, “increase” → `/cv/bigger`  
- “rojo”, “red” → `/cv/color_red`  
- “siguiente color” → `/cv/next_color`  
- “captura”, “screenshot” → `/cv/screenshot`  
- “salir”, “terminate / quit” → finaliza el programa  

5. El sistema responde por voz y por consola imprime el evento. También puede enviar el mensaje OSC si está activado.

## Configuración OSC (opcional)  
Al igual que en el punto 7:  

```
export USE_OSC=1
export OSC_IP=127.0.0.1
export OSC_PORT=9000
python main.py
```

## Evidencias / entrega  
Captura o graba:  
- Terminal donde se muestran los comandos reconocidos y los eventos disparados.  
- Grabación de audio/voz del sistema respondiendo (“Animación iniciada.” etc).  
- **Video evidencia:** Incluye el archivo `8_video.mp4` mostrando el funcionamiento completo del sistema.  