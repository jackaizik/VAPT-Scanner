from flask import Flask, request, render_template, jsonify
from scanners.nmap_scanner import run_nmap_scan
from scanners.zap_scanner import run_zap_scan
from scanners.nuclei_scanner import run_nuclei_scan
from scanners.nikto_scanner import run_nikto_scan
from scanners.amass_scanner import run_amass_scan


app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    try:
        data = request.get_json(force=True)
        scan_type = data.get('scan_type')
        target = data.get('target')

        if scan_type == 'nmap':
            results = run_nmap_scan(target)
        elif scan_type == 'zap':
            results = run_zap_scan(target)
        elif scan_type == 'nuclei':
            results = run_nuclei_scan(target)
        elif scan_type == 'nikto':
            results = run_nikto_scan(target)
        elif scan_type == 'amass':
            results = run_amass_scan(target)
        else:
            results = {"error": "Invalid scan type"}
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": f"Internal server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
