import subprocess

def run_amass_scan(target, scan_args):
    if target.startswith('http://') or target.startswith('https://'):
        target = target.split("://")[1]
    timeout = int(scan_args.get('timeout', 180)) if scan_args else 180
    try:
        cmd = ["amass", "enum", "-d", target]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        results = [line for line in proc.stdout.split("\n") if line.strip()]
        return {"scan_type": "amass", "results": results}
    except Exception as e:
        return {"error": f"Amass scan failed: {str(e)}"}
