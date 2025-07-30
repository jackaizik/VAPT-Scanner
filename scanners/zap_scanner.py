import requests, time

def run_zap_scan(target):
    zap_api = 'http://localhost:8080'
    zap_url = f'{zap_api}/JSON/ascan/action/scan/'
    params = {'url': target}

    # Start ZAP active scan
    response = requests.get(zap_url, params=params)
    scan_id = response.json().get('scan')

    status_url = f'{zap_api}/JSON/ascan/view/status/?scanId={scan_id}'

    # Monitor scan progress
    while True:
        status = int(requests.get(status_url).json().get('status'))
        if status >= 100:
            break
        print(f'Scan progress: {status}%')
        time.sleep(10)

    # Get alerts
    alerts_url = f'{zap_api}/JSON/core/view/alerts/?baseurl={target}'
    alerts = requests.get(alerts_url).json()

    return {'scan_type': 'zap', 'results': alerts}
