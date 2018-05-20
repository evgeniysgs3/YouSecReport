from adapters.nmap.nmapadapter import NmapAdapter
from threading import Thread
from time import sleep
from queue import Queue

class ScanTask(Thread):
    """
    ip - host ip to scan
    out_queue - Queue class to return scan results in format ('tool_name', json_report)
    """
    def __init__(self, ip, out_queue):
        Thread.__init__(self)
        self.setDaemon(True)
        self.ip = ip
        self.out_queue = out_queue

    def run(self):
        try:
            nmap = NmapAdapter(self.ip)
        except ValueError:
            #TODO log
            return
        nmap.start()
        while ('running' in nmap.status()): # waiting nmap to finish TODO: log
            sleep(3)
        nmap_report = nmap.get_result_json()
        self.out_queue.put(('nmap', nmap_report))

if __name__ == '__main__':
    out_queue = Queue()
    task = ScanTask('127.0.0.1', out_queue)
    task2 = ScanTask('127.0.0.1', out_queue)
    task.start()
    sleep(5)
    task2.start()
    task.join()
    task2.join()
    print(out_queue.get())
    print(out_queue.get())
    out_queue.task_done()