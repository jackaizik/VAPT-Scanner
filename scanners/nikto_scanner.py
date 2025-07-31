import subprocess

def run_nikto_scan(target, scan_args):
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    timeout = int(scan_args.get('timeout', 180)) if scan_args else 180
    try:
        cmd = ["nikto", "-h", target, "-nointeractive"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"scan_type": "nikto", "results": proc.stdout}
    except Exception as e:
        return {"error": f"Nikto scan failed: {str(e)}"}
