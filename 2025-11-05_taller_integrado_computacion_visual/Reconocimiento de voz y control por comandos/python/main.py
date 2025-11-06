import os
import time
import re
import pyttsx3
from pythonosc.udp_client import SimpleUDPClient
import speech_recognition as sr

# Config OSC opcional (USE_OSC=1 para activar)
USE_OSC = os.environ.get("USE_OSC", "0") == "1"
OSC_IP   = os.environ.get("OSC_IP", "127.0.0.1")
OSC_PORT = int(os.environ.get("OSC_PORT", "9000"))
osc = SimpleUDPClient(OSC_IP, OSC_PORT) if USE_OSC else None

# TTS
tts = pyttsx3.init()
tts.setProperty('rate', 175)

def speak(text):
    print(f"[TTS] {text}")
    try:
        tts.say(text)
        tts.runAndWait()
    except Exception as e:
        print(f"[TTS error] {e}")

def send_event(name, value=None):
    print({"event": name, "value": value, "t": time.time()})
    if osc:
        path = f"/cv/{name}"
        if value is None:
            osc.send_message(path, [])
        else:
            if isinstance(value, (list, tuple)):
                osc.send_message(path, list(value))
            else:
                osc.send_message(path, [value])

# Diccionario de comandos (ES/EN)
COMMANDS = {
    # acción : patrones
    "start_anim":   [r"\b(iniciar|empieza|play|start)\b"],
    "pause_anim":   [r"\b(pausa|detén|stop|pause)\b"],
    "reset":        [r"\b(reset|reinicia|reiniciar)\b"],
    "bigger":       [r"\b(más grande|aumenta|bigger|increase)\b"],
    "smaller":      [r"\b(más pequeño|reduce|smaller|decrease)\b"],
    "color_red":    [r"\b(rojo|red)\b"],
    "color_blue":   [r"\b(azul|blue)\b"],
    "color_green":  [r"\b(verde|green)\b"],
    "next_color":   [r"\b(siguiente color|next color)\b"],
    "screenshot":   [r"\b(captura|screenshot)\b"]
}

def match_command(text):
    text_low = text.lower()
    for action, patterns in COMMANDS.items():
        for pat in patterns:
            if re.search(pat, text_low):
                return action
    return None

def recognize_once(recognizer, mic):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.6)
        print("Di un comando… (frase corta)")
        audio = recognizer.listen(source, phrase_time_limit=3)

    # 1) Offline pocketsphinx
    try:
        txt = recognizer.recognize_sphinx(audio, language="es-ES")
        if not txt.strip():
            raise ValueError("Sphinx vacío")
        return txt
    except Exception:
        pass

    # 2) Google Web Speech (requiere internet)
    try:
        txt = recognizer.recognize_google(audio, language="es-ES")
        return txt
    except Exception:
        # fallback inglés
        try:
            txt = recognizer.recognize_google(audio, language="en-US")
            return txt
        except Exception as e:
            print(f"[Reconocimiento falló] {e}")
            return ""

def main():
    r = sr.Recognizer()

    # Selección de micrófono por defecto
    try:
        mic = sr.Microphone()
    except Exception as e:
        print(f"No se pudo abrir el micrófono: {e}")
        return

    speak("Reconocimiento de voz listo.")
    print("Comandos ejemplo: 'iniciar', 'pausa', 'reset', 'más grande', 'rojo', 'siguiente color', 'screenshot'.")

    while True:
        text = recognize_once(r, mic)
        if not text:
            print("No entendí. Repite por favor.")
            continue

        print(f"Escuché: {text}")
        action = match_command(text)
        if action:
            send_event(action, 1)
            # respuestas habladas cortas
            if action == "start_anim":   speak("Animación iniciada.")
            elif action == "pause_anim": speak("Animación en pausa.")
            elif action == "reset":      speak("Reiniciado.")
            elif action in ("bigger","smaller"): speak("Tamaño ajustado.")
            elif action.startswith("color_"):    speak("Color cambiado.")
            elif action == "next_color":         speak("Siguiente color.")
            elif action == "screenshot":         speak("Captura tomada.")
        else:
            speak("No encontré comando.")

        # salida con palabra clave
        if re.search(r"\b(salir|terminar|exit|quit)\b", text.lower()):
            speak("Adiós.")
            break

if __name__ == "__main__":
    main()
