import subprocess, json

def run_nuclei_scan(target, scan_args):
    nuclei_args = scan_args.get('args', '') if scan_args else ''
    timeout = int(scan_args.get('timeout', 120)) if scan_args else 120
    cmd = ["nuclei", "-u", target, "-json"]
    if nuclei_args:
        cmd += nuclei_args.split()
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        results = []
        for line in proc.stdout.strip().split("\n"):
            try:
                results.append(json.loads(line))
            except Exception:
                continue
        return {"scan_type": "nuclei", "results": results}
    except Exception as e:
        return {"error": f"Nuclei scan failed: {str(e)}"}
