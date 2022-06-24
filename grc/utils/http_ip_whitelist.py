import ipaddress
from flask import abort, request, Response
from grc.utils.logger import LogLevel, Logger


class HttpIPWhitelist:
    def __init__(self, app=None):
        self.app = app
        self.ip_whitelist = app.config['IP_WHITELIST']
        #request.remote_addr = request.remote_addr
        self.logger = Logger()

        app.before_request_funcs.setdefault(None, []).append(self._handler)

    def _handler(self):
        def check_ip(ip):
            if '/' in ip:
                if ipaddress.ip_address(request.remote_addr) in ipaddress.ip_network(ip):
                    return True
            elif ipaddress.ip_address(ip) == ipaddress.ip_address(request.remote_addr):
                return True
            return False

        try:
            if ',' in self.ip_whitelist:
                ipaddresses = self.ip_whitelist.split(',')
                for ip in ipaddresses:
                    if check_ip(ip):
                        return

            elif check_ip(self.ip_whitelist):
                return

        except:
            pass

        self.logger.log(LogLevel.WARN, f"A user has attempted to access the site from an unauthorised ip address ({request.remote_addr})")
        response = Response('', 418)

        abort(response)
