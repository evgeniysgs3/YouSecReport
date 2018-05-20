import os
import shlex
import subprocess
from ..api import ToolAdapter
from . import nikto_setup

tool_full_path = nikto_setup.PATH_NIKTO_TOOL


class NiktoAdapter(ToolAdapter):
    """>>> a = adapters.NiktoAdapter("127.0.0.1", ["5000"])"""
    CODING = "UTF-8"

    def __init__(self, host, ports, max_time_per_port=600):
        self.ports = ports
        self.max_scan_time = max_time_per_port * len(self.ports)
        args_str = "-h {host} -p {ports} -ask no -maxtime {max_time}".format(
            host=host,
            ports=",".join(map(str, ports)),
            max_time=self.max_scan_time,
            )
        args = shlex.split(args_str)
        self.nktproc = subprocess.Popen([tool_full_path, *args], stdout=subprocess.PIPE)

    def start(self):
        try:
            report, error = self.nktproc.communicate(timeout=self.max_scan_time)
        except subprocess.TimeoutExpired:
            self.nktproc.kill()
            report, error = self.nktproc.communicate()

        self.report = report
        self.error = error

    def status(self):
        return self.nktproc.returncode

    def kill(self):
        self.nktproc.kill()

    def get_result_json(self):
        """не успел"""
        return str(self.report, self.CODING)
