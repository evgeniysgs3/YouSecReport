import configparser


class Config:

    def __init__(self, file_config):
        self.f_config = file_config

    def read_config(self):
        """Read configuration file"""
        config = configparser.ConfigParser()
        config.read(self.f_config)
        return config

    def get_auth_for_send_email(self):
        """Return auth settingth for email sender report"""
        config = self.read_config()
        email_auth_section = config['EMAILAUTH']
        return email_auth_section['login'], email_auth_section['password']


if __name__ == '__main__':
    config = Config('config.ini')
    print(config.get_auth_for_send_email())
