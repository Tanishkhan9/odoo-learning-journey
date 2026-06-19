# Docker Setup

This project can be run locally with Docker using the official Odoo image and a PostgreSQL container.

## What this setup gives you

- Odoo in a reproducible containerized environment
- PostgreSQL with a persistent volume
- A simple path for onboarding and demos
- A consistent base for future CI and testing work

## Prerequisites

- Docker Desktop or Docker Engine
- Docker Compose
- Git

## Suggested project files

Create this file at the repository root:

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: odoo
    volumes:
      - odoo-db-data:/var/lib/postgresql/data

  odoo:
    image: odoo:16.0
    depends_on:
      - db
    ports:
      - "8069:8069"
    environment:
      HOST: db
      USER: odoo
      PASSWORD: odoo
    volumes:
      - ./modules:/mnt/extra-addons
      - odoo-web-data:/var/lib/odoo

volumes:
  odoo-db-data:
  odoo-web-data:
```

## Run it

```bash
docker compose up -d
```

Then open:

- Odoo web UI: http://localhost:8069

## Install the addons

1. Enable developer mode in Odoo.
2. Update the app list.
3. Install `course_management` first.
4. Install `student_management` after that.

## Notes

- The sample compose file uses official images only.
- For production, set stronger passwords and store them in environment files or secrets.
- If you want database backups, add a scheduled backup container or bind mount strategy.
