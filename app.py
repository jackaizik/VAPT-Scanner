from flask import Flask, request, render_template
from scanners.nmap_scanner import run_nmap_scan
from scanners.zap_scanner import run_zap_scan

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/scan/nmap', methods=['POST'])
def nmap_scan():
    target = request.form.get('target')
    results = run_nmap_scan(target)
    return render_template('index.html', result=results)

@app.route('/scan/zap', methods=['POST'])
def zap_scan():
    target = request.form.get('target')
    results = run_zap_scan(target)
    return render_template('index.html', result=results)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
