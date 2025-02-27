import os
from flask import Flask, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import SlackToolkit
from typing import Optional

# Importación condicional para manejar posibles errores
try:
    from langgraph.prebuilt import create_react_agent
    langgraph_available = True
except ImportError:
    langgraph_available = False
    print("Advertencia: langgraph no está disponible. Se usará solo el LLM básico.")

# ARQUITECTURA: Carga de variables de entorno
load_dotenv()

# ARQUITECTURA: Configuración de credenciales
slack_token = os.getenv("SLACK_USER_TOKEN")
groq_api_key = os.getenv("GROQ_API_KEY")
channel_id = os.getenv("SLACK_CHANNEL_ID")

# Validación de credenciales
if not slack_token or not groq_api_key or not channel_id:
    raise ValueError("Faltan credenciales: Verifica SLACK_USER_TOKEN, GROQ_API_KEY y SLACK_CHANNEL_ID")

# ARQUITECTURA: Configuración del modelo LLM de Groq
llm = ChatGroq(model="llama3-8b-8192")

# Configuración del cliente de Slack
slack_client = WebClient(token=slack_token)

# Inicialización del toolkit de Slack y agente si está disponible
if langgraph_available:
    try:
        # Configuración del toolkit de Slack
        toolkit = SlackToolkit()
        tools = toolkit.get_tools()
        
        # Crear el agente con las herramientas de Slack
        agent_executor = create_react_agent(llm, tools)
        print("Agente de Slack inicializado con herramientas avanzadas.")
    except Exception as e:
        langgraph_available = False
        print(f"Error al inicializar el agente: {e}")
        print("Se usará el modo básico sin herramientas avanzadas.")

# Configuración de Flask para eventos de Slack
app = Flask(__name__)

def send_message_to_channel(channel_id, message):
    """Envía un mensaje a un canal específico de Slack."""
    try:
        slack_client.chat_postMessage(
            channel=channel_id,
            text=message
        )
    except SlackApiError as e:
        print(f"Error enviando mensaje: {e}")

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """Manejador de eventos de Slack"""
    data = request.json
    
    # Manejar desafío de URL (necesario para configuración inicial)
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})
    
    # Procesar solo eventos de mensaje en canales
    if "event" in data and data["event"]["type"] == "message":
        event = data["event"]
        
        # Ignorar mensajes de bots para evitar bucles
        if "bot_id" not in event:
            # Procesar el mensaje según el modo disponible
            if langgraph_available:
                # Modo avanzado con agente y herramientas
                result = agent_executor.invoke(
                    {"messages": [("user", f"Procesa este mensaje de Slack: {event['text']}")]}
                )
                response_text = result['messages'][-1][1]
            else:
                # Modo básico solo con LLM
                response = llm.invoke(f"Procesa este mensaje de Slack: {event['text']}")
                response_text = response.content
            
            # Enviar respuesta al canal
            send_message_to_channel(event['channel'], response_text)
    
    return jsonify({"status": "ok"})

def run_slack_listener():
    """Iniciar el servidor de escucha de eventos de Slack"""
    app.run(host='0.0.0.0', port=3000)

# Ejemplo de uso
if __name__ == "__main__":
    # Iniciar el servidor de eventos de Slack
    run_slack_listener()
