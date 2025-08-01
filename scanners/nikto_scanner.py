import subprocess

def run_nikto_scan(target, scan_args):
    args = ["nikto", "-h", target, "-nointeractive"]
    if scan_args.get("ssl"):
        args.append("-ssl")
    if scan_args.get("useragent"):
        args.extend(["-useragent", scan_args.get("useragent")])
    if scan_args.get("use_plugins"):
        for plugin in scan_args.get("use_plugins"):
            args.extend(["-Plugins", plugin])
    timeout = int(scan_args.get("timeout", 180))
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return {"scan_type": "nikto", "results": proc.stdout}
    except subprocess.TimeoutExpired:
        return {"error": f"Nikto scan timed out after {timeout}s"}
    except Exception as e:
        return {"error": f"Nikto scan failed: {str(e)}"}
