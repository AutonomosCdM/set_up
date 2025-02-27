# ARQUITECTURA: Imagen base de Python para entorno de ejecución
# CONTEXTO: Usar imagen slim de Python para mantener el contenedor ligero
# RESTRICCIONES: Compatibilidad con las dependencias del proyecto
FROM python:3.10-slim

# Establecer variables de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias del sistema y de Python
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar el resto del código de la aplicación
COPY . .

# ARQUITECTURA: Configuración de ejecución del agente
# CONTEXTO: Ejecutar el script principal del agente
# RESTRICCIONES: Usar variables de entorno para configuración
CMD ["python", "agent.py"]

# Exponer puerto para eventos de Slack
EXPOSE 3000
