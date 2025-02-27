# Agente LangChain para Slack

## Descripción general

Este proyecto implementa un agente simple basado en LangChain que se conecta con Slack para leer y escribir mensajes.

## Componentes principales

- **Conector de Slack**: Gestiona la comunicación con la API de Slack
- **Agente LLM**: Utiliza Groq para procesar y generar respuestas

## Configuración

### Instalación local

1. Instalar dependencias: `pip install -r requirements.txt`
2. Configurar variables de entorno en `.env`:
   - `SLACK_USER_TOKEN`: Token de bot de Slack
   - `GROQ_API_KEY`: API key de Groq
   - `SLACK_CHANNEL_ID`: ID del canal de Slack

### Configuración con Docker

1. Asegúrate de tener Docker y Docker Compose instalados
2. Copiar `.env.example` a `.env` y configurar las variables
3. Construir y ejecutar el contenedor:
   ```bash
   docker-compose up --build
   ```

## Ejecución

### Ejecución local

Ejecutar con: `python agent.py`

### Ejecución con Docker

- Iniciar: `docker-compose up`
- Detener: `docker-compose down`
- Reiniciar: `docker-compose restart`

## Estructura del proyecto

- `agent.py`: Código principal del agente
- `Dockerfile`: Configuración de construcción del contenedor
- `docker-compose.yml`: Configuración de Docker Compose
- `.env`: Configuración de credenciales
- `requirements.txt`: Dependencias del proyecto

## Decisiones de diseño

Consultar `DESIGN_DECISIONS.md` para más detalles sobre las decisiones arquitectónicas.

## Notas de desarrollo

- El agente está configurado para reiniciarse automáticamente
- Los logs se pueden ver con `docker-compose logs`
- Para desarrollo, los volúmenes permiten cambios en caliente
