FROM python:3.11.3 as requirements
WORKDIR /tmp

ARG POETRY_VERSION=1.3.2
ENV PATH /root/.local/bin:$PATH
RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=$POETRY_VERSION python -

COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes



FROM python:3.11.3 as server
RUN curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64 && \
    chmod +x /usr/local/bin/dbmate
WORKDIR /project
COPY --from=requirements /tmp/requirements.txt /project/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /project/requirements.txt
COPY . /project
CMD ["bash", "-c", "dbmate up && gunicorn -c settings/gunicorn.conf.py app.main:app"]
