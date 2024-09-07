FROM python:3.11
WORKDIR /atelier

COPY ./requirements.txt /atelier/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /atelier/requirements.txt

COPY ./dev_certs/key.pem /atelier/key.pem
COPY ./dev_certs/cert.pem /atelier/cert.pem
COPY ./packages/gallery /atelier/gallery

CMD ["uvicorn", "gallery.main:app", "--host", "0.0.0.0", "--port", "33333", "--ssl-keyfile", "/atelier/key.pem", "--ssl-certfile", "/atelier/cert.pem", "--workers", "4"]
