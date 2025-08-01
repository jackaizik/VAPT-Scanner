import subprocess

def run_nmap_scan(target, scan_args):
    args = ["nmap"]
    # Build up arguments based on config
    if scan_args.get("os_detection"):
        args.append("-O")
    if scan_args.get("service_version"):
        args.append("-sV")
    if scan_args.get("no_ping"):
        args.append("-Pn")
    if scan_args.get("aggressive"):
        args.append("-A")
    args.append(f"--top-ports={scan_args.get('top_ports', 100)}")
    args.append(f"-T{scan_args.get('timing_template', 4)}")
    if scan_args.get("custom_args"):
        args.extend(scan_args.get("custom_args").split())
    args.append(target)
    timeout = int(scan_args.get("timeout", 60))
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=timeout)
        return {"scan_type": "nmap", "results": proc.stdout}
    except subprocess.TimeoutExpired:
        return {"error": f"Nmap scan timed out after {timeout}s"}
    except Exception as e:
        return {"error": f"Nmap scan failed: {str(e)}"}
