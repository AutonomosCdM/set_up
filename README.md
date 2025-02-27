# Slack Agent con LLM

## Descripción
Este proyecto implementa un agente de Slack que utiliza un modelo de lenguaje (LLM) para procesar y responder a mensajes en canales de Slack. El agente está construido con Flask, Docker y utiliza el LLM de Groq para generar respuestas.

## Arquitectura
El sistema consta de los siguientes componentes:
- **Servidor Flask**: Recibe eventos de Slack y maneja las respuestas
- **LLM de Groq**: Procesa los mensajes y genera respuestas inteligentes
- **Docker**: Contiene la aplicación en un entorno aislado
- **ngrok**: Expone el servidor local a Internet para recibir eventos de Slack

## Requisitos
- Python 3.10+
- Docker y Docker Compose
- Cuenta de Slack con permisos para crear aplicaciones
- Cuenta de Groq para acceder a su API de LLM
- ngrok para exponer el servidor local

## Configuración

### Variables de entorno
Crea un archivo `.env` con las siguientes variables:
```
SLACK_USER_TOKEN=xoxp-tu-token-de-slack
GROQ_API_KEY=tu-api-key-de-groq
SLACK_CHANNEL_ID=ID-del-canal-de-slack
```

### Configuración de Slack
1. Crea una aplicación en [api.slack.com/apps](https://api.slack.com/apps)
2. En "OAuth & Permissions", añade los siguientes scopes:
   - `channels:history`
   - `channels:read`
   - `chat:write`
3. En "Event Subscriptions":
   - Activa los eventos
   - Configura la URL de Request (usando ngrok): `https://tu-url-ngrok.app/slack/events`
   - Suscribe a los eventos de bot: `message.channels`

## Instalación y ejecución

### Usando Docker
```bash
# Construir la imagen
docker-compose build

# Ejecutar el contenedor
docker-compose up
```

### Exponer el servidor con ngrok
```bash
ngrok http 3000
```

## Uso
Una vez configurado, el agente responderá automáticamente a los mensajes enviados en el canal de Slack configurado. Simplemente envía un mensaje en el canal y el agente procesará la solicitud y responderá.

## Archivos principales
- `agent.py`: Implementación principal del agente
- `test_slack_connection.py`: Script para probar la conexión con Slack
- `Dockerfile` y `docker-compose.yml`: Configuración de Docker
- `requirements.txt`: Dependencias de Python

## Fecha de última actualización
27 de febrero de 2025, 12:11 (UTC-3, hora de Chile)
