import speech_recognition as sr
import pyttsx3
import mysql.connector
from db_connector import conectar_db, cerrar_db
import os
import noisereduce as nr
import scipy.signal as sg

# Inicializa el reconocimiento de voz y el motor de síntesis de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Función para obtener respuestas de la base de datos y ejecutar comandos
def obtener_respuesta(entrada):
    conn = conectar_db()
    if conn is None:
        return "No pude conectar a la base de datos."

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT respuesta, tipo, comando FROM respuestas WHERE palabra_clave=%s", (entrada,))
        resultado = cursor.fetchone()

        if resultado:
            respuesta, tipo, comando = resultado
            if tipo == "accion":
                ejecutar_accion(comando)
            return respuesta
        else:
            return "No entendí tu solicitud."
    except mysql.connector.Error as e:
        print(f"Error en la consulta: {e}")
        return "Ocurrió un error al consultar la base de datos."

    finally:
        cerrar_db(conn)

# Función para ejecutar comandos
def ejecutar_accion(comando):
    os.system(comando)

# Función para hablar
def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

# Función para escuchar
def escuchar():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=5)  # Ajustar el nivel de ruido ambiental
        print("Escuchando...")
        audio = recognizer.listen(source)

    try:
        entrada = recognizer.recognize_google(audio, language="es-ES").lower()
        print(f"Usuario: {entrada}")
        return entrada
    except sr.UnknownValueError:
        print("No se entendió la entrada.")
        return ""
    except sr.RequestError as e:
        print(f"Error en la solicitud: {e}")
        return ""

# Bucle principal
while True:
    entrada = escuchar()
    if entrada:
        respuesta = obtener_respuesta(entrada)
        print(f"Asistente: {respuesta}")
        hablar(respuesta)
