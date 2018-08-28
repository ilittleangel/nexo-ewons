import configparser
from os.path import dirname, abspath

config = configparser.ConfigParser()
config.read('config.ini')
credentials = config['CREDENTIALS']

ROOT_DIR = dirname(dirname(abspath(__file__)))
DB_LOCATION = "./db/ewons.db"
EWON_ROOT = "https://m2web.talk2m.com/t2mapi"
APPID = "app-nexo-1"
t2maccount = credentials['t2maccount']
t2musername = credentials['t2musername']
t2mpassword = credentials['t2mpassword']
t2mdeveloperid = credentials['t2mdeveloperid']


def counter(init_val=0, step=1):
    counter_val = init_val
    while True:
        counter_val += step
        yield counter_val
