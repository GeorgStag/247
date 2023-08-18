# base image
FROM python:3.8

# working directory
WORKDIR /app

# python requirements to the container
COPY requirements.txt .

# dependencies
RUN pip install --no-cache-dir -r requirements.txt

# all files inside the directory copied
COPY . .

# flask app runs on port 247
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=247
EXPOSE 247

# flask app run command
CMD ["flask", "run", "--host=0.0.0.0", "--port=247"]
