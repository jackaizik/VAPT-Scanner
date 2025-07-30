import requests, time

def run_zap_scan(target):
    zap_api = 'http://localhost:8080'
    zap_url = f'{zap_api}/JSON/ascan/action/scan/'
    params = {'url': target}

    # Start ZAP active scan
    try:
        response = requests.get(zap_url, params=params)
        response.raise_for_status()
        scan_id = response.json().get('scan')
        if scan_id is None:
            return {'error': 'ZAP did not return a scan ID. Is the target URL reachable?'}
    except Exception as e:
        return {'error': f'Failed to start scan: {str(e)}'}

    # Monitor scan progress with status checks
    status_url = f'{zap_api}/JSON/ascan/view/status/?scanId={scan_id}'

    while True:
        try:
            status_response = requests.get(status_url)
            status_response.raise_for_status()
            status_value = status_response.json().get('status')
            if status_value is None:
                return {'error': f'Failed to get status from ZAP. Check the target or ZAP logs.'}
            status = int(status_value)
        except Exception as e:
            return {'error': f'Scan status check failed: {str(e)}'}

        if status >= 100:
            break
        print(f'Scan progress: {status}%')
        time.sleep(5)

    # Get alerts
    try:
        alerts_url = f'{zap_api}/JSON/core/view/alerts/?baseurl={target}'
        alerts = requests.get(alerts_url).json()
    except Exception as e:
        return {'error': f'Failed to fetch alerts: {str(e)}'}

    return {'scan_type': 'zap', 'results': alerts}
