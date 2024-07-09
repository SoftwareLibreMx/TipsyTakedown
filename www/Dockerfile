FROM python:3.12

# Set the working directory
WORKDIR /www

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Change to the working directory
RUN cd /www

# Copy the current directory contents into the container at /www
ENTRYPOINT ["gunicorn", "app:flask_app", "--config", "/www/gunicorn_config.py"]

HEALTHCHECK --interval=10s --timeout=3s CMD curl --fail http://localhost:8000/health|| exit 1
