import configparser
config = configparser.ConfigParser()
config['EMAILAUTH'] = {'Login': 'yoursecreport@gmail.com',
                      'Password': '***********'}
with open('config.ini', 'w') as configfile:
    config.write(configfile)