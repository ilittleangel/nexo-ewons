import json
import logging
import time
import sys
import requests.exceptions

import utils.m2web_api
from utils.elastic import index
from utils.logging import init_logging, close_logging, failure_logging
from utils.helpers import csv_to_dict, prepare, counter
from settings import ROOT_DIR, sleep_seconds


def _accountinfo():
    res_info = utils.m2web_api.getaccountinfo()
    if res_info.status_code == 200:
        logger.debug(f"res_info.status_code={res_info.status_code}")
        accountinfo = res_info.json()
        logger.debug(json.dumps(accountinfo, indent=4))
        return accountinfo
    else:
        failure_logging(f"Something wrong with `getaccountinfo()`: {res_info}", logger='pipeline')


def _ewons(accountinfo):
    for pool in accountinfo['pools']:
        id_installation = pool['id']
        res_ewons = utils.m2web_api.getewons(id_installation)
        if res_ewons.status_code == 200:
            logger.debug(f"res_ewons.status_code={res_ewons.status_code}")
            ewons = res_ewons.json()
            logger.debug(json.dumps(ewons, indent=4))
            return ewons
        else:
            failure_logging(f"Something wrong with `getewons()`: {res_ewons}", logger='pipeline')


def _tags(ewons, count):
    for ewon in ewons['ewons']:
        name = ewon['name']  # it could be 'encodedName'
        res = utils.m2web_api.gettags(name)
        if res.status_code == 200:
            tags = res.text
            doc = prepare(csv_to_dict(tags))
            logger.debug(f"Indexing tags: {doc}")
            if index(doc=doc, doc_type_mode="tags"):
                logger.info("Tags ingestion SUCCEDEDD")
                failures = 0
                return failures, counter(init_val=0), res
            else:
                failure_logging("Tags ingestion FAILED because TAGs was not indexed", logger='pipeline')
        else:
            failures = next(count)
            return failures, count, res


# noinspection PyShadowingBuiltins
def _action_failure(params):
    failure_logging(message=params['msg'], logger='pipeline', exit=params['exit'], level=params['level'])
    logger.info(f"sleeping {params['sleep_time']} seconds")
    time.sleep(params['sleep_time'])


def _actions_against_failure(failures, res):
    message_warn = f"Something wrong with `gettags()`: {res}"
    message_error = f"Tags ingestion FAILED because too many failures: failures=`{failures}`"
    switcher = {
        1: {'sleep_time': 10, 'exit': False, 'msg': message_warn,  'level': "WARN"},
        2: {'sleep_time': 10, 'exit': False, 'msg': message_warn,  'level': "WARN"},
        3: {'sleep_time': 20, 'exit': False, 'msg': message_warn,  'level': "WARN"},
        4: {'sleep_time': 20, 'exit': False, 'msg': message_warn,  'level': "WARN"},
        5: {'sleep_time': 0,  'exit': True,  'msg': message_error, 'level': "ERROR"}
    }
    params = switcher.get(failures, lambda: "Invalid num of failures")
    _action_failure(params)


def main():

    logger.info("START tags ingestion")
    # noinspection PyBroadException
    try:

        accountinfo = _accountinfo()
        ewons = _ewons(accountinfo)
        count = counter(init_val=0)
        while True:
            failures, count, res = _tags(ewons, count)
            logger.debug(f"num failures=`{failures}`")
            if failures > 0:
                _actions_against_failure(failures, res)
            time.sleep(sleep_seconds)

    except requests.exceptions.ConnectionError as ce:
        logger.error(f"Something wrong connecting to ewon cloud: {ce}")
        time.sleep(30)
        main()
    except Exception as e:
        logger.error(f"Something wrong happens but it is unknown: {e}")
        sys.exit(1)


if __name__ == '__main__':
    init_logging(f'{ROOT_DIR}/logs/ewons')
    logger = logging.getLogger('pipeline')
    main()
    close_logging()
