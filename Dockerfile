FROM kalilinux/kali-rolling

# Install system dependencies
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nmap \
    zaproxy \
    git \
    && apt clean

WORKDIR /app
COPY . .

# Set up a Python virtual environment and install dependencies
RUN python3 -m venv venv \
    && . venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 5000 8080

# Activate virtual environment and start ZAP and Flask application
CMD . venv/bin/activate && \
    zaproxy -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true & \
    python3 app.py
