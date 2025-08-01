import subprocess

def run_amass_scan(target, scan_args):
    args = ["amass", "enum", "-d", target]
    if scan_args.get("brute_force"):
        args.append("-brute")
    if scan_args.get("passive"):
        args.append("-passive")
    timeout = int(scan_args.get("timeout", 180))
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        results = [line for line in proc.stdout.split("\n") if line.strip()]
        return {"scan_type": "amass", "results": results}
    except subprocess.TimeoutExpired:
        return {"error": f"Amass scan timed out after {timeout}s"}
    except Exception as e:
        return {"error": f"Amass scan failed: {str(e)}"}
