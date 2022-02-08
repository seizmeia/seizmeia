FROM python:3.10-slim-buster as server

RUN apt-get -y update && apt-get install -y --no-install-recommends git

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENTRYPOINT [ "uvicorn", "server.__main__:app", "--host", "0.0.0.0" ]