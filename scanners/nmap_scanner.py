import nmap

def run_nmap_scan(target):
    scanner = nmap.PortScanner()
    scanner.scan(hosts=target, arguments='-sV -Pn -T4')
    
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
