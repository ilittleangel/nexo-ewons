import configparser
from os.path import dirname, abspath

ROOT_DIR = dirname(abspath(__file__))

# config.ini
config = configparser.ConfigParser()
config.read('config.ini')
acc_credentials = config['ACC_CREDENTIALS']
ins_credentials = config['INS_CREDENTIALS']

# db
DB_LOCATION = "./db/ewons.db"
APPID = "app-nexo-1"

# ewon
EWON_ROOT = "https://m2web.talk2m.com/t2mapi"
t2maccount = acc_credentials['t2maccount']
t2musername = acc_credentials['t2musername']
t2mpassword = acc_credentials['t2mpassword']
t2mdeveloperid = acc_credentials['t2mdeveloperid']
t2mdeviceusername = ins_credentials['t2mdeviceusername']
t2mdevicepassword = ins_credentials['t2mdevicepassword']
