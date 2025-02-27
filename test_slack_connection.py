import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Cargar variables de entorno
load_dotenv()

# Obtener credenciales
slack_token = os.getenv("SLACK_USER_TOKEN")
channel_id = os.getenv("SLACK_CHANNEL_ID")

def test_slack_connection():
    """
    Prueba básica de conexión con Slack
    """
    try:
        # Crear cliente de Slack
        client = WebClient(token=slack_token)
        
        # Intentar obtener información del canal
        result = client.conversations_info(channel=channel_id)
        
        # Imprimir información básica del canal
        print("Conexión exitosa con Slack!")
        print(f"Nombre del canal: {result['channel']['name']}")
        
        # Intentar enviar un mensaje de prueba
        response = client.chat_postMessage(
            channel=channel_id,
            text="¡Hola! Este es un mensaje de prueba desde el agente de Slack. Conexión establecida correctamente. 🤖"
        )
        print("Mensaje de prueba enviado exitosamente.")
        
        return True
    except SlackApiError as e:
        print(f"Error en la conexión con Slack: {e}")
        return False

if __name__ == "__main__":
    test_slack_connection()
