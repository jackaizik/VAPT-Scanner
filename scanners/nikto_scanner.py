import subprocess

def run_nikto_scan(target):
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    try:
        cmd = ["nikto", "-h", target, "-nointeractive"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        return {"scan_type": "nikto", "results": proc.stdout}
    except Exception as e:
        return {"error": f"Nikto scan failed: {str(e)}"}