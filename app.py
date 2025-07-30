from flask import Flask, request, jsonify, render_template, redirect, url_for
from scanners.nmap_scanner import run_nmap_scan
from scanners.zap_scanner import run_zap_scan

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan', methods=['POST'])
def scan():
    scan_type = request.form.get('scan_type')
    target = request.form.get('target')

    if scan_type == 'nmap':
        results = run_nmap_scan(target)
    elif scan_type == 'zap':
        results = run_zap_scan(target)
    else:
        results = {"error": "Invalid scan type"}

    return render_template('index.html', results=results)

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        nmap_args = request.form.get('nmap_args')
        zap_url = request.form.get('zap_url')
        # Save settings in a simple file or session (left basic for MVP)
        with open('settings.txt', 'w') as f:
            f.write(f"{nmap_args}\n{zap_url}")
        return redirect(url_for('home'))
    return render_template('settings.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
