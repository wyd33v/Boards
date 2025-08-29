FROM python:3.12-slim


# permissions and nonroot user for tightened security
RUN useradd --create-home appuser

# create /app directory and chown to to node user or else it will be owned by root
RUN mkdir -p /app && chown appuser:appuser /app
WORKDIR /app

RUN apt-get update && apt upgrade -y

COPY --chown=appuser:appuser . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

USER appuser

CMD [ "fastapi", "dev", "app.py"]
