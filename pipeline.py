import json
import logging
import time
import requests.exceptions

import utils.m2web_api
from utils.elastic import index
from utils.logging import init_logging, close_logging, failure_logging
from utils.helpers import csv_to_dict, prepare, counter
from settings import ROOT_DIR, sleep_seconds
from settings import ESNODES, USER, PASS, ENABLE_INDEX
from settings import ESNODES_cloud, USER_cloud, PASS_cloud, ENABLE_INDEX_cloud


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
            ewon_failures = 0
            tags = res.text
            doc = prepare(csv_to_dict(tags))
            logger.debug(f"Indexing tags: {doc}")
            res = index(doc, "tags", USER, PASS, ESNODES, ENABLE_INDEX)
            logger.info(f"Indexing on {ESNODES}: {res}")
            res_cloud = index(doc, "tags", USER_cloud, PASS_cloud, ESNODES_cloud, ENABLE_INDEX_cloud)
            logger.info(f"Indexing on {ESNODES_cloud}: {res_cloud}")
            results = [("on-premise", res), ("cloud", res_cloud)]
            return ewon_failures, counter(init_val=0), results
        else:
            ewon_failures = next(count)
            return ewon_failures, count, res


# noinspection PyShadowingBuiltins
def _action_failure(params):
    failure_logging(message=params['msg'], logger='pipeline', exit=params['exit'], level=params['level'])
    logger.info(f"sleeping {params['sleep_time']} seconds")
    time.sleep(params['sleep_time'])


def _actions_against_failure(failures, res):
    message_error1 = f"Something wrong with `gettags()`: {res}"
    message_error2 = f"Tags ingestion FAILED because too many failures: failures=`{failures}`"
    if 0 < failures < 6:
        params = {'sleep_time': 10, 'exit': False, 'msg': message_error1, 'level': "ERROR"}
    else:
        params = {'sleep_time': 60, 'exit': False, 'msg': message_error2, 'level': "ERROR"}

    _action_failure(params)


def main():

    logger.info("START tags ingestion")
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
            logger.debug(f"num failures=`{failures}`")
            if failures > 0:
                _actions_against_failure(failures, res)
            time.sleep(sleep_seconds)

    except requests.exceptions.RequestException as re:
        logger.error(f"Something wrong connecting to ewon cloud: {re}")
        time.sleep(30)
        main()


if __name__ == '__main__':
    init_logging(f'{ROOT_DIR}/logs/ewons')
    logger = logging.getLogger('pipeline')
    main()
    close_logging()
