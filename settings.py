import configparser
from os.path import dirname, abspath


ROOT_DIR = dirname(abspath(__file__))
NO_PROXY = {'http': None, 'https': None}

# config.ini
config = configparser.ConfigParser()
config.read('config.ini')

# db
DB_LOCATION = "./db/ewons.db"
APPID = "app-nexo-1"

# ewon
acc_credentials = config['ACC_CREDENTIALS']
ins_credentials = config['INS_CREDENTIALS']
EWON_ROOT = "https://m2web.talk2m.com/t2mapi"
t2maccount = acc_credentials['t2maccount']
t2musername = acc_credentials['t2musername']
t2mpassword = acc_credentials['t2mpassword']
t2mdeveloperid = acc_credentials['t2mdeveloperid']
t2mdeviceusername = ins_credentials['t2mdeviceusername']
t2mdevicepassword = ins_credentials['t2mdevicepassword']

# elastic
elastic = config['ELASTIC']
ESNODES = str(elastic['esnodes']).split(',')
INDEX_NAME = "ewon-tags".lower()
USER = ""
PASS = ""
try:
    USER = elastic['user']
    PASS = elastic['pass']
except KeyError:
    pass
ENABLE_INDEX = elastic.getboolean('enable_index', fallback=True)


# elastic cloud
elastic_cloud = config['ELASTIC_CLOUD']
ESNODES_cloud = str(elastic_cloud['esnodes']).split(',')
USER_cloud = elastic_cloud['user']
PASS_cloud = elastic_cloud['pass']
ENABLE_INDEX_cloud = elastic_cloud.getboolean('enable_index', fallback=True)

# logging
logging = config['LOGGING']
log_level = logging['level']

# pipeline
pipeline = config['PIPELINE']
sleep_seconds = int(pipeline['sleep_seconds'])

