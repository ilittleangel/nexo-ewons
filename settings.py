import configparser
from os.path import dirname, abspath

from utils.helpers import is_int

ROOT_DIR = dirname(abspath(__file__))
NO_PROXY = {'http': None, 'https': None}

# config.ini
config = configparser.ConfigParser()
config.read('config.ini')
acc_credentials = config['ACC_CREDENTIALS']
ins_credentials = config['INS_CREDENTIALS']
elastic = config['ELASTIC']
logging = config['LOGGING']
pipeline = config['PIPELINE']

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

# elastic
ESNODES = str(elastic['esnodes']).split(',')
INDEX_NAME = "ewon-tags".lower()
USER = ""
PASS = ""
try:
    USER = elastic['user']
    PASS = elastic['pass']
except KeyError:
    pass

# logging
log_level = logging['level']

# pipeline
sleep_seconds = int(pipeline['sleep_seconds'])

