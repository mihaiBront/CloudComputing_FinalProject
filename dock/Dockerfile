# 1. Usar Ubuntu como imagen base
FROM ubuntu:22.04

# 2. Configurar argumentos y variables de entorno
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH

# 3. Instalar dependencias: git, python3, pip y venv
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    && apt-get clean

# 4. Clonar el repositorio
WORKDIR /app
RUN git clone https://github.com/mihaiBront/CloudComputing_FinalProject.git .

# 5. Crear entorno virtual usando el script de ".scripts"
RUN python3 -m venv venv && \
    /bin/bash -c "source venv/bin/activate && bash .scripts/env-setup.bash"

# 6. Instalar dependencias del proyecto
#COPY requirements.txt .
#RUN . venv/bin/activate && pip install -r requirements.txt

# 7. Exponer el puerto en el que correrá la app
EXPOSE 5000

# 8. Comando para arrancar la app
#CMD ["/bin/bash", "-c", ". venv/bin/activate && flask run --host=0.0.0.0 --port=5000"]
RUN source venv/bin/activate
RUN flask run --host=0.0.0.0 --port=5000
