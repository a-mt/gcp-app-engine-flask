FROM python:3.12.2-alpine

COPY src/requirements.txt .
RUN pip install -r requirements.txt

ENV HOST=0.0.0.0
ENV PORT=8080
EXPOSE 8080
WORKDIR /srv/www

ENTRYPOINT ["python", "main.py"]