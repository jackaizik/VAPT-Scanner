FROM kalilinux/kali-rolling

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

# Create and activate venv
RUN python3 -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000 8080

# Explicitly start services within a shell
CMD ["/bin/bash", "-c", "source venv/bin/activate && zaproxy -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true & python app.py"]
