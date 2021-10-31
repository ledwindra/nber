import os
from random import randint

class Proxy:

    def proxy(self):
        try:
            proxy_user = os.environ['PROXY_USER']
            proxy_password = os.environ['PROXY_PASSWORD']
            proxy_port = os.environ['PROXY_PORT']
            return proxy_user, proxy_password, proxy_port
        except KeyError:
            pass

    def get_host(self):
        file_name = 'host.txt'
        if os.path.exists(file_name):
            host = open(file_name, 'r').read().split('\n')
            index = randint(0, len(host)-1)

            return host[index]

    def get_proxy(self):
        proxy = self.proxy()
        try:
            return f'socks5h://{proxy[0]}:{proxy[1]}@{self.get_host()}:{proxy[2]}'
        except TypeError:
            return None

