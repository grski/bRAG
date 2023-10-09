# Business Assistant API

This project contains a microservice that implements common tools, patterns, and technologies used at AI/LLM projects.
## Development Lifecycle



### Getting Started


## Style & Formatting

Style & formatting checks are run on every commit as part of the CI Pipeline

On the python side the project is setup to use the following linting and formatting tools:
- [black](https://black.readthedocs.io/)
- [ruff](https://beta.ruff.rs/docs/)

If you have this project up and running locally, you can run these checks:
```bash
make lint
```

## Project structure

The file structure is:
```
 |-- app/  # Main codebase directory
 |---- chat/
 |------ __init__.py
 |------ api.py
 |------ constants.py
 |------ message.py
 |------ models.py
 |------ streams.py
 
 |---- core/
 |------ __init__.py
 |------ api.py
 |------ logs.py
 |------ middlewares.py
 |------ models.py
 
 |---- __init__.py
 |---- db.py
 |---- main.py
 
 
 |-- db/  # Database/migration/pugsql related code
 |---- migrations/
 |---- queries/
 |---- schema.sql
 
 |-- settings/  # Settings files directory
 |---- base.py
 |---- gunicorn.conf.py
 |-- tests/  # Main tests directory
 |-- requirements/
 
 |-- .dockerignore
 |-- .env.example
 |-- .gitignore
 |-- pre-commit-config.yaml  # for linting in during development
 |-- docker-compose.yml
 |-- Dockerfile
 |-- Makefile  # useful shortcuts
 |-- README.md
```

## Required actions to get this running

- Secrets present in the `.github/workflows/ci.yml` file need to be added to the repository secrets on Github.
   - `DB_ENDPOINT`
   - `DB_NAME`
   - `DB_PASSWORD`
   - `DB_PORT`
   - `DB_USERNAME`

## Running the project

To run this locally, run:
```bash
docker-compose up
```
If you'd like to force rebuild of images, do:
```bash
docker-compose up --build
```
to run in deattached mode (services will run in the background):
```bash
docker-compose up -d
```

The recommended approach is however, to run the other services in docker, but the api locally:
```bash
docker-compose up -d database
```
then later
```bash
poetry run gunicorn -c settings/gunicorn.conf.py app.main:app
```
Or just 
```bash
make run
```
