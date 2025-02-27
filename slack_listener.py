from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Cargar variables de entorno
load_dotenv()

# Configuración de cliente de Slack
slack_token = os.getenv("SLACK_USER_TOKEN")
channel_id = os.getenv("SLACK_CHANNEL_ID")
client = WebClient(token=slack_token)

app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    """
    Manejador básico de eventos de Slack
    """
    data = request.json
    
    # Manejar desafío de URL (necesario para configuración inicial)
    if "challenge" in data:
        return jsonify({"challenge": data["challenge"]})
    
    # Procesar solo eventos de mensaje en canales
    if "event" in data and data["event"]["type"] == "message":
        event = data["event"]
        
        # Ignorar mensajes de bots para evitar bucles
        if "bot_id" not in event:
            try:
                # Enviar mensaje de prueba de vuelta al canal
                client.chat_postMessage(
                    channel=event["channel"],
                    text=f"Recibí tu mensaje: {event['text']}"
                )
            except SlackApiError as e:
                print(f"Error enviando mensaje: {e}")
    
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=3000, debug=True)
