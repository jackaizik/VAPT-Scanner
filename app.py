from flask import Flask, request, render_template, jsonify
from scan_manager import start_scan, stop_scan
from scanners.nmap_scanner import run_nmap_scan
from scanners.zap_scanner import run_zap_scan
from scanners.nuclei_scanner import run_nuclei_scan
from scanners.nikto_scanner import run_nikto_scan
from scanners.amass_scanner import run_amass_scan
import json, os
from multiprocessing import Manager

app = Flask(__name__)
CONFIG_PATH = 'args.conf'
manager = Manager()
result_registry = manager.dict()

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

def save_result(scanner_type, result):
    result_registry[scanner_type] = result

def execute_scan(scan_type, target, config):
    if scan_type == 'nmap':
        result = run_nmap_scan(target, config.get('nmap', {}))
    elif scan_type == 'zap':
        result = run_zap_scan(target, config.get('zap', {}))
    elif scan_type == 'nuclei':
        result = run_nuclei_scan(target, config.get('nuclei', {}))
    elif scan_type == 'nikto':
        result = run_nikto_scan(target, config.get('nikto', {}))
    elif scan_type == 'amass':
        result = run_amass_scan(target, config.get('amass', {}))
    else:
        result = {"error": "Invalid scan type"}
    save_result(scan_type, result)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json(force=True)
    scan_type = data.get('scan_type')
    target = data.get('target')
    config = load_config()
    result_registry[scan_type] = None
    # Each scanner runs in a background process for stop support
    start_scan(scan_type, execute_scan, scan_type, target, config)
    return jsonify({"status": "started"})

@app.route('/scan_status/<scanner_type>', methods=['GET'])
def scan_status(scanner_type):
    # Return result if available, else status
    result = result_registry.get(scanner_type)
    if result is not None:
        return jsonify(result)
    else:
        return jsonify({"status": "running"})

@app.route('/stop_scan', methods=['POST'])
def stop_scan_route():
    data = request.get_json(force=True)
    scan_type = data.get('scan_type')
    stopped = stop_scan(scan_type)
    if stopped:
        save_result(scan_type, {"error": "Scan was stopped by user."})
    return jsonify({"status": "stopped" if stopped else "not running"})

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
