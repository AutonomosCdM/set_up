Desarrolla un agente inteligente basado en Python que se integre con Google Workspace (Gmail, Calendar, Drive, Sheets, Docs) utilizando Groq LLM para procesamiento de lenguaje natural.

Este desarrollo deberá ser una "plantilla" para conectar este agente o agentes a otros sistemas que requieran los servicios de google workspace.

 El agente debe:

1. Arquitectura y Componentes:
   - Crear una estructura modular con separación clara de responsabilidades
   - Implementar un cliente para la API de Google Workspace
   - Desarrollar un cliente para Groq LLM
   - Diseñar una interfaz para sistemas externos
   - Implementar gestión de contexto de conversación

2. Funcionalidades de Google Workspace:
   - Gmail: Leer, clasificar y responder correos electrónicos
   - Calendar: Crear, modificar y consultar eventos
   - Drive: Buscar, organizar y compartir archivos
   - Sheets: Leer, analizar y modificar hojas de cálculo
   - Docs: Crear, editar y formatear documentos

3. Integración con LLM:
   - Procesar consultas en lenguaje natural
   - Generar respuestas contextuales
   - Extraer información relevante de documentos
   - Resumir contenido de correos y documentos
   - Sugerir acciones basadas en el contexto

4. Seguridad y Autenticación:
   - Implementar OAuth 2.0 para autenticación con Google
   - Gestionar tokens de acceso y refresco
   - Manejar permisos granulares para cada servicio
   - Proteger datos sensibles

5. Despliegue y Operación:
   - Variables de entorno para credenciales
   - Logging estructurado
   - Monitoreo de rendimiento

El código debe seguir buenas prácticas de desarrollo, incluir documentación completa y estar preparado para despliegue en producción.
