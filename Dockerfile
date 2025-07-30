FROM kalilinux/kali-rolling

RUN apt update && apt install -y \
    python3 \
    python3-pip \
    nmap \
    zaproxy \
    git \
    && apt clean

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000 8080

CMD zaproxy -daemon -host 0.0.0.0 -port 8080 -config api.disablekey=true & python3 app.py
