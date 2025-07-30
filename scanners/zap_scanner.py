import requests, time

def run_zap_scan(target):
    zap_api = 'http://localhost:8080'
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    # 1. "Access" the URL so it's in the Sites tree
    try:
        access_url = f'{zap_api}/JSON/core/action/accessUrl/'
        resp = requests.get(access_url, params={'url': target, 'followRedirects': True})
        resp.raise_for_status()
        time.sleep(2)  # Let ZAP process
    except Exception as e:
        return {'error': f'Failed to access URL in ZAP: {str(e)}'}

    # 2. (Optional) Spider the target to discover more URLs
    try:
        spider_url = f'{zap_api}/JSON/spider/action/scan/'
        resp = requests.get(spider_url, params={'url': target})
        resp.raise_for_status()
        scan_id = resp.json().get('scan')
        # Wait for spider to finish (poll status)
        spider_status_url = f'{zap_api}/JSON/spider/view/status/?scanId={scan_id}'
        while True:
            status = int(requests.get(spider_status_url).json().get('status'))
            if status >= 100:
                break
            time.sleep(2)
    except Exception as e:
        return {'error': f'Spidering failed: {str(e)}'}

    # 3. Start Active Scan
    zap_url = f'{zap_api}/JSON/ascan/action/scan/'
    params = {'url': target}
    try:
        response = requests.get(zap_url, params=params)
        response.raise_for_status()
        scan_id = response.json().get('scan')
        if scan_id is None:
            return {'error': 'ZAP did not return a scan ID after spidering.'}
    except Exception as e:
        return {'error': f'Failed to start scan: {str(e)}'}

    # 4. Monitor scan progress
    status_url = f'{zap_api}/JSON/ascan/view/status/?scanId={scan_id}'
    while True:
        status_value = requests.get(status_url).json().get('status')
        if status_value is None:
            return {'error': f'Failed to get status from ZAP. Check the target or ZAP logs.'}
        status = int(status_value)
        if status >= 100:
            break
        time.sleep(5)

    # 5. Get alerts
    try:
        alerts_url = f'{zap_api}/JSON/core/view/alerts/?baseurl={target}'
        alerts = requests.get(alerts_url).json()
    except Exception as e:
        return {'error': f'Failed to fetch alerts: {str(e)}'}

    return {'scan_type': 'zap', 'results': alerts}
