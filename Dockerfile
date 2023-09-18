FROM python:3.11.5-slim
WORKDIR /usr/src/app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=app.py:create_app
ENV FLASK_ENV=development
CMD ["flask", "run", "--host=0.0.0.0"]