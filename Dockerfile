FROM python:3.10-slim-buster as base

RUN apt-get -y update && apt-get install -y --no-install-recommends git

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


FROM base AS production

COPY . .

EXPOSE 8000
ENTRYPOINT [ "uvicorn", "seizmeia.server:app", "--host", "0.0.0.0" ]


FROM base AS development

COPY . .

RUN pip install -e .

EXPOSE 8000
ENTRYPOINT [ "python", "seizmeia/__main__.py" ]