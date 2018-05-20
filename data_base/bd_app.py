import configparser
import datetime
from pymongo import MongoClient, DESCENDING


config = configparser.ConfigParser()
config.read("settings.secret")
USER = config["mongo_connect"]["User"]
PASSWORD = config["mongo_connect"]["Password"]
IP_BASE = config["mongo_connect"]["IP"]


class Client_DB:
    iw = {"login": "login",  # init_words
          "password": "password",
          "mail": "mail",
          "target": "target",
          "cr_time": "creation_time",
          }

    def __init__(self):
        """создает подключение к базе и коллекции"""
        client = MongoClient('mongodb://{}:{}@{}'.format(USER, PASSWORD, IP_BASE), connect=False)
        self.db = client.test_db
        self.collection = self.db.client_coll

    def add_client(self, login, passwd, mail, target=[]):
        """добавляет юзера в базу"""
        if self.get_client(login):
            return False

        to_base = {self.iw["login"]: login,
                   self.iw["password"]: passwd,
                   self.iw["mail"]: mail,
                   self.iw["target"]: target,
                   self.iw["cr_time"]: datetime.datetime.utcnow(),
                   }
        return self.collection.insert_one(to_base).acknowledged

    def get_client(self, login):
        return self.collection.find_one({self.iw["login"]: login}, {'_id': False})

    def get_all_client(self):
        """достать всех клиентов"""
        return [cl for cl in self.collection.find()]

    def get_mail(self, login):
        """достать почту клиента"""
        person = self.get_client(login)
        if person:
            return person[self.iw["mail"]]

    def get_target(self, login):
        """возвращает список списков с ip"""
        person = self.get_client(login)
        if person:
            return person[self.iw["target"]]

    def add_target(self, login, target):
        """добавить цель, не может быть больше 5"""
        if len(self.get_target(login)) >= 5 or target in self.get_target(login):
            return False
        return self.collection.update_one({self.iw["login"]: login}, {"$push": {self.iw["target"]: target}}).modified_count

    def del_target(self, login, target):
        """убрать цель"""
        return self.collection.update_one({self.iw["login"]: login}, {"$pull": {self.iw["target"]: target}}).modified_count

    def validate_pswd(self, login, pswd):
        """проверить пароль"""
        person = self.get_client(login)
        if person:
            return person[self.iw["password"]] == pswd


class Report_DB:

    iw = {"login": "login",  # init words
          "cr_time": "creation_time",
          "target": "target",  # так обозначаются сканируемые хосты
          "report": "report",
          "report_type": "report_type",
          }

    report_type_allow = ["nmap", "nikto"]

    def __init__(self):
        """создает подключение к базе и коллекции"""
        client = MongoClient('mongodb://{}:{}@{}'.format(USER, PASSWORD, IP_BASE), connect=False)
        self.db = client.test_db
        self.collection = self.db.report_coll

    def add_report(self, login, target, report_type, report, time=False):
        """добавить отчет в базу"""

        if report_type not in self.report_type_allow:
            raise "Incorrect report type"

        to_base = {self.iw["login"]: login,
                   self.iw["cr_time"]: time if time else datetime.datetime.utcnow(),
                   self.iw["target"]: target,
                   self.iw["report"]: report,
                   self.iw["report_type"]: report_type,
                   }
        return self.collection.insert_one(to_base).acknowledged

    def get_report(self, **kwargs):
        """достать отчеты по логину юзера (login), по цели(target), по времени(day_before) - это фильтры к поиску"""
        filter_dict = {self.iw[k]: v for k, v in kwargs.items() if k in self.iw}

        if "day_before" in kwargs:
            end = datetime.datetime.utcnow()
            start = end - datetime.timedelta(days=kwargs["day_before"])
            filter_dict[self.iw["cr_time"]] = {'$gte': start, '$lt': end}

        return [report for report in self.collection.find(filter_dict, {'_id': False})]

    def get_last_report(self, **kwargs):
        """достать последний отчет юзера и/или цели"""
        filter_dict = {self.iw[k]: v for k, v in kwargs.items() if k in self.iw}

        try:
            report = self.collection.find(filter_dict, {'_id': False}).sort(self.iw["cr_time"], DESCENDING).limit(1).next()
        except StopIteration:
            return False
        else:
            return report


def check_report_time(day_before=7):
    """Возвращает словарь __логин: сисок хостов__ на которые нет отчетов day_before дней"""
    t_now = datetime.datetime.utcnow()
    t_last = t_now - datetime.timedelta(day_before)

    to_ret = dict()

    users = Client_DB()
    report = Report_DB()
    for user in users.get_all_client():
        login = user[users.iw["login"]]
        for target in user[users.iw["target"]]:
            if type(target) != str:
                # users.del_target(login, target)  # чистка
                continue
            last_report = report.get_last_report(login=login, target=target)
            if not last_report or last_report[report.iw["cr_time"]] < t_last:
                to_ret.setdefault(login, []).append(target)
    return to_ret
