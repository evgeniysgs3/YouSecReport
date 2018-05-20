from datetime import datetime, date, time
from flask_login import UserMixin, login_user
from werkzeug.security import check_password_hash
from app import login_manager
from app.database import db, rdb


@login_manager.user_loader
def load_user(username):
    u = db.get_client(username)
    if not u:
        return None
    return User(u['login'])


class User(UserMixin):
    def __init__(self, username):
        self._user = db.get_client(username)
        self._name = self._user['login']
        self._email = self._user['mail']
        self._hash_pwd = self._user['password']
        self._services = self._user['target']

    def get_id(self):
        return self._name

    def check_password(self, password):
        return check_password_hash(self._hash_pwd, password)

    def get_last_scan_date(self):
        dic_serv_data_last_scan = {}
        for serv in self._services:
            lst_report = rdb.get_last_report(login=self._name, target=serv)
            if not lst_report:
                dic_serv_data_last_scan.setdefault(serv, 'don`t scan')
            else:
                dic_serv_data_last_scan[serv] = lst_report[rdb.iw['cr_time']].strftime("%d-%b-%Y %H:%M")
        return dic_serv_data_last_scan

