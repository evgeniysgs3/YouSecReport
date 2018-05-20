import ipaddress

class ToolAdapter(object):
    '''Abstract class which describes all necessary methods for a scan tool adapter'''
    def start(self):
        raise NotImplemented

    def stop(self):
        raise NotImplemented

    def status(self):
        raise NotImplemented

    def kill(self):
        raise NotImplemented

    def get_result_json(self):
        raise NotImplemented

    def is_valid_ip(self, ip):
        try:
            ip_ = ipaddress.ip_address(ip)
            return True
        except ValueError:
            return False