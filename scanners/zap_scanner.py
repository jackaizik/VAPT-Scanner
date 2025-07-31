import requests, time

def run_zap_scan(target, scan_args):
    zap_api = 'http://localhost:8080'
    timeout = int(scan_args.get('timeout', 180)) if scan_args else 180
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target

    try:
        access_url = f'{zap_api}/JSON/core/action/accessUrl/'
        resp = requests.get(access_url, params={'url': target, 'followRedirects': True}, timeout=timeout)
        resp.raise_for_status()
        time.sleep(2)
    except Exception as e:
        return {'error': f'Failed to access URL in ZAP: {str(e)}'}

    try:
        spider_url = f'{zap_api}/JSON/spider/action/scan/'
        resp = requests.get(spider_url, params={'url': target}, timeout=timeout)
        resp.raise_for_status()
        scan_id = resp.json().get('scan')
        spider_status_url = f'{zap_api}/JSON/spider/view/status/?scanId={scan_id}'
        start_time = time.time()
        while True:
            status = int(requests.get(spider_status_url).json().get('status'))
            if status >= 100 or (time.time() - start_time > timeout):
                break
            time.sleep(2)
    except Exception as e:
        return {'error': f'Spidering failed: {str(e)}'}

    zap_url = f'{zap_api}/JSON/ascan/action/scan/'
    params = {'url': target}
    try:
        response = requests.get(zap_url, params=params, timeout=timeout)
        response.raise_for_status()
        scan_id = response.json().get('scan')
        if scan_id is None:
            return {'error': 'ZAP did not return a scan ID after spidering.'}
    except Exception as e:
        return {'error': f'Failed to start scan: {str(e)}'}

    status_url = f'{zap_api}/JSON/ascan/view/status/?scanId={scan_id}'
    start_time = time.time()
    while True:
        status_value = requests.get(status_url).json().get('status')
        if status_value is None:
            return {'error': f'Failed to get status from ZAP.'}
        status = int(status_value)
        if status >= 100 or (time.time() - start_time > timeout):
            break
        time.sleep(5)

    try:
        alerts_url = f'{zap_api}/JSON/core/view/alerts/?baseurl={target}'
        alerts = requests.get(alerts_url).json()
    except Exception as e:
        return {'error': f'Failed to fetch alerts: {str(e)}'}

    return {'scan_type': 'zap', 'results': alerts}
