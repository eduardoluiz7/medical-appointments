## Medical Appointments

### Estrutura do Projeto
```bash
medical_appointments/
├── api/
│   ├── appointments_api/
│   ├   ├───settings.py
│   └── ...
├── frontend/
├── docker-compose.yml
├── Dockerfile
├── README.md
├── .gitignore
```

### Configuração e Execução
  #### Usando docker-compose
  - Construir e iniciar os containers
  ```bash
    docker-compose up --build
  ```
  - Parar os containers
  ```bash
    docker-compose down
  ```
  - Rodar migrações
  ```bash
    docker-compose exec api python manage.py migrate
    docker-compose exec frontend python manage.py migrate
  ```

### Dependências
  #### Requisitos
  - Docker
  - Docker Compose

