import json
import logging
import utils.m2web_api

from utils.elastic import create_connection, index
from utils.logging import init_logging, close_logging
from utils.helpers import csv_to_dict, prepare
from settings import ROOT_DIR


def main():

    es, health = create_connection()
    logger.debug(f"Connected to Elasticsearch")
    logger.debug(f"Elasticsearch health: {health}")

    res_info = utils.m2web_api.getaccountinfo()
    if res_info.status_code == 200:

        logger.debug(f"res_info.status_code={res_info.status_code}")
        accountinfo = res_info.json()
        logger.debug(json.dumps(accountinfo, indent=4))

        for pool in accountinfo['pools']:
            id_installation = pool['id']
            res_ewons = utils.m2web_api.getewons(id_installation)
            if res_ewons.status_code == 200:

                logger.debug(f"res_ewons.status_code={res_ewons.status_code}")
                ewons = res_ewons.json()
                logger.debug(json.dumps(ewons, indent=4))

                for ewon in ewons['ewons']:
                    name = ewon['name']  # it could be 'encodedName'
                    res_tag = utils.m2web_api.gettags(name)
                    if res_tag.status_code == 200:
                        tags = res_tag.text
                        doc = prepare(csv_to_dict(tags))
                        logger.debug(doc)
                        index(es, doc=doc, doc_type_mode="tags")

                    else:
                        logger.error(f"Something wrong with `gettags()`: {res_tag}")
            else:
                logger.error(f"Something wrong with `getewons()`: {res_ewons}")
    else:
        logger.error(f"Something wrong with `getaccountinfo()`: {res_info}")


if __name__ == '__main__':
    init_logging(f'{ROOT_DIR}/logs/ewons')
    logger = logging.getLogger('pipeline')
    main()
    close_logging()
