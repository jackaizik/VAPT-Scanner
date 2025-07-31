from flask import Flask, request, render_template, jsonify
from scanners.nmap_scanner import run_nmap_scan
from scanners.zap_scanner import run_zap_scan
from scanners.nuclei_scanner import run_nuclei_scan
from scanners.nikto_scanner import run_nikto_scan
from scanners.amass_scanner import run_amass_scan
import json
import os

app = Flask(__name__)
CONFIG_PATH = 'args.conf'

def load_config():
    # Load or create with defaults
    if not os.path.exists(CONFIG_PATH):
        default_config = {
            "nmap": {"args": "-sV -Pn -T4", "timeout": 60},
            "zap": {"timeout": 180},
            "nuclei": {"args": "", "timeout": 120},
            "nikto": {"timeout": 180},
            "amass": {"timeout": 180}
        }
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config
    with open(CONFIG_PATH, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.get_json(force=True)
        scan_type = data.get('scan_type')
        target = data.get('target')
        config = load_config()

        if scan_type == 'nmap':
            results = run_nmap_scan(target, config.get('nmap', {}))
        elif scan_type == 'zap':
            results = run_zap_scan(target, config.get('zap', {}))
        elif scan_type == 'nuclei':
            results = run_nuclei_scan(target, config.get('nuclei', {}))
        elif scan_type == 'nikto':
            results = run_nikto_scan(target, config.get('nikto', {}))
        elif scan_type == 'amass':
            results = run_amass_scan(target, config.get('amass', {}))
        else:
            results = {"error": "Invalid scan type"}
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

@app.route('/load_config', methods=['GET'])
def load_config_route():
    config = load_config()
    return jsonify(config)

@app.route('/save_config', methods=['POST'])
def save_config_route():
    config = request.get_json(force=True)
    save_config(config)
    return jsonify({"status": "saved"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
