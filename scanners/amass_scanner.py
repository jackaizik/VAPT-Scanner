import subprocess

def run_amass_scan(target):
    # Only works with domains (not IPs)
    if target.startswith('http://') or target.startswith('https://'):
        target = target.split("://")[1]
    try:
        cmd = ["amass", "enum", "-d", target]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        results = [line for line in proc.stdout.split("\n") if line.strip()]
        return {"scan_type": "amass", "results": results}
    except Exception as e:
        return {"error": f"Amass scan failed: {str(e)}"}
