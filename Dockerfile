# Use a base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code into the container
COPY . .

# Set the environment variable to run the Flask app on port 247
ENV FLASK_APP=app.py
ENV FLASK_RUN_PORT=247

# Expose the port
EXPOSE 247

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=247"]