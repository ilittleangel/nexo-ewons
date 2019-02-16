import json
import logging
import time
import requests.exceptions

import utils.m2web_api
from utils.elastic import index
from utils.logging import init_logging, close_logging, failure_logging
from utils.helpers import csv_to_dict, prepare, counter
from settings import ROOT_DIR, sleep_seconds


def _accountinfo():
    res_info = utils.m2web_api.getaccountinfo()
    if res_info.status_code == 200:
        logger.info(f"res_info.status_code={res_info.status_code}")
        accountinfo = res_info.json()
        logger.info(json.dumps(accountinfo, indent=4))
        return accountinfo
    else:
        failure_logging(f"Something wrong with `getaccountinfo()`: {res_info}", logger='pipeline')


def _ewons(accountinfo):
    for pool in accountinfo['pools']:
        id_installation = pool['id']
        res_ewons = utils.m2web_api.getewons(id_installation)
        if res_ewons.status_code == 200:
            logger.info(f"res_ewons.status_code={res_ewons.status_code}")
            ewons = res_ewons.json()
            logger.info(json.dumps(ewons, indent=4))
            return ewons
        else:
            failure_logging(f"Something wrong with `getewons()`: {res_ewons}", logger='pipeline')


def _tags(ewons, count):
    for ewon in ewons['ewons']:
        name = ewon['name']  # it could be 'encodedName'
        res = utils.m2web_api.gettags(name)
        if res.status_code == 200:
            ewon_failures = 0
            tags = res.text
            doc = prepare(csv_to_dict(tags))
            return ewon_failures, counter(init_val=0), index(doc)
        else:
            ewon_failures = next(count)
            return ewon_failures, count, res


# noinspection PyShadowingBuiltins
def _action_failure(params):
    failure_logging(message=params['msg'], logger='pipeline', exit=params['exit'], level=params['level'])
    logger.info(f"sleeping {params['sleep_time']} seconds")
    time.sleep(params['sleep_time'])


def _actions_against_failure(failures, res):
    message_error1 = f"Something wrong with `gettags()`: {res}: failures=`{failures}`"
    message_error2 = f"Tags ingestion FAILED because too many failures: failures=`{failures}`"
    if 0 < failures < 6:
        params = {'sleep_time': 10, 'exit': False, 'msg': message_error1, 'level': "ERROR"}
    else:
        params = {'sleep_time': 60, 'exit': False, 'msg': message_error2, 'level': "ERROR"}

    _action_failure(params)


def main():
    import setproctitle as sp
    sp.setproctitle('pipeline.py')

    logger.info("START tags ingestion")
    failures = 0
    # noinspection PyBroadException
    try:

        logger.info(f"Requesting for Account Info ...")
        accountinfo = _accountinfo()
        logger.info(f"Requesting for Ewons Intallations ...")
        ewons = _ewons(accountinfo)
        count = counter(init_val=0)
        while True:
            logger.info(f"Requesting for Tags ...")
            failures, count, res = _tags(ewons, count)
            logger.info(f"num failures=`{failures}`")
            if failures > 0:
                _actions_against_failure(failures, res)
            time.sleep(sleep_seconds)

    except requests.exceptions.RequestException as re:
        logger.error(f"Something wrong connecting to ewon cloud: {re}: failures=`{failures}`")
        time.sleep(30)
        main()


if __name__ == '__main__':
    init_logging(f'{ROOT_DIR}/logs/ewons')
    logger = logging.getLogger('pipeline')
    main()
    close_logging()
