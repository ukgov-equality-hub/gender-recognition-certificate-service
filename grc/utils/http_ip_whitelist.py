import ipaddress
from flask import abort, request, Response
from grc.utils.logger import LogLevel, Logger


class HttpIPWhitelist:
    def __init__(self, app=None):
        self.app = app
        self.ip_whitelist = app.config['IP_WHITELIST']
        self.logger = Logger()

        app.before_request_funcs.setdefault(None, []).append(self._handler)

    def _handler(self):
        try:
            if ',' in self.ip_whitelist:
                ipaddresses = self.ip_whitelist.split(',')
                for ip in ipaddresses:
                    if self.check_ip(ip):
                        return

            elif self.check_ip(self.ip_whitelist):
                return

        except:
            pass

        self.logger.log(LogLevel.WARN, f"A user has attempted to access the site from an unauthorised ip address ({self.get_client_ip()})")
        response = Response('', 401)

        abort(response)

    def get_client_ip(self):
        return request.access_route[0]  # request.remote_addr

    def check_ip(self, ip):
        client_ip = self.get_client_ip()
        if '/' in ip:
            if ipaddress.ip_address(client_ip) in ipaddress.ip_network(ip):
                return True
        elif ipaddress.ip_address(ip) == ipaddress.ip_address(client_ip):
            return True
        return False
