FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

ENV FLASK_APP=app.py

CMD [ "python", "app.py" ]
