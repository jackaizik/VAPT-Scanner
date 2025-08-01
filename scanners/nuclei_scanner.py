import subprocess, json

def run_nuclei_scan(target, scan_args):
    args = ["nuclei", "-u", target, "-json"]
    if scan_args.get("rate_limit"):
        args.extend(["-rl", str(scan_args.get("rate_limit"))])
    if scan_args.get("severity"):
        args.extend(["-severity", ",".join(scan_args.get("severity"))])
    if scan_args.get("templates"):
        for tmpl in scan_args.get("templates"):
            args.extend(["-tags", tmpl])
    if scan_args.get("exclude_templates"):
        for tmpl in scan_args.get("exclude_templates"):
            args.extend(["-etags", tmpl])
    timeout = int(scan_args.get("timeout", 120))
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        results = []
        for line in proc.stdout.strip().split("\n"):
            try:
                results.append(json.loads(line))
            except Exception:
                continue
        return {"scan_type": "nuclei", "results": results}
    except subprocess.TimeoutExpired:
        return {"error": f"Nuclei scan timed out after {timeout}s"}
    except Exception as e:
        return {"error": f"Nuclei scan failed: {str(e)}"}
