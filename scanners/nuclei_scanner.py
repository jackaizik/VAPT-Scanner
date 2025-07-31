import subprocess

def run_nuclei_scan(target):
    # Basic nuclei scan, save output as JSON for easy parsing
    try:
        cmd = ["nuclei", "-u", target, "-json"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        results = []
        for line in proc.stdout.strip().split("\n"):
            try:
                # nuclei outputs one JSON object per line
                import json
                results.append(json.loads(line))
            except Exception:
                continue
        return {"scan_type": "nuclei", "results": results}
    except Exception as e:
        return {"error": f"Nuclei scan failed: {str(e)}"}