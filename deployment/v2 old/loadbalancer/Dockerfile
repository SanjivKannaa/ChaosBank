FROM nginx:latest

# Install Python & dependencies
RUN apt update && apt install -y python3 python3-pip python3-venv

# Set up virtual environment
RUN python3 -m venv /app/venv
COPY app /app

ENV PATH="/app/venv/bin:$PATH"

# Copy Nginx config
COPY nginx/nginx.conf /etc/nginx/nginx.conf
COPY nginx/backends.conf /etc/nginx/conf.d/backends.conf
COPY nginx/frontends.conf /etc/nginx/conf.d/frontends.conf

# Copy Python script and install dependencies
WORKDIR /app
RUN pip install boto3

# Start Nginx and Python script
CMD ["sh", "-c", "/app/venv/bin/python3 update_nginx.py & nginx -g 'daemon off;'"]
