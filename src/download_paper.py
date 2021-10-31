import os
import requests
import traceback
from proxy import Proxy

if __name__ == "__main__":
    nber_id = os.environ['NBER_ID']
    proxy = Proxy().get_proxy()
    attempt = 0
    status_code = None
    while attempt < 3:
        try:
            url = f'https://www.nber.org/system/files/working_papers/w{nber_id}/w{nber_id}.pdf'
            response = requests.get(url, proxies={'https': proxy}, timeout=5)
            status_code = response.status_code
            if status_code in [403, 404]:
                break
            with open(f'paper/{nber_id}.pdf', 'wb') as file:
                file.write(response.content)
        except Exception:
            print(f'{traceback.print_exc()}: {nber_id}')
            pass
        
        attempt += 1
