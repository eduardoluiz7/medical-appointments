# Use a imagem base oficial do Python
FROM python:3.9-slim

# Defina o diretório de trabalho
WORKDIR /app

# Instale as dependências do sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev

# Instale as dependências do projeto
ARG requirements_file
COPY ${requirements_file} /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copie os arquivos do projeto
ARG project_dir
COPY ${project_dir} /app

# Exponha a porta 8000
EXPOSE 8000
EXPOSE 8001

# Comando padrão para iniciar o servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000", "0.0.0.0:8001"]