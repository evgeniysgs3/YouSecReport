from adapters.api import ToolAdapter
from libnmap.process import NmapProcess
from libnmap.parser import NmapParser, NmapParserException
from json import dumps
from time import sleep
from log.log_config import log, configlogging

logger = configlogging()

class NmapAdapter(ToolAdapter):
    @log(logger)
    def __init__(self, ip, commandline=None):
        if self.is_valid_ip(ip):
            self.ip = ip
        else:
            raise ValueError

        if commandline:
            self.commandline = commandline
        else:
            self.commandline = '-sV'
        self.nmproc = NmapProcess(self.ip, self.commandline)

    @log(logger)
    def start(self):
        logger.info('nmap started on IP {}'.format(self.ip))
        rc = self.nmproc.run_background()
        if self.nmproc.stderr:
            logger.critical('nmap has failed: {0}'.format(self.nmproc.stderr))
            print('nmap scan has failed:', self.nmproc.stderr)

    def status(self):
        if self.nmproc.is_running():
            return 'running: {0}%'.format(self.nmproc.progress)
        else:
            if self.nmproc.has_failed():
                return 'failed'
            elif self.nmproc.is_successful():
                return 'finished (successfully)'
            else:
                return 'stopped'

    @log(logger)
    def stop(self):
        if self.nmproc.is_running():
            self.nmproc.stop()

    @log(logger)
    def get_result_json(self):
        report = None
        try:
            report = NmapParser.parse(self.nmproc.stdout)
        except NmapParserException as e:
            logger.critical("Exception raised while parsing scan: {0}".format(e.msg))
            print("Exception raised while parsing scan: {0}".format(e.msg))
            return None
        report_dict = {}
        report_dict['starttime'] = report.started
        report_dict['endtime'] = report.endtime
        report_dict['host'] = self.ip
        host = report.hosts[0]
        report_dict['hoststatus'] = host.status
        services = []
        for serv in host.services:
            service = {}
            service['port'] = serv.port
            service['protocol'] = serv.protocol
            service['state'] = serv.state
            service['service'] = serv.service
            if len(serv.banner):
                service['banner'] = serv.banner
            if len(serv.cpelist):
                cpe = {}
                cpe['part'] = serv.cpelist[0].get_part()
                cpe['vendor'] = serv.cpelist[0].get_vendor()
                cpe['product'] = serv.cpelist[0].get_product()
                cpe['version'] = serv.cpelist[0].get_version()
                cpe['update'] = serv.cpelist[0].get_update()
                cpe['edition'] = serv.cpelist[0].get_edition()
                cpe['language'] = serv.cpelist[0].get_language()
                service['cpe'] = cpe
            services.append(service)
        report_dict['services'] = services
        json_data = dumps(report_dict)
        return json_data

if __name__ == '__main__':
    adapter = NmapAdapter('127.0.0.1')
    adapter.start()
    while('running' in adapter.status()):
        print(adapter.status())
        sleep(1)
    print(adapter.get_result_json())