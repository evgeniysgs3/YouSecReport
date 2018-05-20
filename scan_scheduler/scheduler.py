import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_base.bd_app import check_report_time, Client_DB, Report_DB
from datetime import datetime
from time import sleep
from queue import Queue
from sw_controller.scan_task import ScanTask
from threading import Thread
from report_generator import generate_report, pdf
from report_sendler.sendler import send_mail


DAYS_FROM_LAST_SCAN = 7
clientdb = Client_DB()
send_queue = Queue()

class Scan():
    def __init__(self, login, target, type_name, report_json):
        self.login = login
        self.target = target
        self.type_name = type_name
        self.report_json = report_json

    def get_html_report(self):
        if self.report_json:
            return generate_report(self.type_name, self.report_json)

    def get_pdf_report(self):
        filename = '{0}-{1}-{date:%Y-%m-%d_%H-%M-%S}.pdf'.format(self.target.replace('.', '-'),
                                                                 self.type_name, date=datetime.now())
        path = os.path.join(os.getcwd(), 'log', 'pdf_reports')
        if pdf.convert_html_to_pdf(self.get_html_report(), os.path.join(path, filename)):
            return path, filename
        else:
            return None

class ReadyScanProcessor(Thread):
    def __init__(self, send_queue):
        Thread.__init__(self)
        self.setDaemon(True)
        self.reportdb = Report_DB()
        self.send_queue = send_queue

    def run(self):
        while True:
            if not self.send_queue.empty():
                scan = send_queue.get()
                self.reportdb.add_report(login=scan.login, target=scan.target,
                                         report_type=scan.type_name, report=scan.report_json)
                path, filename = scan.get_pdf_report()
                try:
                    send_mail(clientdb.get_mail(scan.login), path, filename)
                except Exception as e:
                    print(e)
                send_queue.task_done()
            else:
                sleep(5)

def get_hosts_to_scan(days):
    #if __debug__:  # run with -O
    #    print('----DEBUG: LOCALHOST IS USED----')
    #    return [('debug', '127.0.0.1')]  # change 'debug' to your email
    logins_and_hosts_dict = check_report_time(days)
    hosts = []
    for key, value in logins_and_hosts_dict.items():  # convert {'login', ['ip', 'ip2']} to (login, ip) tuple
        hosts.extend(zip([key] * len(value), value))  # and add to list, to avoid emb. loop later
    return hosts

if __name__ == '__main__':
    ready_scan_thread = ReadyScanProcessor(send_queue)
    ready_scan_thread.start()

    while True:
        # Получить список хостов для сканирования
        hosts = get_hosts_to_scan(DAYS_FROM_LAST_SCAN)
        # Для каждого хоста провести скан
        scan_queue = Queue()
        for host in hosts:
            print('Scanning {0} for user {1} started'.format(host[1], host[0]))
            scan = ScanTask(host[1], scan_queue)
            scan.start()
            scan.join() # т.к. пока 1 сервер, пусть сканятся по очереди
            print('Scanning {0} for user {1} finished'.format(host[1], host[0]))
            for scan in iter(scan_queue.get, None):
                # Результат скана сохранить в базу и отправить на почту
                scan_result = Scan(login=host[0], target=host[1], type_name=scan[0], report_json=scan[1])
                send_queue.put(scan_result)
                print(host[1], scan[0], scan[1])
                scan_queue.task_done()
        # Заснуть, если возможно
        sleep(1*60)
