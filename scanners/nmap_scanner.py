import nmap

def run_nmap_scan(target, scan_args):
    scanner = nmap.PortScanner()
    args = scan_args.get('args', '-sV -Pn -T4') if scan_args else '-sV -Pn -T4'
    timeout = int(scan_args.get('timeout', 60)) if scan_args else 60
    # Note: python-nmap doesn't support timeout directly, so you may want to run with subprocess for real timeouts.
    scanner.scan(hosts=target, arguments=args)
    results = []
    for host in scanner.all_hosts():
        host_info = {
            'host': host,
            'status': scanner[host].state(),
            'open_ports': []
        }
        for proto in scanner[host].all_protocols():
            ports = scanner[host][proto].keys()
            for port in ports:
                host_info['open_ports'].append({
                    'port': port,
                    'service': scanner[host][proto][port]['name'],
                    'version': scanner[host][proto][port]['version']
                })
        results.append(host_info)
    return {'scan_type': 'nmap', 'results': results}
